# Hermes Desktop App — Architecture Reference

## Overview

The Hermes Desktop app is an Electron + React application that connects to a Hermes backend (dashboard on port 9119). It provides a GUI for chat, file browsing, settings, and management.

## Key Architecture Patterns

### Lazy-loaded Views
All major views are lazy-loaded React components in `apps/desktop/src/app/`:
- `chat/` — Main chat interface
- `skills/` — Skills & tools management
- `messaging/` — Platform configuration
- `artifacts/` — Generated artifacts
- `cron/` — Scheduled jobs
- `profiles/` — Profile management
- `agents/` — Multi-agent orchestration
- `settings/` — Configuration
- `command-center/` — Unified management panel

### Route System
Routes defined in `apps/desktop/src/app/routes.ts`:
- Each view has a route constant (e.g., `SKILLS_ROUTE = '/skills'`)
- `AppView` type union lists all views
- `APP_ROUTES` array maps paths to views
- `appViewForPath()` resolves current view from URL

### Sidebar Navigation
Nav items defined in `apps/desktop/src/app/chat/sidebar/index.tsx`:
- `SIDEBAR_NAV` array defines visible items
- Each item has: id, label, icon, route
- Active view detection checks `currentView` against item id

### API Layer
- `apps/desktop/src/hermes.ts` — API functions
- Uses `window.hermesDesktop.api()` for HTTP calls
- Goes through gateway backend (port 9119)
- Auth: session token injected via `window.__HERMES_SESSION_TOKEN__`

### Electron IPC
- `electron/preload.cjs` — IPC bridge definitions
- `electron/main.cjs` — Main process handlers
- Key handlers: readFileDataUrl, readFileText, saveImageFromUrl, saveImageBuffer

## Adding a New View

1. Add route constant to `routes.ts`
2. Add `'newview'` to `AppView` and `AppRouteId` types
3. Add route to `APP_ROUTES`
4. Create `app/newview/index.tsx` with `NewView` component
5. Add lazy import in `desktop-controller.tsx`
6. Add nav item to `SIDEBAR_NAV` in `chat/sidebar/index.tsx`
7. Add active view check in sidebar

## File Operations (Current State)

| Operation | Handler | Works |
|-----------|---------|-------|
| Read file as data URL | `readFileDataUrl` | ✓ |
| Read file as text | `readFileText` | ✓ |
| Save image from URL | `saveImageFromUrl` | ✓ |
| Save image buffer | `saveImageBuffer` | ✓ |
| Save generic file | — | ✗ Not implemented |

## Kanban Plugin (Web Dashboard Only)

The kanban board UI exists only in the web dashboard plugin:
- Backend: `plugins/kanban/dashboard/plugin_api.py`
- Frontend: `plugins/kanban/dashboard/dist/index.js` (IIFE bundle)
- Uses `window.__HERMES_PLUGIN_SDK__` for React + components
- Calls `/api/plugins/kanban/` endpoints

### Kanban API Endpoints (all under /api/plugins/kanban/)
- `GET /board` — Full board grouped by columns
- `GET /tasks/{id}` — Task detail
- `POST /tasks` — Create task
- `PATCH /tasks/{id}` — Update/move task
- `DELETE /tasks/{id}` — Delete task
- `POST /tasks/{id}/comments` — Add comment
- `POST /tasks/{id}/attachments` — Upload attachment
- `WS /events` — Live task event stream

### Board Columns
triage → todo → scheduled → ready → running → blocked → review → done

## Connection Architecture

```
Desktop App  ──HTTP──▶  Dashboard (port 9119)  ──▶  Hermes Agent
                         (hermes dashboard --tui)
```

The official desktop app connects to the dashboard, NOT the API server (port 8642). The API server is for third-party integrations.
