# Kanban Integration Research (2026-06-04)

## Status
Feasibility confirmed, implementation not started.

## Current State

### Desktop App Views
- Chat (default)
- Skills & Tools (`/skills`)
- Messaging (`/messaging`)
- Artifacts (`/artifacts`)
- Cron, Profiles, Agents — via command center only

### Kanban Plugin (web dashboard only)
- Backend: `plugins/kanban/dashboard/plugin_api.py`
- Frontend: `plugins/kanban/dashboard/dist/index.js` (IIFE bundle)
- Uses `window.__HERMES_PLUGIN_SDK__` for React + shadcn primitives

## Kanban API Endpoints

All under `/api/plugins/kanban/`:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/board` | Full board grouped by columns |
| GET | `/tasks/{id}` | Task detail |
| POST | `/tasks` | Create task |
| PATCH | `/tasks/{id}` | Update/move task |
| DELETE | `/tasks/{id}` | Delete task |
| POST | `/tasks/{id}/comments` | Add comment |
| POST | `/tasks/{id}/attachments` | Upload attachment |
| GET | `/tasks/{id}/attachments` | List attachments |
| GET | `/attachments/{id}` | Download attachment |
| DELETE | `/attachments/{id}` | Remove attachment |
| GET | `/diagnostics` | Task diagnostics |
| WS | `/events` | Live task event stream |

Board columns: triage → todo → scheduled → ready → running → blocked → review → done

## Integration Approach

1. Add `KANBAN_ROUTE` to routes.ts
2. Add `'kanban'` to AppView and AppRouteId types
3. Add kanban route to APP_ROUTES
4. Create `apps/desktop/src/app/kanban/index.tsx` (KanbanView component)
5. Add kanban API functions to `hermes.ts` (calling `/api/plugins/kanban/`)
6. Add kanban types to `types/hermes.ts`
7. Add lazy import in `desktop-controller.tsx`
8. Add kanban to sidebar nav in `chat/sidebar/index.tsx`

## Files to Modify
- `apps/desktop/src/app/routes.ts`
- `apps/desktop/src/app/desktop-controller.tsx`
- `apps/desktop/src/app/chat/sidebar/index.tsx`
- `apps/desktop/src/hermes.ts`
- `apps/desktop/src/types/hermes.ts`

## New Files
- `apps/desktop/src/app/kanban/index.tsx`

## Estimate
~600-800 lines of new code. No blockers identified.
