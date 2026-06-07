# Python 3.12+ ctypes Win32 Callback Compatibility

## Symptom

PyInstaller-built .exe crashes on launch with:

```
ERROR RedShift failed to start
Traceback (most recent call last):
  File "redshift.py", line 1556, in <module>
  ...
  File "redshift.py", line 1109, in _get_windows_display_names
ctypes.ArgumentError: argument 3: TypeError: expected WinFunctionType instance instead of function
```

No window, no tray icon — just a log line and exit. The old v1.0.0 (.exe built with Python 3.11) works fine.

## Root cause

Python 3.12+ tightens ctypes type validation. When calling a Win32 API that accepts a callback pointer (e.g. `EnumDisplayMonitors`), the declared `argtypes` for that API includes a `WINFUNCTYPE`. Previously (3.11 and earlier), passing a plain Python function with matching parameter types worked silently. Python 3.12+ requires the callback to be explicitly wrapped with its declared `WINFUNCTYPE` at the call site.

## Fix

```python
# Before (works on 3.11, crashes on 3.12+):
if not self.user32.EnumDisplayMonitors(None, None, enum_monitor_proc, None):

# After (works on both):
MONITORENUMPROC = self.MONITORENUMPROC
if not self.user32.EnumDisplayMonitors(None, None, MONITORENUMPROC(enum_monitor_proc), None):
```

The key: `MONITORENUMPROC(enum_monitor_proc)` wraps the plain function with the `WINFUNCTYPE` that was declared for the API's argtypes.

## APIs known to be affected

Any Win32 API that takes a callback via ctypes:
- `EnumDisplayMonitors` (MONITORENUMPROC)
- `SetWinEventHook` (WINEVENTPROC)
- `EnumWindows` (WNDENUMPROC)
- `EnumChildWindows` (WNDENUMPROC)
- `EnumPrinters` (PRINTER_ENUM_PROC)
- Any other `Enum*` or callback-taking API

## Detection

After building a PyInstaller .exe with Python 3.12+, launch it from a terminal (not double-click) to see the crash output:
```powershell
.\dist\RedShift\RedShift.exe
```
If it exits silently, check the app's log file (`~/.redshift/redshift.log`) for `ERROR` lines and backtraces.

Alternatively, run the source Python script directly on the build machine to catch ctypes errors before building.

## Environment

- Python 3.12.10 (Microsoft Store)
- PyInstaller 6.20.0
- Windows 11 (build 26200)
- App: RedShift (blue-light filter, ctypes gamma ramp manipulation via user32 + gdi32)

## Build context

The build used Microsoft Store Python (`C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_...`). The .exe bundles its own Python runtime, so even if the build Python is Store-based, the resulting .exe is standalone.
