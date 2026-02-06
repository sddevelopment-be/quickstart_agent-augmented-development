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
        
        container.innerHTML = tasks.map(task => createTaskCard(task)).join('');
        
        // Add click handlers
        container.querySelectorAll('.task-card').forEach((card, index) => {
            card.addEventListener('click', () => showTaskModal(tasks[index]));
        });
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
                    <span>🏷️ ${escapeHtml(priority)}</span>
                    <span>🕐 ${createdAt}</span>
                </div>
            </div>
        `;
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
                <value>${escapeHtml(task.priority || 'N/A')}</value>
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
