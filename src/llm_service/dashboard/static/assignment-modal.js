/**
 * Assignment Modal for Orphan Task Specification Linking
 * 
 * Implements SPEC-DASH-008 v1.0.0: Orphan Task Assignment
 * Follows ADR-035 modal UI patterns for consistency
 * 
 * Features:
 * - Task preview (title, agent, priority)
 * - Initiative hierarchy display (expandable)
 * - Client-side search/filter (no backend round-trip)
 * - Feature-level assignment
 * - Conflict resolution dialog
 * - Keyboard navigation (Tab, Escape, Enter)
 * - Performance: Modal load <500ms (P95)
 * 
 * API Integration:
 * - PATCH /api/tasks/:task_id/specification
 * - WebSocket events: task.assigned, task.updated
 */

(function() {
    'use strict';

    // ========================================
    // State Management
    // ========================================
    
    let currentTaskId = null;
    let currentTask = null;
    let initiatives = [];
    let expandedInitiatives = new Set();
    let modalLoadStartTime = null;

    // ========================================
    // Public API
    // ========================================
    
    /**
     * Open assignment modal for an orphan task
     * @param {string} taskId - Task ID to assign
     * @param {Object} taskData - Task metadata (optional, for preview)
     */
    async function openAssignmentModal(taskId, taskData = null) {
        modalLoadStartTime = performance.now();
        currentTaskId = taskId;
        currentTask = taskData;
        
        // Show modal immediately
        const modal = document.getElementById('assignment-modal');
        if (!modal) {
            console.error('Assignment modal element not found');
            return;
        }
        
        modal.classList.remove('hidden');
        modal.setAttribute('aria-hidden', 'false');
        
        // Disable body scroll
        document.body.style.overflow = 'hidden';
        
        try {
            // Load task data if not provided
            if (!currentTask) {
                currentTask = await fetchTaskData(taskId);
            }
            
            // Display task preview
            displayTaskPreview(currentTask);
            
            // Load initiatives from portfolio API (should be cached)
            initiatives = await fetchInitiatives();
            
            // Render initiative list
            renderInitiativeList(initiatives);
            
            // Focus search input for keyboard accessibility
            const searchInput = document.getElementById('spec-search');
            if (searchInput) {
                setTimeout(() => searchInput.focus(), 100);
            }
            
            // Track performance
            const loadTime = performance.now() - modalLoadStartTime;
            console.log(`✅ Modal loaded in ${loadTime.toFixed(2)}ms`);
            
            if (loadTime > 500) {
                console.warn(`⚠️ Modal load time exceeded 500ms: ${loadTime.toFixed(2)}ms`);
            }
            
        } catch (error) {
            console.error('Failed to open assignment modal:', error);
            showErrorToast('Failed to load assignment modal. Please try again.');
            closeAssignmentModal();
        }
    }
    
    /**
     * Close assignment modal
     */
    function closeAssignmentModal() {
        const modal = document.getElementById('assignment-modal');
        if (modal) {
            modal.classList.add('hidden');
            modal.setAttribute('aria-hidden', 'true');
        }
        
        // Re-enable body scroll
        document.body.style.overflow = '';
        
        // Reset state
        currentTaskId = null;
        currentTask = null;
        expandedInitiatives.clear();
        
        // Clear search
        const searchInput = document.getElementById('spec-search');
        if (searchInput) {
            searchInput.value = '';
        }
        
        // Hide dialogs
        hideConflictDialog();
        hideLoadingState();
    }

    // ========================================
    // Data Fetching
    // ========================================
    
    /**
     * Fetch task data from backend
     */
    async function fetchTaskData(taskId) {
        // For now, task data should be provided by caller
        // If we need to fetch it, we'd use the tasks API
        // but typically the orphan task is already in the portfolio data
        throw new Error('Task data must be provided to openAssignmentModal');
    }
    
    /**
     * Fetch initiatives from portfolio API
     * This data should be cached by the dashboard
     */
    async function fetchInitiatives() {
        const response = await fetch('/api/portfolio');
        if (!response.ok) {
            throw new Error(`Failed to fetch portfolio: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Transform to format needed for modal
        return (data.initiatives || []).map(initiative => ({
            id: initiative.id,
            title: initiative.title,
            status: initiative.status,
            priority: initiative.priority,
            specifications: (initiative.specifications || []).map(spec => ({
                id: spec.id,
                title: spec.title,
                path: spec.specification_path,
                status: spec.status,
                priority: spec.priority
            }))
        }));
    }

    // ========================================
    // UI Rendering
    // ========================================
    
    /**
     * Display task preview in modal header
     */
    function displayTaskPreview(task) {
        const titleEl = document.getElementById('assignment-task-title');
        const agentEl = document.getElementById('assignment-task-agent');
        const priorityEl = document.getElementById('assignment-task-priority');
        
        if (titleEl) {
            titleEl.textContent = task.title || task.id;
        }
        
        if (agentEl) {
            agentEl.textContent = task.agent || 'unassigned';
            agentEl.className = `badge agent-${(task.agent || 'unassigned').toLowerCase()}`;
        }
        
        if (priorityEl) {
            priorityEl.textContent = task.priority || 'MEDIUM';
            priorityEl.className = `badge priority-${(task.priority || 'medium').toLowerCase()}`;
        }
    }
    
    /**
     * Render initiative list with specifications
     */
    function renderInitiativeList(initiativeList) {
        const listEl = document.getElementById('initiative-list');
        if (!listEl) return;
        
        if (initiativeList.length === 0) {
            listEl.innerHTML = '<div class="empty-state">No initiatives found. Add specifications to see them here.</div>';
            return;
        }
        
        listEl.innerHTML = initiativeList.map(initiative => 
            createInitiativeElement(initiative)
        ).join('');
        
        // Attach event listeners
        attachInitiativeListeners();
    }
    
    /**
     * Create HTML for a single initiative
     */
    function createInitiativeElement(initiative) {
        const isExpanded = expandedInitiatives.has(initiative.id);
        const expandIcon = isExpanded ? '▼' : '▶';
        const bodyClass = isExpanded ? '' : 'hidden';
        
        const specsHtml = initiative.specifications.length > 0 
            ? initiative.specifications.map(spec => createSpecificationElement(spec, initiative.id)).join('')
            : '<div class="empty-state">No specifications defined</div>';
        
        return `
            <div class="initiative-item" data-initiative-id="${escapeHtml(initiative.id)}">
                <div class="initiative-header" data-action="toggle-initiative">
                    <span class="expand-icon">${expandIcon}</span>
                    <div class="initiative-info">
                        <h4 class="initiative-title">${escapeHtml(initiative.title)}</h4>
                        <div class="initiative-meta">
                            <span class="badge status-${initiative.status}">${escapeHtml(initiative.status)}</span>
                            <span class="badge priority-${(initiative.priority || 'medium').toLowerCase()}">${escapeHtml(initiative.priority || 'MEDIUM')}</span>
                            <span>${initiative.specifications.length} spec${initiative.specifications.length !== 1 ? 's' : ''}</span>
                        </div>
                    </div>
                </div>
                <div class="specification-list ${bodyClass}">
                    ${specsHtml}
                </div>
            </div>
        `;
    }
    
    /**
     * Create HTML for a single specification (feature)
     */
    function createSpecificationElement(spec, initiativeId) {
        return `
            <div class="specification-item" data-spec-id="${escapeHtml(spec.id)}">
                <div class="specification-info">
                    <span class="spec-icon">📄</span>
                    <span class="spec-title">${escapeHtml(spec.title)}</span>
                    <span class="badge status-${spec.status}">${escapeHtml(spec.status)}</span>
                </div>
                <button 
                    class="btn-assign"
                    data-action="assign-task"
                    data-spec-path="${escapeHtml(spec.path)}"
                    data-spec-title="${escapeHtml(spec.title)}"
                    aria-label="Assign to ${escapeHtml(spec.title)}">
                    Assign to ${escapeHtml(spec.title)}
                </button>
            </div>
        `;
    }

    // ========================================
    // Event Handlers
    // ========================================
    
    /**
     * Attach event listeners to initiative list
     */
    function attachInitiativeListeners() {
        const listEl = document.getElementById('initiative-list');
        if (!listEl) return;
        
        // Use event delegation for efficiency
        listEl.addEventListener('click', handleInitiativeListClick);
    }
    
    /**
     * Handle clicks within initiative list (event delegation)
     */
    function handleInitiativeListClick(event) {
        const target = event.target.closest('[data-action]');
        if (!target) return;
        
        const action = target.dataset.action;
        
        if (action === 'toggle-initiative') {
            const initiativeItem = target.closest('.initiative-item');
            if (initiativeItem) {
                toggleInitiative(initiativeItem);
            }
        } else if (action === 'assign-task') {
            const specPath = target.dataset.specPath;
            const specTitle = target.dataset.specTitle;
            if (specPath) {
                assignTask(specPath, specTitle);
            }
        }
    }
    
    /**
     * Toggle initiative expansion
     */
    function toggleInitiative(initiativeItem) {
        const initiativeId = initiativeItem.dataset.initiativeId;
        const specList = initiativeItem.querySelector('.specification-list');
        const expandIcon = initiativeItem.querySelector('.expand-icon');
        
        if (!specList || !expandIcon) return;
        
        if (expandedInitiatives.has(initiativeId)) {
            expandedInitiatives.delete(initiativeId);
            specList.classList.add('hidden');
            expandIcon.textContent = '▶';
        } else {
            expandedInitiatives.add(initiativeId);
            specList.classList.remove('hidden');
            expandIcon.textContent = '▼';
        }
    }
    
    /**
     * Search/filter initiatives
     */
    function handleSearch(event) {
        const query = event.target.value.toLowerCase().trim();
        
        if (!query) {
            // Show all initiatives
            renderInitiativeList(initiatives);
            return;
        }
        
        // Client-side filter
        const startTime = performance.now();
        
        const filtered = initiatives.map(initiative => {
            // Check if initiative title matches
            const initiativeMatches = initiative.title.toLowerCase().includes(query);
            
            // Filter specifications
            const matchingSpecs = initiative.specifications.filter(spec => 
                spec.title.toLowerCase().includes(query)
            );
            
            // Include initiative if it matches OR has matching specs
            if (initiativeMatches || matchingSpecs.length > 0) {
                return {
                    ...initiative,
                    specifications: initiativeMatches ? initiative.specifications : matchingSpecs
                };
            }
            
            return null;
        }).filter(Boolean);
        
        const filterTime = performance.now() - startTime;
        console.log(`🔍 Filter completed in ${filterTime.toFixed(2)}ms`);
        
        if (filterTime > 100) {
            console.warn(`⚠️ Filter time exceeded 100ms: ${filterTime.toFixed(2)}ms`);
        }
        
        renderInitiativeList(filtered);
    }

    // ========================================
    // Task Assignment
    // ========================================
    
    /**
     * Assign task to specification
     */
    async function assignTask(specPath, specTitle) {
        if (!currentTaskId) {
            console.error('No task ID set');
            return;
        }
        
        // Show loading state
        showLoadingState();
        
        try {
            const response = await fetch(`/api/tasks/${currentTaskId}/specification`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    specification: specPath,
                    feature: specTitle
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                
                // Success!
                showSuccessToast(`Task assigned to ${specTitle}`);
                closeAssignmentModal();
                
                // Refresh portfolio to show updated task location
                if (window.loadPortfolioData) {
                    window.loadPortfolioData();
                }
                
            } else if (response.status === 409) {
                // Concurrent edit conflict
                const error = await response.json();
                showConflictDialog(error.error || 'This task was modified by another user.');
                
            } else {
                // Other error
                const error = await response.json();
                showErrorToast(error.error || 'Failed to assign task');
            }
            
        } catch (error) {
            console.error('Failed to assign task:', error);
            showErrorToast('Network error. Please check your connection and try again.');
            
        } finally {
            hideLoadingState();
        }
    }

    // ========================================
    // Loading & Dialog States
    // ========================================
    
    function showLoadingState() {
        const loadingEl = document.getElementById('assignment-loading-state');
        if (loadingEl) {
            loadingEl.classList.remove('hidden');
        }
    }
    
    function hideLoadingState() {
        const loadingEl = document.getElementById('assignment-loading-state');
        if (loadingEl) {
            loadingEl.classList.add('hidden');
        }
    }
    
    function showConflictDialog(message) {
        const dialogEl = document.getElementById('assignment-conflict-dialog');
        const messageEl = document.getElementById('conflict-message');
        
        if (dialogEl) {
            dialogEl.classList.remove('hidden');
        }
        
        if (messageEl) {
            messageEl.textContent = message;
        }
    }
    
    function hideConflictDialog() {
        const dialogEl = document.getElementById('assignment-conflict-dialog');
        if (dialogEl) {
            dialogEl.classList.add('hidden');
        }
    }
    
    /**
     * Refresh modal data (for conflict resolution)
     */
    async function refreshModal() {
        hideConflictDialog();
        
        if (currentTaskId) {
            // Re-open modal with refreshed data
            closeAssignmentModal();
            
            // Refresh portfolio first
            if (window.loadPortfolioData) {
                await window.loadPortfolioData();
            }
            
            // Task might have been assigned already, so just show toast
            showSuccessToast('Data refreshed. Please try assigning again.');
        }
    }

    // ========================================
    // Keyboard Navigation
    // ========================================
    
    /**
     * Handle keyboard events in modal
     */
    function handleKeydown(event) {
        const modal = document.getElementById('assignment-modal');
        if (!modal || modal.classList.contains('hidden')) {
            return;
        }
        
        // Escape key: close modal
        if (event.key === 'Escape') {
            event.preventDefault();
            closeAssignmentModal();
        }
        
        // Enter key: trigger focused button
        if (event.key === 'Enter' && event.target.tagName === 'BUTTON') {
            event.preventDefault();
            event.target.click();
        }
    }

    // ========================================
    // Utility Functions
    // ========================================
    
    /**
     * Escape HTML to prevent XSS
     */
    function escapeHtml(text) {
        if (typeof text !== 'string') return '';
        
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    /**
     * Show success toast notification
     */
    function showSuccessToast(message) {
        if (window.showToast) {
            window.showToast('success', message);
        } else {
            // Fallback: simple console log
            console.log('✅', message);
        }
    }
    
    /**
     * Show error toast notification
     */
    function showErrorToast(message) {
        if (window.showToast) {
            window.showToast('error', message);
        } else {
            // Fallback: simple console log
            console.error('❌', message);
        }
    }

    // ========================================
    // Initialization
    // ========================================
    
    /**
     * Initialize assignment modal
     */
    function initAssignmentModal() {
        console.log('🔧 Initializing assignment modal');
        
        // Set up search input listener
        const searchInput = document.getElementById('spec-search');
        if (searchInput) {
            searchInput.addEventListener('input', handleSearch);
        }
        
        // Set up keyboard navigation
        document.addEventListener('keydown', handleKeydown);
        
        // Set up close button
        const closeBtn = document.getElementById('assignment-modal-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', closeAssignmentModal);
        }
        
        // Set up backdrop click to close
        const modal = document.getElementById('assignment-modal');
        if (modal) {
            modal.addEventListener('click', (event) => {
                if (event.target === modal) {
                    closeAssignmentModal();
                }
            });
        }
        
        // Set up conflict dialog buttons
        const refreshBtn = document.getElementById('conflict-refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', refreshModal);
        }
        
        const cancelBtn = document.getElementById('conflict-cancel-btn');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', hideConflictDialog);
        }
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAssignmentModal);
    } else {
        initAssignmentModal();
    }

    // ========================================
    // Public API Export
    // ========================================
    
    // Export to global scope for use by dashboard
    window.openAssignmentModal = openAssignmentModal;
    window.closeAssignmentModal = closeAssignmentModal;

})();
