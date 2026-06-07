## Voice & Transcription

Hermes supports two voice workflows in the CLI: **push-to-talk** (press a key to record, press again to transcribe) and **continuous VAD** (voice activity detection — auto-stops on silence). On messaging platforms, voice messages are auto-transcribed using the same STT provider.

### Prerequisites

**Python packages** needed for voice to work in the CLI:
```bash
# From the hermes venv:
python3 -m pip install faster-whisper sounddevice soundfile
```
- `faster-whisper` — local STT (used by `stt.provider: local`)
- `sounddevice` — microphone capture (needs system PortAudio library)
- `soundfile` — WAV file I/O for recording
- `edge-tts` — free TTS (bundled with Hermes, already installed)

**System dependency** (Linux/WSL):
```bash
sudo apt-get install -y libportaudio2    # required by sounddevice
```
On WSL, audio routing goes through WSLg's PulseAudio server at `$PULSE_SERVER` (`unix:/mnt/wslg/PulseServer`). If `sounddevice` raises `OSError: PortAudio library not found`, PortAudio is missing.

**Hermes venv may lack pip** — fix with:
```bash
python3 -m ensurepip --upgrade
```

### STT (Speech-to-Text) — Microphone → Text

Voice messages from messaging platforms are auto-transcribed.

Provider priority (auto-detected):
1. **Local faster-whisper** — free, no API key: `pip install faster-whisper`
2. **Groq Whisper** — free tier: set `GROQ_API_KEY`
3. **OpenAI Whisper** — paid: set `VOICE_TOOLS_OPENAI_KEY`
4. **Mistral Voxtral** — set `MISTRAL_API_KEY`

Config:
```yaml
stt:
  enabled: true
  provider: local        # local, groq, openai, mistral
  local:
    model: base          # tiny, base, small, medium, large-v3
```

### TTS (Text-to-Speech) — Text → Spoken Audio

| Provider | Env var | Free? |
|----------|---------|-------|
| Edge TTS | None | Yes (default, bundled with Hermes) |
| ElevenLabs | `ELEVENLABS_API_KEY` | Free tier |
| OpenAI | `VOICE_TOOLS_OPENAI_KEY` | Paid |
| MiniMax | `MINIMAX_API_KEY` | Paid |
| Mistral (Voxtral) | `MISTRAL_API_KEY` | Paid |
| NeuTTS (local) | None (`pip install neutts[all]` + `espeak-ng`) | Free |

### Voice Config Section

Full voice configuration lives under `voice:` in `config.yaml`:

```yaml
voice:
  record_key: ctrl+b          # Push-to-talk keybinding
  max_recording_seconds: 120  # Max recording duration
  auto_tts: false             # Auto-speak each response (true = always speak)
  beep_enabled: true          # Audible cues on record start/stop
  silence_threshold: 200      # VAD sensitivity (lower = more sensitive)
```

### In-Session Commands

| Command | Effect |
|---------|--------|
| `/voice on` | Full voice-voice mode (always listening + TTS responses) |
| `/voice tts` | TTS output only (type your input, hear spoken replies) |
| `/voice off` | Disable voice entirely |
| **Ctrl+B** (push-to-talk) | Press to start recording, press again to stop and transcribe |

When `auto_tts: true` is set in config, each agent response is spoken aloud automatically without needing `/voice tts`.

### Verifying Voice Works

Test microphone access:
```python
# From the hermes venv
python3 -c "
import sounddevice as sd
for i, d in enumerate(sd.query_devices()):
    if d['max_input_channels'] > 0:
        print(f'  [{i}] {d[\"name\"]}')
"
```
On WSL, confirm `echo $PULSE_SERVER` points to a WSLg path. If no input devices appear, install `libportaudio2` and verify Windows mic permissions.

---

