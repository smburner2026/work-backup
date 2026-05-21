# RedShift 2026-05 Optimization Session

## Changes applied
- Added `(intensity, brightness_map)` state cache in `apply_filter` with early return.
- Introduced `_get_cached_ramps()` that precomputes and stores 256-entry gamma tables keyed by `(intensity, sorted brightness tuple)`.
- Replaced aggressive 2 s / 5 s re-apply timers with native display reconfiguration callbacks (macOS) and safety-net timers only (5 s Windows).
- Cached PIL tray icons in module-level dict.
- Debounced settings writes at 300 ms.
- Moved ctypes struct definitions and argtypes to module scope.
- Version bumped to 1.1.0.

## Result
- Near-zero scheduled wake-ups on idle.
- No redundant `SetDeviceGammaRamp` / `CGSetDisplayTransferByTable` calls.
- Same user experience, lower resource use.

## Build notes
After replacing `redshift.py`, run `python build_release.py`. The `.spec` file requires no modification. Copy entire `dist/RedShift/` folder to a Windows location (`C:\Program Files\RedShift` recommended) and create desktop shortcut. First run triggers SmartScreen — user must choose "Run anyway".