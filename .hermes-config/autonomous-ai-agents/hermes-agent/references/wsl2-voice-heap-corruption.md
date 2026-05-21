# WSL2 Voice Mode Heap Corruption

## Symptom

Hermes Agent crashes with SIGABRT (signal 6) during voice mode on WSL2. The terminal output shows:

```
malloc(): smallbin double linked list corrupted
```

Or `dmesg` shows:

```
python3.11: hermes: potentially unexpected fatal signal 6.
```

The crash happens **reproducibly** with voice mode — not on every recording, but often enough that voice mode is unusable.

## Root Cause

PortAudio negotiates an **implicit/auto block size** (`framesPerBuffer = paFramesPerBufferUnspecified`) when opening a stream. On WSL2, audio goes through the WSLg PulseAudio server over a Unix socket (`unix:/mnt/wslg/PulseServer`).

PulseAudio (via WSLg) can **renegotiate buffer parameters** mid-stream — for example, when the Windows audio subsystem restarts the virtual device, or when PulseAudio reconnects the socket after an idle timeout. When PortAudio adapts to this renegotiation, it may free its internal ring buffer while the Python callback (`sounddevice.InputStream.callback`) still holds a reference to stale memory. The `indata.copy()` in the callback then reads freed heap memory, overwriting glibc `malloc` metadata as it copies.

On the next `malloc()` or `free()` call (often during numpy array operations in the callback or when faster-whisper processes the resulting audio), glibc detects the corrupted `smallbin` linked list and calls `abort()` (signal 6).

### Detailed trace from dmesg (~/386-... microsoft-standard-WSL2)

```
RAX: 0000000000000000 RBX: 00000000000003a2 RCX: 00007765a88a648c
RDX: 0000000000000006 RSI: 00000000000003a2 RDI: 0000000000000323
ORIG_RAX: 00000000000000ea  →  tgkill (syscall 234 / 0xea)
```

The syscall `tgkill` with signal 6 (SIGABRT) — the process sent SIGABRT to one of its own threads. This is exactly what glibc does when `malloc` detects heap corruption via its integrity checks (`smallbin double linked list`).

## Fix

Add an explicit `blocksize` to the `sd.InputStream(...)` in `tools/voice_mode.py`:

```python
stream = sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype=DTYPE,
    blocksize=1024,      # 64 ms @ 16 kHz — stabilises PulseAudio buffer contract
    callback=_callback,
)
```

**Why 1024?** At 16 kHz sample rate, 1024 samples = 64 ms. This is a standard PortAudio block size:
- Short enough for responsive VAD (voice activity detection)
- Long enough to avoid the PulseAudio zero-size-buffer edge case
- Matches what most native ALSA/PulseAudio apps use by default

The explicit `blocksize` tells PortAudio to negotiate a fixed buffer with PulseAudio on stream open, rather than using `paFramesPerBufferUnspecified` (which allows PulseAudio to change it dynamically). Without the dynamic renegotiation, there is no buffer-free-and-reallocate cycle, so no use-after-free in the callback.

## Diagnostic Steps

### 1. Confirm it's heap corruption (not missing libs)

```bash
dmesg | grep -i "signal 6\|SIGABRT\|hermes" | tail -5
```

Look for `fatal signal 6` with Comm=`python3.11` and `ORIG_RAX: ...ea` (tgkill).

### 2. Check PULSE_SERVER is configured

```bash
echo $PULSE_SERVER
# Should show: unix:/mnt/wslg/PulseServer
```

### 3. Check libportaudio2 is installed

```bash
dpkg -l libportaudio2 | tail -1
```

### 4. Test raw audio capture outside Hermes

```python
# From the hermes venv
python3 -c "
import sounddevice as sd
import numpy as np

# Explicit blocksize test
rec = sd.rec(int(16000), samplerate=16000, channels=1, dtype='int16', blocksize=1024)
sd.wait()
print(f'Recorded {len(rec)} samples, max={np.abs(rec).max()}')
"
```

If this itself crashes, the issue is at the PortAudio/sounddevice level and the blocksize fix should help.

## Alternative Workarounds

### Switch STT provider (avoids faster-whisper C++ buffer handling)

If the blocksize fix alone doesn't resolve the crash, the issue may also involve faster-whisper's CTranslate2 C++ layer mishandling WSL2-sourced audio buffers. Switch to a cloud STT:

```bash
hermes config set stt.provider groq
# Set GROQ_API_KEY in ~/.hermes/.env
```

Or:

```bash
hermes config set stt.provider openai
# Set VOICE_TOOLS_OPENAI_KEY in ~/.hermes/.env
```

### Increase max_recording_seconds

If crashing correlates with long recordings:

```bash
hermes config set voice.max_recording_seconds 30
```

### PulseAudio socket refresh

If crash happens after WSL sleep/resume:

```bash
# In PowerShell (as admin):
wsl --shutdown
# Then reopen WSL terminal
```