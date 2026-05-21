# PyInstaller Desktop Tray App Patterns

Common patterns observed across multiple Python desktop tools using pystray + ctypes:

## Gamma / color effect apps
- Always cache the last applied color matrix or ramp set.
- Use safety-net timers (5–10 s) rather than continuous polling.
- On Windows prefer a single method (either Magnification or GDI gamma) to avoid state-flip artifacts.
- macOS: register `CGDisplayRegisterReconfigurationCallback` for attach/detach/sleep events.

## Packaging
- Keep `pyinstaller` spec pointing at the main script only.
- Exclude numpy, pandas, matplotlib, scipy by default (they bloat the bundle).
- For tray-only apps set `console=False` and use `LSUIElement=True` on macOS.
- Unsigned builds always require "More info → Run anyway" on first Windows launch.

## Safe installation locations (Windows)
- `C:\Program Files\<App>` (requires admin to write, cleanest)
- `%LocalAppData%\<App>` (no admin, user-writable)
- Desktop folder (quick testing only)

Never install directly into `C:\` root or user profile root.