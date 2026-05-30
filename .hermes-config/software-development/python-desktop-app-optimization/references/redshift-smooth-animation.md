# RedShift v1.1.0 — Smooth Animation + Auto-Start

## Changes from v1.0.0
- **Smooth eased transitions** — replaced instantaneous `set_intensity` jumps with animated stepping via `root.after()` at ~30 fps using smoothstep easing.
- **Windows auto-start** — added registry Run key integration via `advapi32` ctypes, with "Launch at startup" checkbox in the window.
- Version bumped to 1.1.0, window height increased from 310→340 to fit the checkbox.

## Animation implementation

### Core mechanism
```python
ANIMATION_FRAME_MS = 33          # ~30 fps
ANIMATION_STARTUP_MS = 1500      # startup ramp
ANIMATION_TRANSITION_MS = 800    # slider change
ANIMATION_TURN_OFF_MS = 500      # off/on fade

def ease_in_out(t: float) -> float:
    return t * t * (3.0 - 2.0 * t)  # smoothstep
```

### State tracking
- `self._animating: bool` — true while a step loop is in progress
- `self._target_intensity: int` — updated by `set_intensity()` during animation; the running loop reads this on each frame rather than restarting

### Step loop
```python
def _animate_intensity(self, from_value, to_value, duration_ms):
    self._animating = True
    start_time = None
    def step():
        elapsed = now - start_time
        target = self._target_intensity  # may have moved
        if elapsed >= duration_ms:
            self.intensity = target
            self.apply_filter(target, persist=True, update_ui=True)
            self._animating = False
            return
        progress = ease_in_out(clamp(elapsed / duration_ms, 0.0, 1.0))
        current = int(round(lerp(float(from_value), float(target), progress)))
        if current != self.intensity:
            self.intensity = current
            self.apply_filter(current, persist=False, update_ui=False)
            self._update_window_ui()
            self._update_tray_ui()
        self.root.after(ANIMATION_FRAME_MS, step)
    step()
```

### Reapply guard
During animation, `_reapply_windows_filter` and the macOS timer both check `self._animating` and skip gamma calls. This prevents flicker from the 2 s reapply timer stepping on top of the animation.

## Auto-start implementation

### Registry path
```
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
```

### Win32 API via ctypes
```python
advapi32 = ctypes.windll.advapi32
# RegOpenKeyExW — open key
# RegSetValueExW — write value (REG_SZ = 1)
# RegQueryValueExW — read value
# RegDeleteValueW — remove value
# RegCloseKey — close handle
```

### UI integration
- `self.auto_start_var = tk.BooleanVar(value=is_startup_enabled())`
- `ttk.Checkbutton(footer, text="Launch at startup", variable=self.auto_start_var, command=self._toggle_auto_start)`
- `_toggle_auto_start()` calls `enable_startup()` or `disable_startup()`, reverts checkbox on failure

### CLI flags
- `--install-startup` — headless enable
- `--uninstall-startup` — headless disable

## Build note
Built on Windows via PyInstaller. Linux PyInstaller produces a Linux binary, not .exe. To build:
1. Copy source tree to Windows (`/mnt/c/Users/<name>/OneDrive/Desktop/RedShift-v1.1.0/`)
2. Run `python build_release.py` in PowerShell from that directory
3. Output at `dist/RedShift/RedShift.exe`
