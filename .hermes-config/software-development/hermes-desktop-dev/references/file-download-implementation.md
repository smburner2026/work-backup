# File Download Implementation (2026-06-04)

## What Was Added

Two new IPC handlers for downloading files from VPS to local machine:

### `saveFileFromUrl(url)`
- Downloads from any URL (http/https/data/file)
- Shows native save dialog
- Returns `{ saved: boolean, path?: string }`

### `saveFileFromPath(filePath)`
- Reads file directly from VPS filesystem
- Shows native save dialog
- Returns `{ saved: boolean, path?: string }`

## Files Modified

### electron/main.cjs
Added two functions near `saveImageFromUrl`:
```javascript
async function saveFileFromUrl(rawUrl) {
  const { buffer, mimeType } = await resourceBufferFromUrl(rawUrl)
  const fallbackName = filenameFromUrl(rawUrl, 'download')
  const result = await dialog.showSaveDialog(mainWindow, {
    title: 'Save File',
    defaultPath: fallbackName
  })
  if (result.canceled || !result.filePath) return { saved: false }
  await fs.promises.writeFile(result.filePath, buffer)
  return { saved: true, path: result.filePath }
}

async function saveFileFromPath(filePath) {
  const buffer = await fs.promises.readFile(filePath)
  const fallbackName = path.basename(filePath) || 'download'
  const result = await dialog.showSaveDialog(mainWindow, {
    title: 'Save File',
    defaultPath: fallbackName
  })
  if (result.canceled || !result.filePath) return { saved: false }
  await fs.promises.writeFile(result.filePath, buffer)
  return { saved: true, path: result.filePath }
}
```

Added IPC handlers near existing ones:
```javascript
ipcMain.handle('hermes:saveFileFromUrl', (_event, url) => saveFileFromUrl(String(url || '')))
ipcMain.handle('hermes:saveFileFromPath', (_event, filePath) => saveFileFromPath(String(filePath || '')))
```

### electron/preload.cjs
Added to contextBridge.exposeInMainWorld:
```javascript
saveFileFromUrl: url => ipcRenderer.invoke('hermes:saveFileFromUrl', url),
saveFileFromPath: filePath => ipcRenderer.invoke('hermes:saveFileFromPath', filePath),
```

### src/global.d.ts
Added TypeScript declarations:
```typescript
saveFileFromUrl: (url: string) => Promise<{ saved: boolean; path?: string }>
saveFileFromPath: (filePath: string) => Promise<{ saved: boolean; path?: string }>
```

## Usage from Renderer

```typescript
// Download from VPS path (most common)
const result = await window.hermesDesktop.saveFileFromPath('/root/work/file.txt')
if (result.saved) {
  notify({ kind: 'success', title: 'File saved', message: result.path })
}

// Download from URL
const result = await window.hermesDesktop.saveFileFromUrl('http://localhost:9119/api/...')
```

## Key Pattern
- Uses existing `resourceBufferFromUrl` helper for URL downloads
- Uses existing `filenameFromUrl` helper for default filenames
- Uses existing `dialog.showSaveDialog` for native save dialog
- Returns consistent `{ saved, path }` shape for both handlers
