---
name: python-desktop-app-optimization
description: Review, optimize, and package Python desktop/tray applications (gamma manipulation, polling reduction, PyInstaller builds). Encodes caching patterns, event-driven display callbacks, and safe Windows deployment for system-level display tools.
category: software-development
tags: [python, desktop, pyinstaller, gamma, tray-app, optimization, packaging]
trigger: User provides a Python desktop/tray application (especially one using ctypes, gamma ramps, or system display APIs) and asks to review it for performance, reduce polling, improve caching, or produce a distributable Windows .exe.
---

# Python Desktop App Optimization & Packaging

## When to use
- User shares a GitHub repo or local Python script for a system-tray / menu-bar desktop tool.
- Request involves making the app "faster", "less CPU", "event-driven instead of timers", "better caching", or "build a working .exe".
- Common in blue-light filters, color temperature tools, overlay utilities, and low-level Windows/macOS display manipulation apps.

## Core workflow
1. Fetch the main source (raw GitHub or local file).
2. Identify polling timers, repeated API calls, and mutable state.
3. Introduce state caching + early exit in hot paths (`apply_filter`, gamma application).
4. Replace periodic timers with native reconfiguration callbacks where possible (CGDisplayRegisterReconfigurationCallback on macOS, device notifications on Windows).
5. Precompute and cache gamma ramps / color matrices.
6. Debounce settings writes and icon generation.
7. Ensure the PyInstaller .spec still points at the main script; rebuild after edits.
8. Guide user on safe Windows installation locations and SmartScreen handling.

## Key optimizations this skill encodes
- Cache last-applied `(intensity, per-display brightness)` tuple before any ctypes call.
- Module-level ramp cache keyed by `(intensity, brightness_tuple)`.
- Safety-net timers only (5–10 s) instead of aggressive 2 s re-application.
- Cached PIL tray icons.
- Debounced JSON persistence (300 ms).

## Smooth color transition animations
Replace instantaneous `set_intensity` jumps with eased stepping for a f.lux-like feel:
- Add `_animate_intensity(self, from_value, to_value, duration_ms)` method.
- Use `root.after(ANIMATION_FRAME_MS, step)` (~30 fps) with an `ease_in_out(t) = t*t*(3-2*t)` smoothstep.
- Typical durations: 1500 ms startup ramp, 800 ms slider change, 500 ms off/on fade.
- Store `_target_intensity` that can be updated mid-animation (if user moves slider again) — the running step loop picks it up rather than restarting.
- During animation, set `_animating = True` so reapply timers skip gamma calls (prevents flicker).
- Apply the gamma ramp on every step frame via the existing `apply_filter(current, persist=False, update_ui=False)`.
- Use `threading.Timer` as fallback on macOS (no `root.after` in menu-bar mode).

## Windows auto-start via registry
Add a "Launch at startup" checkbox using ctypes + advapi32:
```python
import ctypes
AUTO_START_REG_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"

def enable_startup() -> bool:
    advapi32 = ctypes.windll.advapi32
    hkey = ctypes.c_void_p()
    res = advapi32.RegOpenKeyExW(0x80000001, AUTO_START_REG_KEY, 0, 0x00020006, ctypes.byref(hkey))
    if res != 0: return False
    exe_path = os.path.abspath(sys.argv[0])
    res = advapi32.RegSetValueExW(hkey, APP_NAME, 0, 1, exe_path, len(exe_path) * 2)
    advapi32.RegCloseKey(hkey)
    return res == 0

def disable_startup() -> bool:
    # RegOpenKeyExW + RegDeleteValueW
    ...

def is_startup_enabled() -> bool:
    # RegOpenKeyExW + RegQueryValueExW + check file exists
    ...
```
Wire to a `ttk.Checkbutton` with a `BooleanVar` in the window footer; on toggle call enable/disable. Add `--install-startup` / `--uninstall-startup` CLI flags for headless install.

## Pitfalls to avoid
- Do not rewrite the entire UI layer unless requested — focus on the filter application and event loop.
- Keep the original `redshift.spec` and `build_release.py` untouched when possible.
- Unsigned PyInstaller builds will always trigger SmartScreen on first run; document the "More info → Run anyway" path.
- Never claim the app requires admin rights (it does not).
- **PyInstaller cross-compilation**: A Linux PyInstaller build produces a Linux ELF binary, NOT a Windows .exe. To build the Windows exe, copy the source tree to the Windows side (`/mnt/c/Users/...`) and run `python build_release.py` there in PowerShell or CMD. The source, asset icons, .spec, and build script all need to be on Windows.
- **Animation thread safety**: Never call `root.after()` from a non-main thread. Use the existing `_ui_queue` (SimpleQueue + periodic drain) pattern, or schedule via `_call_on_ui()`. The step function itself runs on the main thread since `root.after` fires there.
- **Python 3.12+ ctypes callback strictness**: Python 3.12 enforces that Win32 API callbacks match their declared WINFUNCTYPE signature exactly. Passing a plain nested function raises `ctypes.ArgumentError: argument N: TypeError: expected WinFunctionType instance instead of function`. Fix: wrap the callback with its declared type at the call site:
  ```python
  MONITORENUMPROC = self.MONITORENUMPROC
  self.user32.EnumDisplayMonitors(None, None, MONITORENUMPROC(enum_monitor_proc), None)
  ```
  This is a breaking change from 3.11 — code that worked fine on 3.11 crashes on 3.12+. Applies to any Win32 ctypes callback: `EnumDisplayMonitors`, `SetWinEventHook`, `EnumWindows`, `EnumChildWindows`, etc. Audit all WINFUNCTYPE definitions before shipping a 3.12+ build.
- **Microsoft Store Python**: pip is NOT on PATH as a standalone command — use `python -m pip` instead. Store Python works fine for PyInstaller builds since the .exe bundles its own runtime.

## References
- `references/redshift-optimization-notes.md` — concrete changes from the 2026-05 RedShift session (gamma caching, macOS reconfiguration callback, Windows safety timer reduction).
- `references/redshift-smooth-animation.md` — smooth eased transitions via `root.after()`, Windows auto-start via ctypes+advapi32, cross-compilation pitfall.
- `references/pyinstaller-desktop-patterns.md` — reusable patterns for tray apps using pystray + ctypes.
- `references/python312-ctypes-callback.md` — Python 3.12+ ctypes callback strictness when passing functions to Win32 APIs; error signature, fix pattern, and affected APIs.

## Building the executable
After editing the main script:
```bash
# On the build machine:
python build_release.py
```

**CRITICAL: Platform constraint** — PyInstaller is NOT a cross-compiler. A Linux PyInstaller run produces a Linux ELF binary, not a Windows .exe. Always build on the target platform:
- Windows .exe → build on Windows (PowerShell or CMD)
- macOS .app → build on macOS

If you're working from WSL/Linux, copy the entire source tree to the Windows side:
```bash
cp -r /path/to/RedShift-source /mnt/c/Users/<name>/Desktop/RedShift-build/
```
Then open PowerShell on Windows and run:
```powershell
cd C:\Users\<name>\Desktop\RedShift-build
pip install -r requirements.txt -r requirements-build.txt
python build_release.py
```

Copy the entire `dist/RedShift/` folder to `C:\\Program Files\\RedShift` (or `%LocalAppData%\\RedShift`) and create a desktop shortcut to `RedShift.exe`.

## Safety note
The resulting executable only manipulates display gamma ramps and writes a small settings JSON. It is safe for personal use.