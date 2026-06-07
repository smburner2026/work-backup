---
name: hermes-desktop-dev
description: "Develop, extend, and debug the Hermes Desktop app (Electron). Covers architecture, IPC handlers, new views/panels, file download, and gateway integration."
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [electron, desktop, hermes, ipc, react, development]
---

# Hermes Desktop App Development

The Hermes Desktop app is an Electron application that provides a native GUI for the Hermes agent. It connects to the Hermes gateway backend (same process as `hermes dashboard`) and reuses the agent core — same config, same sessions, same tools.

**Design priority:** The primary value of the desktop app is **file access from VPS** — browsing, previewing, and downloading files. Any feature work should prioritize this capability first.

## Architecture

```
apps/desktop/
├── electron/           # Electron main process (compiled .cjs)
│   ├── main.cjs        # Main process: IPC handlers, window management
│   ├── preload.cjs     # Preload: bridges main↔renderer via contextBridge
│   └── *.cjs           # Other main-process modules
├── src/                # React renderer (TypeScript)
│   ├── app/            # Views (lazy-loaded)
│   ├── components/     # Shared UI components
│   ├── hermes.ts       # API client (calls gateway via IPC)
│   ├── global.d.ts     # TypeScript declarations for window.hermesDesktop
│   └── store/          # State management
└── package.json
```

### IPC Communication Pattern

```
Renderer (React) → window.hermesDesktop.method() → preload.cjs → ipcRenderer.invoke() → main.cjs handler
```

All communication goes through three layers:
1. **preload.cjs** — exposes `window.hermesDesktop` methods via `contextBridge.exposeInMainWorld`
2. **main.cjs** — registers handlers via `ipcMain.handle('hermes:channelName', handler)`
3. **global.d.ts** — TypeScript declarations for the exposed methods

## Adding a New IPC Handler

When the renderer needs to call a main-process function (file system, native dialogs, etc.):

### 1. Add handler function in main.cjs

```javascript
// Near other handler functions (e.g., saveImageFromUrl)
async function myNewHandler(param) {
  // Do work...
  return { success: true, data: result }
}
```

### 2. Register IPC handler in main.cjs

```javascript
// Near other ipcMain.handle registrations
ipcMain.handle('hermes:myNewHandler', (_event, param) => myNewHandler(param))
```

### 3. Expose in preload.cjs

```javascript
// Add to the contextBridge.exposeInMainWorld object
myNewHandler: param => ipcRenderer.invoke('hermes:myNewHandler', param),
```

### 4. Add TypeScript declaration in global.d.ts

```typescript
// Inside the window.hermesDesktop interface
myNewHandler: (param: string) => Promise<{ success: boolean; data?: unknown }>
```

### Existing IPC Handlers (reference)

| Handler | Purpose |
|---------|---------|
| `readFileDataUrl(filePath)` | Read file as base64 data URL |
| `readFileText(filePath)` | Read file as text |
| `saveImageFromUrl(url)` | Save image from URL via native dialog |
| `saveFileFromUrl(url)` | Save any file from URL via native dialog |
| `saveFileFromPath(filePath)` | Save file from VPS path via native dialog |
| `saveImageBuffer(data, ext)` | Save image buffer to local disk |
| `selectPaths(options)` | Native file/folder picker dialog |
| `readDir(path)` | List directory contents |
| `api(request)` | Call gateway REST API |

## Adding a New View/Panel

When adding a new tab or section to the desktop app:

### 1. Create the view component

```
src/app/my-feature/index.tsx
```

Use `PageSearchShell` for consistent layout with search/filter bar.

Follow the pattern from existing views (SkillsView, CronView):
- Export a named component (e.g., `MyFeatureView`)
- Accept `setStatusbarItemGroup` prop
- Use `@/hermes` API functions for data fetching
- Use `notify`/`notifyError` for user feedback

### 2. Add route in routes.ts

```typescript
export const MY_FEATURE_ROUTE = '/my-feature'

// Add to AppView type
export type AppView = 'my-feature' | ...

// Add to AppRouteId type
export type AppRouteId = 'my-feature' | ...

// Add to APP_ROUTES array
{ id: 'my-feature', path: MY_FEATURE_ROUTE, view: 'my-feature' }
```

### 3. Add lazy import in desktop-controller.tsx

```typescript
const MyFeatureView = lazy(async () => ({ default: (await import('./my-feature')).MyFeatureView }))
```

### 4. Add to sidebar navigation in chat/sidebar/index.tsx

```typescript
// Add to SIDEBAR_NAV array
{ id: 'my-feature', label: 'My Feature', icon: props => <Codicon name="icon-name" {...props} />, route: MY_FEATURE_ROUTE }
```

### 5. Add active view check in sidebar

```typescript
// In the active view logic
(item.id === 'my-feature' && currentView === 'my-feature')
```

## Gateway API Communication

The desktop app calls the gateway backend via `window.hermesDesktop.api()`:

```typescript
import { apiCall } from '@/hermes'

// GET request
const data = await apiCall<MyType>('/api/endpoint')

// POST request
const result = await apiCall<ResultType>('/api/endpoint', { method: 'POST', body: payload })
```

The gateway URL and session token are managed by the Electron main process and injected into the renderer.

### Auth Architecture (two modes)

The gateway supports two auth modes, detected via `GET /api/status` → `auth_required` field:

| Mode | REST auth | WS auth | Token lifecycle |
|------|-----------|---------|-----------------|
| **Token** (legacy) | `X-Hermes-Session-Token` header | `?token=` query param | **Ephemeral** — regenerated on every gateway process start. Desktop mints via `HERMES_DASHBOARD_SESSION_TOKEN` env var; if unset, gateway generates random `secrets.token_urlsafe(32)`. Dies when process exits. |
| **OAuth** | HttpOnly session cookie (`__Host-hermes_session_at` / `__Secure-hermes_session_at` / `hermes_session_at`) | Single-use `?ticket=` from `POST /api/auth/ws-ticket` | Cookie-based, auto-refreshes. More resilient to restarts. |

**Connection flow** (`connection-config.cjs`):
1. Desktop fetches `GET /api/status` to determine `auth_required` → classifies mode as `'oauth'` or `'token'`
2. Token mode: uses stored token in `X-Hermes-Session-Token` header for REST, `?token=` for WS
3. OAuth mode: uses session cookie for REST, mints a fresh ticket at `/api/auth/ws-ticket` for each WS upgrade

**Critical: desktop app update → gateway restart → connection failure.** When the desktop app updates, it may restart the gateway process. The gateway regenerates the session token on restart. If the desktop app is in token mode and doesn't re-discover the new token, all API calls return 401. Fix: reconnect from desktop settings, or `hermes gateway restart` on VPS + re-enter gateway URL in desktop.

See `references/desktop-auth-lifecycle.md` for the full auth flow and troubleshooting.

## File Download Pattern

The desktop app's core value is file access. Two patterns:

### From VPS path (most common)
```typescript
const result = await window.hermesDesktop.saveFileFromPath('/root/work/file.txt')
if (result.saved) {
  notify({ kind: 'success', title: 'File saved', message: result.path })
}
```

### From URL
```typescript
const result = await window.hermesDesktop.saveFileFromUrl('http://localhost:9119/api/...')
```

Both show a native save dialog and return `{ saved: boolean, path?: string }`.

## VPS Deployment & Connection

The desktop app connects to the **dashboard web server** (port 9119), NOT the gateway's API server (port 8642). Session tokens are ephemeral — regenerated on every dashboard restart. For remote VPS connections via Tailscale, the dashboard needs `--host 0.0.0.0 --insecure`. Full details: `references/desktop-connection-deployment.md`.

## Local LLM Configuration

The desktop app works with local LLMs — no VPS required. The app connects to the Hermes gateway, which connects to whatever provider is configured.

### llama.cpp Setup

1. Start llama.cpp server with OpenAI-compatible endpoint:
   ```bash
   ./server -m /path/to/model.gguf --port 8080 --ctx-size 65536
   ```
2. Configure Hermes (either via Desktop Settings → Models → Add Custom Endpoint, or edit `~/.hermes/config.yaml`):
   ```yaml
   model:
     default: your-model-name
     provider: custom
     base_url: http://localhost:8080/v1
     context_length: 64000
   ```
3. No `api_key` needed for local servers — omit or leave blank.

### Ollama Setup

```bash
ollama pull qwen2.5-coder:32b
OLLAMA_CONTEXT_LENGTH=64000 ollama serve
```

### Critical: Context Length

Hermes uses long system prompts with tool schemas. **Minimum context: 64,000 tokens.** Below this, expect truncation errors. Set both the server-side `--ctx-size` and the config-side `context_length` to ≥64k.

### Supported Local Providers

Any OpenAI-compatible `/v1/chat/completions` endpoint works: llama.cpp, vLLM, Ollama, LM Studio. The `provider: custom` + `base_url` pattern covers all of them.

## Current Feature Gaps

As of 2026-06-04:
- **Kanban board** — not yet in desktop app (only in web dashboard plugin). See `references/kanban-integration-research.md` for integration plan.
- **Generic file download** — now implemented (saveFileFromUrl/saveFileFromPath). See `references/file-download-implementation.md` for implementation details.
- **File browser download button** — not yet wired up in the preview component

## Pitfalls

- **Never relay session tokens or credentials in chat.** When the user asks for the gateway URL + session token (e.g. to reconnect the desktop app), write them to a temp file with `chmod 600` and instruct the user to SSH-read + delete. Pattern: `cat > /tmp/vps-gateway-creds.txt << EOF ... EOF && chmod 600 /tmp/vps-gateway-creds.txt` then tell user: `ssh root@<ip> "cat /tmp/vps-gateway-creds.txt && rm /tmp/vps-gateway-creds.txt"`. This applies to any credential-bearing response — Telegram, Discord, Slack, etc.
- **CJS files** — main.cjs and preload.cjs are compiled JavaScript, not TypeScript. Edit carefully; no type checking.
- **Preload registration** — forgetting to expose a new handler in preload.cjs means the renderer can't call it (silent failure).
- **TypeScript declarations** — global.d.ts must match the actual preload.cjs exports. Mismatches cause runtime errors.
- **IPC channel naming** — use `hermes:actionName` convention consistently.
- **Dialog requires mainWindow** — native dialogs need the BrowserWindow reference. Use the existing `mainWindow` variable.