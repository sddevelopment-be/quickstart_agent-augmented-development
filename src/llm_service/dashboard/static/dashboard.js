// LLM Service Dashboard - Frontend Logic
// WebSocket client with auto-reconnection and real-time updates

(function() {
    'use strict';

    // Configuration
    const SOCKET_URL = window.location.origin;
    const SOCKET_NAMESPACE = '/dashboard';
    const RECONNECT_DELAY = 3000;

    // State
    let socket = null;
    let costChart = null;
    let modelChart = null;
    let reconnectAttempts = 0;

    // Initialize dashboard on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initDashboard);
    } else {
        initDashboard();
    }

    function initDashboard() {
        console.log('🚀 Initializing LLM Service Dashboard');
        
        // Connect to WebSocket
        connectWebSocket();
        
        // Initialize charts
        initializeCharts();
        
        // Load initial data
        loadDashboardData();
        
        // Set up periodic refresh (fallback if WebSocket fails)
        setInterval(loadDashboardData, 30000); // Every 30 seconds
        
        // Hide loading overlay
        setTimeout(() => {
            document.getElementById('loading-overlay').classList.add('hidden');
        }, 1000);
    }

    function connectWebSocket() {
        console.log('📡 Connecting to WebSocket...', SOCKET_URL + SOCKET_NAMESPACE);
        
        socket = io(SOCKET_URL + SOCKET_NAMESPACE, {
            transports: ['websocket', 'polling'],
            reconnection: true,
            reconnectionDelay: RECONNECT_DELAY,
            reconnectionAttempts: Infinity
        });

        // Connection events
        socket.on('connect', () => {
            console.log('✅ WebSocket connected');
            updateConnectionStatus('connected');
            reconnectAttempts = 0;
            addActivity('System', 'Dashboard connected', 'connected');
        });

        socket.on('disconnect', () => {
            console.log('⚠️ WebSocket disconnected');
            updateConnectionStatus('disconnected');
            addActivity('System', 'Dashboard disconnected', 'disconnected');
        });

        socket.on('connect_error', (error) => {
            console.error('❌ WebSocket connection error:', error);
            updateConnectionStatus('connecting');
            reconnectAttempts++;
        });

        // Dashboard events
        socket.on('connection_ack', (data) => {
            console.log('📨 Connection acknowledged:', data);
        });

        socket.on('task.created', (data) => {
            console.log('📋 Task created:', data);
            handleTaskCreated(data);
            addActivity('Task Created', data.task.title || data.task.id, 'created');
        });

        socket.on('task.assigned', (data) => {
            console.log('🔄 Task assigned:', data);
            handleTaskAssigned(data);
            addActivity('Task Assigned', `${data.task.title || data.task.id} → ${data.task.agent}`, 'assigned');
        });

        socket.on('task.completed', (data) => {
            console.log('✅ Task completed:', data);
            handleTaskCompleted(data);
            addActivity('Task Completed', data.task.title || data.task.id, 'completed');
        });

        socket.on('task.updated', (data) => {
            console.log('🔄 Task updated:', data);
            
            // Real-time priority sync (ADR-035)
            if (data.field === 'priority') {
                updatePriorityInUI(data.task_id, data.new_value);
            }
            
            handleTaskUpdated(data);
        });

        socket.on('cost.update', (data) => {
            console.log('💰 Cost update:', data);
            updateCostMetrics(data.costs);
            updateCharts(data);
        });

        socket.on('pong', (data) => {
            console.log('🏓 Pong received:', data);
        });

        // Keep-alive ping every 30 seconds
        setInterval(() => {
            if (socket && socket.connected) {
                socket.emit('ping');
            }
        }, 30000);
    }

    function updateConnectionStatus(status) {
        const indicator = document.getElementById('connection-indicator');
        const text = document.getElementById('connection-text');
        
        indicator.className = 'status-indicator';
        
        switch(status) {
            case 'connected':
                indicator.classList.add('status-connected');
                text.textContent = 'Connected';
                break;
            case 'disconnected':
                indicator.classList.add('status-disconnected');
                text.textContent = 'Disconnected';
                break;
            case 'connecting':
                indicator.classList.add('status-connecting');
                text.textContent = reconnectAttempts > 0 
                    ? `Reconnecting (${reconnectAttempts})...` 
                    : 'Connecting...';
                break;
        }
    }

    async function loadDashboardData() {
        try {
            // Load task snapshot
            const tasksResponse = await fetch('/api/tasks');
            const tasksData = await tasksResponse.json();
            updateTaskBoard(tasksData);

            // Load stats
            const statsResponse = await fetch('/api/stats');
            const statsData = await statsResponse.json();
            updateCostMetrics(statsData.costs);

            updateLastUpdated();
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
        }
    }

    function updateTaskBoard(data) {
        // Update inbox
        updateTaskColumn('inbox', data.inbox || []);
        
        // Update assigned (nested by agent)
        const assignedTasks = [];
        if (data.assigned && typeof data.assigned === 'object') {
            for (const agent in data.assigned) {
                assignedTasks.push(...data.assigned[agent]);
            }
        }
        updateTaskColumn('assigned', assignedTasks);
        
        // Update done (nested by agent)
        const doneTasks = [];
        if (data.done && typeof data.done === 'object') {
            for (const agent in data.done) {
                doneTasks.push(...data.done[agent]);
            }
        }
        updateTaskColumn('done', doneTasks);
        
        // Update active tasks count
        document.getElementById('tasks-active').textContent = 
            (data.inbox?.length || 0) + assignedTasks.length;
    }

    function updateTaskColumn(columnId, tasks) {
        const container = document.getElementById(`${columnId}-tasks`);
        const countElement = document.getElementById(`${columnId}-count`);
        
        countElement.textContent = tasks.length;
        
        if (tasks.length === 0) {
            container.innerHTML = `<div class="empty-state">No ${columnId} tasks</div>`;
            return;
        }
        
        // Sort tasks by latest change/creation (newest first)
        const sortedTasks = tasks.slice().sort((a, b) => {
            const dateA = new Date(a.updated_at || a.created_at || 0);
            const dateB = new Date(b.updated_at || b.created_at || 0);
            return dateB - dateA; // Descending order (newest first)
        });
        
        container.innerHTML = sortedTasks.map(task => createTaskCard(task)).join('');
        
        // Add click handlers for task cards (excluding priority dropdowns)
        container.querySelectorAll('.task-card').forEach((card, index) => {
            card.addEventListener('click', (event) => {
                // Don't open modal if clicking on priority dropdown
                if (event.target.classList.contains('priority-dropdown') || 
                    event.target.closest('.priority-dropdown-container')) {
                    return;
                }
                showTaskModal(sortedTasks[index]);
            });
        });
        
        // Wire priority dropdown handlers
        attachPriorityHandlers();
    }

    function createTaskCard(task) {
        const priority = task.priority || 'medium';
        const agent = task.agent || 'unassigned';
        const createdAt = task.created_at ? new Date(task.created_at).toLocaleString() : 'Unknown';
        
        return `
            <div class="task-card priority-${priority.toLowerCase()}">
                <h4>${escapeHtml(task.title || task.id)}</h4>
                <div class="task-meta">
                    <span>👤 ${escapeHtml(agent)}</span>
                    ${createPriorityControl(task)}
                    <span>🕐 ${createdAt}</span>
                </div>
            </div>
        `;
    }
    
    function createPriorityControl(task) {
        const priority = task.priority || 'MEDIUM';
        const status = task.status || 'inbox';
        const isEditable = isTaskEditable(status);
        
        // In-progress indicator (pulsing dot)
        const inProgressIndicator = status === 'in_progress' 
            ? '<span class="in-progress-dot"></span>' 
            : '';
        
        if (!isEditable) {
            // Non-editable: show badge with tooltip
            return `
                <span class="priority-badge priority-${priority.toLowerCase()} disabled"
                      title="Cannot edit ${status} tasks"
                      data-task-id="${escapeHtml(task.id)}">
                    ${inProgressIndicator}
                    🏷️ ${escapeHtml(priority)}
                </span>
            `;
        }
        
        // Editable: dropdown
        return `
            <div class="priority-dropdown-container" data-task-id="${escapeHtml(task.id)}">
                <select class="priority-dropdown" 
                        data-task-id="${escapeHtml(task.id)}"
                        data-original-priority="${escapeHtml(priority)}">
                    ${createPriorityOptions(priority)}
                </select>
                <span class="priority-spinner hidden">⏳</span>
                <span class="priority-success hidden">✅</span>
            </div>
        `;
    }
    
    function createPriorityOptions(currentPriority) {
        const priorities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'normal'];
        return priorities.map(p => {
            const selected = p === currentPriority ? 'selected' : '';
            return `<option value="${p}" ${selected}>${p}</option>`;
        }).join('');
    }
    
    function isTaskEditable(status) {
        const nonEditableStatuses = ['in_progress', 'done', 'failed'];
        return !nonEditableStatuses.includes(status);
    }

    function handleTaskCreated(data) {
        loadDashboardData(); // Reload entire board
    }

    function handleTaskAssigned(data) {
        loadDashboardData(); // Reload entire board
    }

    function handleTaskCompleted(data) {
        loadDashboardData(); // Reload entire board
    }

    function handleTaskUpdated(data) {
        loadDashboardData(); // Reload entire board
    }

    function updateCostMetrics(costs) {
        if (!costs) return;
        
        document.getElementById('cost-today').textContent = `$${costs.today?.toFixed(2) || '0.00'}`;
        document.getElementById('cost-month').textContent = `$${costs.month?.toFixed(2) || '0.00'}`;
        document.getElementById('cost-total').textContent = `$${costs.total?.toFixed(2) || '0.00'}`;
    }

    function initializeCharts() {
        // Cost trend chart
        const costCtx = document.getElementById('cost-chart');
        if (costCtx) {
            costChart = new Chart(costCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Daily Cost (USD)',
                        data: [],
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: { display: false },
                        title: { display: false }
                    },
                    scales: {
                        y: { 
                            beginAtZero: true,
                            ticks: { 
                                color: '#cbd5e1',
                                callback: value => '$' + value.toFixed(2)
                            },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' }
                        },
                        x: {
                            ticks: { color: '#cbd5e1' },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' }
                        }
                    }
                }
            });
        }

        // Model usage chart
        const modelCtx = document.getElementById('model-chart');
        if (modelCtx) {
            modelChart = new Chart(modelCtx, {
                type: 'doughnut',
                data: {
                    labels: [],
                    datasets: [{
                        data: [],
                        backgroundColor: [
                            '#3b82f6',
                            '#10b981',
                            '#f59e0b',
                            '#ef4444',
                            '#8b5cf6',
                            '#ec4899'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: '#cbd5e1' }
                        }
                    }
                }
            });
        }
    }

    function updateCharts(data) {
        // Update cost trend chart
        if (costChart && data.trends) {
            costChart.data.labels = data.trends.map(t => t.date);
            costChart.data.datasets[0].data = data.trends.map(t => t.cost_usd);
            costChart.update();
        }

        // Update model usage chart
        if (modelChart && data.models) {
            modelChart.data.labels = data.models.map(m => m.model_name);
            modelChart.data.datasets[0].data = data.models.map(m => m.total_cost_usd);
            modelChart.update();
        }
    }

    function addActivity(type, message, category) {
        const feed = document.getElementById('activity-feed');
        const emptyState = feed.querySelector('.empty-state');
        if (emptyState) emptyState.remove();
        
        const timestamp = new Date().toLocaleTimeString();
        const activityHTML = `
            <div class="activity-item activity-${category}">
                <div class="activity-item-header">
                    <strong>${escapeHtml(type)}</strong>
                    <span class="activity-item-time">${timestamp}</span>
                </div>
                <p>${escapeHtml(message)}</p>
            </div>
        `;
        
        feed.insertAdjacentHTML('afterbegin', activityHTML);
        
        // Keep only last 20 items
        const items = feed.querySelectorAll('.activity-item');
        if (items.length > 20) {
            items[items.length - 1].remove();
        }
    }

    // ========================================
    // Priority Editing Functions (ADR-035)
    // ========================================
    
    function attachPriorityHandlers() {
        document.querySelectorAll('.priority-dropdown').forEach(dropdown => {
            dropdown.removeEventListener('change', handlePriorityChange); // Prevent duplicates
            dropdown.addEventListener('change', handlePriorityChange);
        });
    }

    async function handlePriorityChange(event) {
        const dropdown = event.target;
        const taskId = dropdown.dataset.taskId;
        const newPriority = dropdown.value;
        const originalPriority = dropdown.dataset.originalPriority;
        
        // Skip if no actual change
        if (newPriority === originalPriority) return;
        
        // Update UI to loading state
        showPriorityLoading(taskId, true);
        dropdown.disabled = true;
        
        try {
            // API call with optimistic locking
            const response = await fetch(`/api/tasks/${taskId}/priority`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    priority: newPriority,
                    // TODO: Add last_modified from task data for optimistic locking
                })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || `HTTP ${response.status}`);
            }
            
            const result = await response.json();
            
            // Success: update original value, show feedback
            dropdown.dataset.originalPriority = newPriority;
            showPrioritySuccess(taskId);
            
            // Add activity log
            addActivity('Priority Updated', `${taskId} → ${newPriority}`, 'updated');
            
        } catch (error) {
            // Error: rollback, show error
            dropdown.value = originalPriority;
            showPriorityError(taskId, error.message);
            addActivity('Priority Error', `${taskId}: ${error.message}`, 'error');
        } finally {
            showPriorityLoading(taskId, false);
            dropdown.disabled = false;
        }
    }

    function showPriorityLoading(taskId, isLoading) {
        const containers = document.querySelectorAll(`.priority-dropdown-container[data-task-id="${taskId}"]`);
        containers.forEach(container => {
            const spinner = container.querySelector('.priority-spinner');
            if (spinner) {
                spinner.classList.toggle('hidden', !isLoading);
            }
        });
    }

    function showPrioritySuccess(taskId) {
        const containers = document.querySelectorAll(`.priority-dropdown-container[data-task-id="${taskId}"]`);
        containers.forEach(container => {
            const success = container.querySelector('.priority-success');
            if (success) {
                success.classList.remove('hidden');
                setTimeout(() => success.classList.add('hidden'), 2000);
            }
        });
    }

    function showPriorityError(taskId, message) {
        // Show toast notification
        showToast('error', `Priority Update Failed: ${message}`);
    }

    function showToast(type, message) {
        // Simple toast notification
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => toast.classList.add('show'), 10);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    }
    
    function updatePriorityInUI(taskId, newPriority) {
        // Update dropdowns in task cards and modal
        const dropdowns = document.querySelectorAll(`.priority-dropdown[data-task-id="${taskId}"]`);
        dropdowns.forEach(dropdown => {
            dropdown.value = newPriority;
            dropdown.dataset.originalPriority = newPriority;
        });
        
        // Update badges for disabled tasks
        const badges = document.querySelectorAll(`.priority-badge[data-task-id="${taskId}"]`);
        badges.forEach(badge => {
            badge.textContent = `🏷️ ${newPriority}`;
            // Update class for color coding
            badge.className = `priority-badge priority-${newPriority.toLowerCase()} disabled`;
        });
        
        // Show toast notification (from another user)
        showToast('info', `Priority updated by another user: ${taskId} → ${newPriority}`);
    }

    function showTaskModal(task) {
        const modal = document.getElementById('task-modal');
        const titleElement = document.getElementById('modal-title');
        const bodyElement = document.getElementById('modal-body');
        
        if (!modal || !titleElement || !bodyElement) {
            console.error('Modal elements not found');
            return;
        }
        
        titleElement.textContent = task.title || task.id;
        
        // Build modal HTML with technical fields (plain text)
        bodyElement.innerHTML = `
            <div class="modal-field">
                <label>ID:</label>
                <value>${escapeHtml(task.id)}</value>
            </div>
            <div class="modal-field">
                <label>Agent:</label>
                <value>${escapeHtml(task.agent || 'N/A')}</value>
            </div>
            <div class="modal-field">
                <label>Status:</label>
                <value>${escapeHtml(task.status || 'N/A')}</value>
            </div>
            <div class="modal-field">
                <label>Priority:</label>
                <div class="modal-priority-control">
                    ${createPriorityControl(task)}
                </div>
            </div>
            <div class="modal-field">
                <label>Created:</label>
                <value>${task.created_at ? new Date(task.created_at).toLocaleString() : 'N/A'}</value>
            </div>
            ${task.estimated_hours ? `
            <div class="modal-field">
                <label>Estimated Hours:</label>
                <value>${escapeHtml(task.estimated_hours)}</value>
            </div>
            ` : ''}
            ${task.tags && task.tags.length ? `
            <div class="modal-field">
                <label>Tags:</label>
                <value>${escapeHtml(Array.isArray(task.tags) ? task.tags.join(', ') : task.tags)}</value>
            </div>
            ` : ''}
            ${task.description ? `
            <div class="modal-field">
                <label>Description:</label>
                <div class="markdown-content" id="task-description"></div>
            </div>
            ` : ''}
            ${task.context ? `
            <div class="modal-field">
                <label>Context:</label>
                <div class="markdown-content" id="task-context"></div>
            </div>
            ` : ''}
            ${task.acceptance_criteria ? `
            <div class="modal-field">
                <label>Acceptance Criteria:</label>
                <div class="markdown-content" id="task-acceptance-criteria"></div>
            </div>
            ` : ''}
            ${task.notes ? `
            <div class="modal-field">
                <label>Notes:</label>
                <div class="markdown-content" id="task-notes"></div>
            </div>
            ` : ''}
            ${task.technical_notes ? `
            <div class="modal-field">
                <label>Technical Notes:</label>
                <div class="markdown-content" id="task-technical-notes"></div>
            </div>
            ` : ''}
        `;
        
        // Render markdown fields using MarkdownRenderer (ADR-036)
        // Small delay to ensure DOM elements are available
        setTimeout(() => {
            if (window.MarkdownRenderer) {
                if (task.description) {
                    const descEl = document.getElementById('task-description');
                    if (descEl) {
                        MarkdownRenderer.renderField(descEl, 'description', task.description);
                    }
                }
                
                if (task.context) {
                    const contextEl = document.getElementById('task-context');
                    if (contextEl) {
                        MarkdownRenderer.renderField(contextEl, 'context', task.context);
                    }
                }
                
                if (task.acceptance_criteria) {
                    const acEl = document.getElementById('task-acceptance-criteria');
                    if (acEl) {
                        MarkdownRenderer.renderField(acEl, 'acceptance_criteria', task.acceptance_criteria);
                    }
                }
                
                if (task.notes) {
                    const notesEl = document.getElementById('task-notes');
                    if (notesEl) {
                        MarkdownRenderer.renderField(notesEl, 'notes', task.notes);
                    }
                }
                
                if (task.technical_notes) {
                    const techNotesEl = document.getElementById('task-technical-notes');
                    if (techNotesEl) {
                        MarkdownRenderer.renderField(techNotesEl, 'technical_notes', task.technical_notes);
                    }
                }
            } else {
                console.warn('⚠️ MarkdownRenderer not available, falling back to plain text');
            }
            
            // Wire priority dropdown handlers in modal (ADR-035)
            attachPriorityHandlers();
        }, 10);
        
        modal.classList.remove('hidden');
    }

    // Close modal function (exposed globally for onclick handler)
    window.closeTaskModal = function(event) {
        // Prevent event propagation if called from button click
        if (event && event.stopPropagation) {
            event.stopPropagation();
        }
        
        const modal = document.getElementById('task-modal');
        if (modal) {
            modal.classList.add('hidden');
        }
    };
    
    // Close modal on backdrop click
    document.addEventListener('click', function(event) {
        const modal = document.getElementById('task-modal');
        if (modal && event.target === modal) {
            window.closeTaskModal();
        }
    });
    
    // Close modal on Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            const modal = document.getElementById('task-modal');
            if (modal && !modal.classList.contains('hidden')) {
                window.closeTaskModal();
            }
        }
    });

    function updateLastUpdated() {
        document.getElementById('last-updated').textContent = new Date().toLocaleTimeString();
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Export for debugging
    window.dashboard = {
        socket,
        loadDashboardData,
        updateCharts
    };

    console.log('✅ Dashboard initialized successfully');
})();
