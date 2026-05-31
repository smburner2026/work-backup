# Windows Terminal Font Troubleshooting

## The Silent Fallback Problem

When you set a `font.face` in Windows Terminal settings.json (or the UI) that doesn't exist on the system, Windows Terminal **silently reverts** to a safe fallback font — typically **Consolas**. It gives no error, no warning, no log message. You won't know unless you check settings.json afterwards.

### How to verify

```bash
# From WSL — check the settings.json
grep -A2 'font' /mnt/c/Users/vthen/AppData/Local/Packages/Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/settings.json
```

If `font.face` shows a different value than what you set, the font isn't installed.

### Check if a font is actually installed

```bash
# From WSL — check Windows Fonts directory
ls "/mnt/c/Windows/Fonts/Cascadia"*   # Cascadia Code
ls "/mnt/c/Windows/Fonts/JetBrains"*  # JetBrains Mono
ls "/mnt/c/Windows/Fonts/Iosevka"*    # Iosevka
```

### Fix

**Option A: Install the missing font**

- **Cascadia Code:** `winget install Microsoft.CascadiaCode` (from PowerShell), or download from [GitHub releases](https://github.com/microsoft/cascadia-code/releases)
- **JetBrains Mono:** `winget install JetBrains.Mono` or download from [jetbrains.com](https://www.jetbrains.com/lp/mono/)
- **Iosevka:** Download from [GitHub releases](https://github.com/be5invis/Iosevka/releases)

After installing, Windows Terminal picks it up on next launch — no settings.json change needed if the font name is already set.

**Option B: Use a font that's already installed**

Fonts available on any Windows 10/11 system:

| Font | Monospace | Good for |
|---|---|---|
| Consolas | ✅ Yes | Terminal, coding — default, reliable |
| Courier New | ✅ Yes | Classic, wider characters |
| Lucida Console | ✅ Yes | Readable at small sizes |

Consolas at 15pt is surprisingly good — already the most common terminal font for a reason.

### Common patterns that trigger this

1. **Setting a font name that doesn't match exactly** — Windows font names are exact strings. "Cascadia Code" not "Cascadia" or "CascadiaCode". Check `ls /mnt/c/Windows/Fonts/` for exact filenames.
2. **Setting a font that was installed for one user but not the system** — Some font installers only copy to `%USERPROFILE%\AppData\Local\Microsoft\Windows\Fonts\` (per-user), not `C:\Windows\Fonts\`. WSL's `/mnt/c/Windows/Fonts/` only sees system-wide fonts. Check the per-user path: `/mnt/c/Users/vthen/AppData/Local/Microsoft/Windows/Fonts/`.
3. **Windows Terminal auto-update can reset settings** — Major Windows Terminal updates (e.g. 1.15 → 1.16) can rewrite settings.json. This is rare but known. The `font` and `useAtlasEngine` settings usually survive.

### What sticks regardless of font

- `font.size` — works even when font.face falls back. Size 15+ makes a visible difference.
- `useAtlasEngine: true` — GPU-accelerated renderer, independent of font choice. Makes text noticeably smoother.

### General approach

When Windows Terminal settings don't take effect:

1. Check settings.json is actually written: `grep 'font\|useAtlasEngine' <settings.json>`
2. Verify font exists on Windows: `ls /mnt/c/Windows/Fonts/<font-glob>`
3. Test with a known-good font (Consolas) to isolate whether it's the font or a different setting
4. Restart Windows Terminal completely (Ctrl+Shift+W to close, reopen from Start menu)
