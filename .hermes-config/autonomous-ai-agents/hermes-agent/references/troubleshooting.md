## Troubleshooting

### Voice not working
1. Check `stt.enabled: true` in config.yaml
2. Verify Python packages: `python3 -m pip list | grep -iE 'whisper|sounddevice|soundfile|edge.tts'`
3. Verify system library: `dpkg -l libportaudio2` (Linux/WSL — install with `sudo apt-get install -y libportaudio2`)
4. Check microphone detected: `python3 -c "import sounddevice as sd; print([d['name'] for d in sd.query_devices() if d['max_input_channels'] > 0])"`
5. On WSL: confirm `echo $PULSE_SERVER` shows a WSLg path; if empty, PulseAudio isn't routing audio
6. If `sounddevice` raises `OSError: PortAudio library not found` → install `libportaudio2`
7. If the hermes venv has no pip → run `python3 -m ensurepip --upgrade`
8. In gateway: `/restart`. In CLI: exit and relaunch.
9. Verify the voice tool set is enabled: `hermes tools list | grep tts`
10. **WSL2 heap corruption crash (SIGABRT / `malloc(): smallbin double linked list corrupted`)** — Hermes process aborts during voice mode on WSL2. This is caused by PortAudio negotiating variable-size buffers with PulseAudio over the WSLg Unix socket (`unix:/mnt/wslg/PulseServer`). When PulseAudio reconnects or renegotiates parameters, PortAudio can free/reallocate internal buffers while the sounddevice callback still holds stale pointers, producing a use-after-free that corrupts glibc malloc metadata.
    - Diagnose: `dmesg | grep -i "signal 6|SIGABRT|hermes"` for `python3.11: hermes: potentially unexpected fatal signal 6.` with syscall `tgkill` (0xea).
    - Fix: add `blocksize=1024` to the `sd.InputStream(...)` constructor in `tools/voice_mode.py` (`_ensure_stream()`).
    - Alternative fix: switch to a remote STT provider (Groq or OpenAI Whisper) which bypasses faster-whisper entirely but still uses local PortAudio capture.
    - Full reproduction recipe and alternative workarounds: see `references/wsl2-voice-heap-corruption.md`.
11. **Visual Studio Code WSL remote + voice**: If using VS Code Remote-WSL, the environment inherits VS Code's terminal emulation which may interfere with prompt_toolkit's push-to-talk keybinding. Try voice mode in Windows Terminal (Win32) or the standalone WSL terminal instead.
12. **WSL2 PulseAudio not routing audio on first try**: Set `PULSE_SERVER=unix:/mnt/wslg/PulseServer` explicitly in `~/.bashrc` or `~/.profile`. Restart WSL (`wsl --shutdown` from PowerShell, then reopen terminal) so PulseAudio reconnects with a fresh socket.

### Tool not available
1. `hermes tools` — check if toolset is enabled for your platform
2. Some tools need env vars (check `.env`)
3. `/reset` after enabling tools

### Model/provider issues
1. `hermes doctor` — check config and dependencies
2. `hermes login` — re-authenticate OAuth providers
3. Check `.env` has the right API key
4. **Copilot 403**: `gh auth login` tokens do NOT work for Copilot API. Use the Copilot-specific OAuth device code flow via `hermes model` → GitHub Copilot.

### Changes not taking effect
- **Tools/skills:** `/reset` starts a new session with updated toolset
- **Config changes:** In gateway: `/restart`. In CLI: exit and relaunch.
- **Code changes:** Restart the CLI or gateway process

### Skills not showing
1. `hermes skills list` — verify installed
2. `hermes skills config` — check platform enablement
3. Load explicitly: `/skill name` or `hermes -s name`

### Gateway issues
Check logs first:
```bash
grep -i "failed to send|error|InvalidToken|Unauthorized" ~/.hermes/logs/gateway.log | tail -20
journalctl --user -u hermes-gateway*.service -n 50
```

Common gateway problems:
- **Gateway dies on SSH logout**: Enable linger: `sudo loginctl enable-linger $USER`
- **Gateway dies on WSL2 close**: WSL2 requires `systemd=true` in `/etc/wsl.conf` for systemd services to work. Without it, gateway falls back to `nohup` (dies when session closes).
- **Gateway crash loop from bad platform token**: `InvalidToken`, `401 Unauthorized`, or `LoginFailure` means the stored bot token for Telegram/Discord/etc is expired or wrong. This does not just skip the platform — it can crash the gateway and trigger an auto-restart loop.
  - Diagnose: `journalctl --user -u hermes-gateway*.service -n 50 | grep -i 'InvalidToken|Unauthorized|LoginFailure'`
  - Fix option A — remove the platform entirely:
    - Set `gateway.builtin_platforms: []` to stop loading configured platforms
    - Remove any `telegram:`, `discord:`, `slack:`, etc. blocks from `~/.hermes/config.yaml` and from profile configs if you don't need that platform locally
  - Fix option B — replace the token: put a valid token in the profile's `.env` and restart both systemd services
  - Note: a missing/expired platform token will not silently fall through — the current implementation treats it as a startup failure.
- **Gateway crash loop**: Reset the failed state: `systemctl --user reset-failed hermes-gateway`

### Platform-specific issues
- **Discord bot silent**: Must enable **Message Content Intent** in Developer Portal → Bot → Privileged Gateway Intents.
- **Slack bot only works in DMs**: Must subscribe to `message.channels` event. Without it, the bot ignores public channels.
- **Windows-specific issues** (`Alt+Enter` newline, WinError 10106, UTF-8 BOM config, line endings): see the dedicated **Windows-Specific Quirks** section above.

### Auxiliary models not working
If `auxiliary` tasks (vision, compression, session_search) fail silently, the `auto` provider can't find a backend. Either set `OPENROUTER_API_KEY` or `GOOGLE_API_KEY`, or explicitly configure each auxiliary task's provider:
```bash
hermes config set auxiliary.vision.provider openrouter
hermes config set auxiliary.vision.model openrouter/gpt-4o
```
