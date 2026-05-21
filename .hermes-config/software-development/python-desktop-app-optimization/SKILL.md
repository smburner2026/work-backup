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

## Pitfalls to avoid
- Do not rewrite the entire UI layer unless requested — focus on the filter application and event loop.
- Keep the original `redshift.spec` and `build_release.py` untouched when possible.
- Unsigned PyInstaller builds will always trigger SmartScreen on first run; document the "More info → Run anyway" path.
- Never claim the app requires admin rights (it does not).

## References
- `references/redshift-optimization-notes.md` — concrete changes from the 2026-05 RedShift session (gamma caching, macOS reconfiguration callback, Windows safety timer reduction).
- `references/pyinstaller-desktop-patterns.md` — reusable patterns for tray apps using pystray + ctypes.

## Building the executable
After editing the main script:
```bash
python build_release.py
```
Copy the entire `dist/RedShift/` folder to `C:\Program Files\RedShift` (or `%LocalAppData%\RedShift`) and create a desktop shortcut to `RedShift.exe`.

## Safety note
The resulting executable only manipulates display gamma ramps and writes a small settings JSON. It is safe for personal use.