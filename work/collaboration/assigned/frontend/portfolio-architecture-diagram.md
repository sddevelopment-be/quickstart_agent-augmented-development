# Portfolio View Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    📊 Portfolio Overview                        │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ ▶ Dashboard Enhancements Initiative                  47%  │ │
│  │   ████████░░░░░░░░░░░░  (2/6 tasks)                       │ │
│  │   [HIGH] [in_progress]  3 features                        │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ ▼ Configuration Management Initiative            100%     │ │
│  │   ████████████████████████████  (5/5 tasks)               │ │
│  │   [CRITICAL] [completed]  2 features                      │ │
│  │                                                            │ │
│  │   ├─ ▼ Backend Configuration                     100%    │ │
│  │   │     ████████████████████████████  (3/3)              │ │
│  │   │     [completed]  3 tasks                             │ │
│  │   │                                                       │ │
│  │   │     ├─ ✅ Config Schema Definition                   │ │
│  │   │     │   👤 backend-dev  [HIGH]                       │ │
│  │   │     │                                                 │ │
│  │   │     ├─ ✅ YAML Parser Implementation                 │ │
│  │   │     │   👤 backend-dev  [MEDIUM]                     │ │
│  │   │     │                                                 │ │
│  │   │     └─ ✅ Validation Layer                           │ │
│  │   │         👤 backend-dev  [HIGH]                       │ │
│  │   │                                                       │ │
│  │   └─ ▼ Frontend Configuration UI               100%     │ │
│  │         ████████████████████████████  (2/2)              │ │
│  │         [completed]  2 tasks                             │ │
│  │                                                           │ │
│  │         ├─ ✅ Config Editor Component                    │ │
│  │         │   👤 frontend-freddy  [MEDIUM]                 │ │
│  │         │                                                 │ │
│  │         └─ ✅ Live Preview Panel                         │ │
│  │             👤 frontend-freddy  [LOW]                    │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ ⚠️ Orphan Tasks (12 tasks)                               │ │
│  │                                                            │ │
│  │  ┌────────────────┐  ┌────────────────┐  ┌─────────────┐│ │
│  │  │📋 Legacy Setup │  │📋 Dependency   │  │📋 Misc Fix  ││ │
│  │  │👤 unassigned   │  │   Update       │  │👤 architect ││ │
│  │  │[MEDIUM]        │  │👤 backend-dev  │  │[LOW]        ││ │
│  │  └────────────────┘  │[HIGH]          │  └─────────────┘│ │
│  │                      └────────────────┘                   │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Component Hierarchy

```
PortfolioSection
├─ PortfolioContainer
│  └─ InitiativeCard[] (multiple)
│     ├─ InitiativeHeader (clickable)
│     │  ├─ Toggle icon (▶/▼)
│     │  ├─ InitiativeInfo
│     │  │  ├─ Title
│     │  │  └─ Meta (status, priority, feature count)
│     │  └─ ProgressBar
│     │     ├─ ProgressFill (colored)
│     │     └─ ProgressText (percentage/count)
│     │
│     └─ InitiativeBody (expandable)
│        └─ FeatureItem[] (multiple)
│           ├─ FeatureHeader (clickable)
│           │  ├─ Toggle icon (▶/▼)
│           │  ├─ FeatureInfo
│           │  │  ├─ Title
│           │  │  └─ Meta (status, task count)
│           │  └─ ProgressBar
│           │
│           └─ TaskListContainer (expandable)
│              └─ TaskItem[] (multiple, clickable)
│                 ├─ StatusIcon (✅⏳🔄📋)
│                 ├─ TaskTitle
│                 └─ TaskAgent
│
└─ OrphanSection (conditional)
   ├─ Header (⚠️ + count)
   ├─ Description
   └─ OrphanTasksList (grid)
      └─ OrphanTaskCard[] (multiple, clickable)
         ├─ StatusIcon + Title
         └─ Meta (agent, priority)
```

## Data Flow

```
┌──────────────┐
│   Backend    │
│  /api/       │
│  portfolio   │
└──────┬───────┘
       │
       │ HTTP GET
       │
       ▼
┌──────────────────┐
│ loadPortfolio    │ ◄──┐ WebSocket Events
│ Data()           │    │ (task.completed,
└──────┬───────────┘    │  task.updated)
       │                │
       │ JSON            │
       │                │
       ▼                │
┌──────────────────┐    │
│ renderPortfolio  │    │
│ (data)           │    │
└──────┬───────────┘    │
       │                │
       ├─────────┐      │
       │         │      │
       ▼         ▼      │
 ┌─────────┐ ┌─────────┐
 │Initiatives│ │Orphans │
 └────┬────┘ └────┬────┘
      │           │
      ▼           ▼
 ┌─────────┐ ┌─────────┐
 │Features │ │ Cards   │
 └────┬────┘ └─────────┘
      │
      ▼
 ┌─────────┐
 │ Tasks   │
 └─────────┘
```

## State Management

```
Expand/Collapse State:
┌──────────────────────────────────────┐
│ DOM Classes (Source of Truth)       │
├──────────────────────────────────────┤
│ .initiative-body.expanded            │
│ .task-list-container.expanded        │
│ .initiative-toggle.expanded          │
│ .feature-toggle.expanded             │
└──────────────────────────────────────┘
        ▲                   │
        │ CSS               │ JavaScript
        │ Animations        │ Toggle
        │                   ▼
┌───────────────────────────────────────┐
│ User Interaction                      │
│ - Click initiative header             │
│ - Click feature header                │
└───────────────────────────────────────┘
```

## Event Flow

```
User Action                 JavaScript                  Visual Update
───────────────────────────────────────────────────────────────────

Click Initiative    →   toggleInitiative(id)    →   .expanded class
   Header                                              Arrow rotates
                                                       Body slides down

Click Feature       →   toggleFeature(id)       →   .expanded class
   Header                                              Arrow rotates
                                                       Tasks appear

Click Task          →   openTaskFromPortfolio() →   Modal opens
                        ↓
                        fetch /api/tasks
                        ↓
                        Find task by ID
                        ↓
                        showTaskModal(task)

WebSocket Event     →   loadPortfolioData()     →   Portfolio refreshes
(task.completed)        ↓                            Progress updates
                        fetch /api/portfolio          Colors change
                        ↓
                        renderPortfolio(data)
```

## CSS Animation Timeline

```
Expand Animation (slideDown):
───────────────────────────────────────
0ms     50ms    100ms   150ms   200ms
│       │       │       │       │
├───────┼───────┼───────┼───────┤
│       │       │       │       │
opacity: 0      0.3     0.6     1.0
transform:
  Y: -10px      -5px    -2px    0px
```

## Function Call Graph

```
initDashboard()
├─ loadDashboardData()
└─ loadPortfolioData()
   └─ fetch('/api/portfolio')
      └─ renderPortfolio(data)
         ├─ createInitiativeCard() × N
         │  └─ createFeatureItem() × N
         │     ├─ createTaskItem() × N
         │     └─ createProgressBar()
         │        └─ getProgressClass()
         │
         └─ createOrphanTaskCard() × N
            └─ getTaskStatusIcon()

toggleInitiative(id)
└─ DOM manipulation
   └─ .classList.toggle('expanded')

toggleFeature(id, featureId)
└─ DOM manipulation
   └─ .classList.toggle('expanded')

openTaskFromPortfolio(taskId)
└─ fetch('/api/tasks')
   └─ Find task
      └─ showTaskModal(task)

WebSocket Events
├─ socket.on('task.completed')
│  └─ loadPortfolioData()
└─ socket.on('task.updated')
   └─ if (field === 'status')
      └─ loadPortfolioData()
```

## Progress Bar Color Logic

```
getProgressClass(progress)
│
├─ if progress === 0 → 'progress-0-33' (Red)
├─ if progress <= 33 → 'progress-0-33' (Red)
├─ if progress <= 66 → 'progress-34-66' (Orange)
├─ if progress < 100 → 'progress-67-99' (Yellow)
└─ else             → 'progress-100' (Green)

CSS Variables:
--danger-color: #ef4444   (Red)
--warning-color: #f59e0b  (Orange)
--success-color: #10b981  (Green)
(Yellow): #eab308
```

## Responsive Breakpoints

```
Desktop (1400px+)
├─ Full 3-column kanban
├─ Sidebar visible
└─ Portfolio full width

Tablet (768px - 1024px)
├─ 2-column grid
├─ Sidebar stacks
└─ Portfolio responsive

Mobile (<768px)
├─ Single column
├─ Sidebar vertical
└─ Portfolio stacked
```

## File Size Impact

```
Before (Dashboard only):
├─ index.html: 165 lines
├─ dashboard.css: 746 lines
└─ dashboard.js: 742 lines
Total: 1,653 lines

After (+ Portfolio):
├─ index.html: 188 lines (+23, +13.9%)
├─ dashboard.css: 1,046 lines (+300, +40.2%)
└─ dashboard.js: 1,007 lines (+265, +35.7%)
Total: 2,241 lines (+588, +35.6%)

CSS gzipped: ~8KB → ~12KB (+4KB)
JS gzipped: ~12KB → ~15KB (+3KB)
Total bundle: +7KB (acceptable)
```
