# Priority Editing UI - Visual Mockup

## Task Card - Editable State

```
┌─────────────────────────────────────────────────┐
│  Design Prompt Optimization Framework           │ ← Task Title
│                                                  │
│  👤 architect-alphonso                          │
│  🏷️ [HIGH ▼]  ⏳  ✅                            │ ← Priority Dropdown + Feedback
│  🕐 Jan 30, 2026, 11:20 AM                      │
│                                                  │
└─────────────────────────────────────────────────┘
         ▲
         └── Dropdown (select element)
             Options: CRITICAL, HIGH, MEDIUM, LOW, normal
             
States:
- DEFAULT: Dropdown enabled, shows current priority
- LOADING: Dropdown disabled, ⏳ spinner visible
- SUCCESS: Dropdown re-enabled, ✅ checkmark visible (2s)
- ERROR: Dropdown reverts, toast notification appears
```

## Task Card - In-Progress (Non-Editable)

```
┌─────────────────────────────────────────────────┐
│  Dashboard Markdown Rendering                    │
│                                                  │
│  👤 frontend-dev                                │
│  ● 🏷️ HIGH                                      │ ← Pulsing dot + Badge
│  🕐 Feb 6, 2026, 10:15 AM                       │
│                                                  │
└─────────────────────────────────────────────────┘
    ▲
    └── Orange pulsing dot indicates in_progress
        Badge is not clickable
        Tooltip: "Cannot edit in_progress tasks"
```

## Task Card - Done (Non-Editable)

```
┌─────────────────────────────────────────────────┐
│  Dashboard WebSocket Integration                 │
│                                                  │
│  👤 backend-dev                                 │
│  🏷️ MEDIUM                                      │ ← Static badge (no dot)
│  🕐 Feb 5, 2026, 3:45 PM                        │
│                                                  │
└─────────────────────────────────────────────────┘
    ▲
    └── Gray badge, no animation
        Tooltip: "Cannot edit done tasks"
```

## Priority Dropdown - Expanded

```
┌─────────────────────┐
│ CRITICAL            │ ← Selected (bold)
├─────────────────────┤
│ HIGH                │
├─────────────────────┤
│ MEDIUM              │
├─────────────────────┤
│ LOW                 │
├─────────────────────┤
│ normal              │
└─────────────────────┘
```

## Toast Notifications

### Success (Info)
```
┌──────────────────────────────────────────────┐
│ ℹ️  Priority updated by another user:        │
│    2026-02-06T1149... → HIGH                 │
└──────────────────────────────────────────────┘
      ▲
      └── Blue left border, auto-dismisses after 5s
```

### Error
```
┌──────────────────────────────────────────────┐
│ ❌ Priority Update Failed:                   │
│    Cannot edit task with status              │
│    'in_progress'. Tasks that are             │
│    in_progress, done, or failed cannot       │
│    be edited.                                │
└──────────────────────────────────────────────┘
      ▲
      └── Red left border, auto-dismisses after 5s
```

## Modal View

```
┌────────────────────────────────────────────────────────┐
│  Design Prompt Optimization Framework           [×]    │
├────────────────────────────────────────────────────────┤
│                                                         │
│  ID:                                                    │
│  2026-01-30T1120-design-prompt-optimization-framework  │
│                                                         │
│  Agent:                                                 │
│  architect-alphonso                                    │
│                                                         │
│  Status:                                                │
│  inbox                                                  │
│                                                         │
│  Priority:                                              │
│  [HIGH ▼]  ⏳  ✅                                      │ ← Same control
│                                                         │
│  Created:                                               │
│  Jan 30, 2026, 11:20 AM                                │
│                                                         │
│  Description:                                           │
│  ┌───────────────────────────────────────────────┐   │
│  │ # Task: Design Prompt Optimization Framework  │   │
│  │                                                │   │
│  │ ## Objective                                   │   │
│  │ Review the efficiency analysis findings...     │   │
│  └───────────────────────────────────────────────┘   │
│                                                         │
└────────────────────────────────────────────────────────┘
```

## Activity Feed

```
┌────────────────────────────────────────────────────────┐
│ 🔔 Recent Activity                                      │
├────────────────────────────────────────────────────────┤
│ Priority Updated                              3:05 PM  │
│ 2026-02-06T1149... → HIGH                              │
├────────────────────────────────────────────────────────┤
│ Task Created                                  3:00 PM  │
│ Dashboard Priority Editing                             │
├────────────────────────────────────────────────────────┤
│ Priority Error                                2:58 PM  │
│ test-task: Invalid priority. Must be one of:          │
│ CRITICAL, HIGH, MEDIUM, LOW, normal                    │
└────────────────────────────────────────────────────────┘
     ▲
     └── Different colors:
         - Updated: Blue border
         - Created: Blue border  
         - Error: Red border
```

## Color Scheme (Dark Theme)

```
Priority Badge Colors:
├─ CRITICAL:  🔴 Red (#ef4444)
├─ HIGH:      🟠 Orange (#f59e0b)
├─ MEDIUM:    🔵 Blue (#3b82f6)
├─ LOW:       ⚪ Gray (#94a3b8)
└─ normal:    ⚫ Dark Gray (#cbd5e1)

In-Progress Dot: 🟠 Orange (#f59e0b) - Pulsing

Toast Borders:
├─ Error:   🔴 Red (#ef4444)
├─ Success: 🟢 Green (#10b981)
├─ Warning: 🟠 Orange (#f59e0b)
└─ Info:    🔵 Blue (#3b82f6)
```

## Animation Sequences

### Priority Change Flow (Visual Timeline)

```
T+0ms     User clicks dropdown, selects "HIGH"
          │
          ▼
T+10ms    Dropdown disabled, spinner appears
          │ [MEDIUM ▼] → [HIGH ▼] ⏳
          ▼
T+50ms    API request sent (PATCH /api/tasks/:id/priority)
          │
          ▼
T+200ms   API responds (200 OK)
          │
          ▼
T+210ms   Success checkmark appears, spinner hidden
          │ [HIGH ▼] ⏳ → [HIGH ▼] ✅
          ▼
T+2210ms  Checkmark fades out
          │ [HIGH ▼] ✅ → [HIGH ▼]
          ▼
T+2220ms  Back to default state
          │ [HIGH ▼]
```

### Pulsing Dot Animation (Continuous Loop)

```
0.0s    ● (100% opacity, scale 1.0)
0.5s    ◌ (50% opacity, scale 1.2)
1.0s    ● (100% opacity, scale 1.0)
1.5s    ◌ (50% opacity, scale 1.2)
2.0s    ● (100% opacity, scale 1.0)
        └─→ Repeat infinitely
```

### Toast Slide-In Animation

```
Initial:  translateY(+100px), opacity 0 (off-screen)
          ↓
After 10ms: (trigger show class)
          ↓
300ms:    translateY(0), opacity 1 (visible)
          ↓
5000ms:   Hold position
          ↓
5300ms:   translateY(+100px), opacity 0 (slide out)
          ↓
5600ms:   Remove from DOM
```

## Responsive Breakpoints

### Desktop (>768px)
```
Task Card:
┌────────────────────────────────────────┐
│ Title                                  │
│ 👤 Agent  🏷️ [HIGH▼]  🕐 Timestamp   │
└────────────────────────────────────────┘
```

### Mobile (<768px)
```
Task Card:
┌──────────────────────┐
│ Title                │
│ 👤 Agent             │
│ 🏷️ [HIGH▼]          │
│ 🕐 Timestamp         │
└──────────────────────┘
```

Toast (Mobile):
```
Full width minus 1rem margins on left and right
```

## Accessibility Features

1. **Keyboard Navigation:**
   - Tab to dropdown
   - Arrow keys to select
   - Enter to confirm

2. **Screen Readers:**
   - Dropdown has implicit label from card context
   - Badge has title attribute (tooltip text)
   - Loading state announced by spinner emoji

3. **Color Contrast:**
   - All text meets WCAG AA standards
   - Badge borders provide additional distinction beyond color

4. **Focus Indicators:**
   - Blue glow (2px shadow) on dropdown focus
   - Visible in dark and light themes
