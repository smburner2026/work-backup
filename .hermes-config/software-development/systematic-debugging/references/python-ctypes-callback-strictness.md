# Python 3.12+ ctypes Callback Signature Strictness

## Symptom

A PyInstaller-packaged Windows app (or any Python/Windows ctypes app) crashes on startup with:

```
ctypes.ArgumentError: argument 3: TypeError: expected WinFunctionType instance instead of function
```

The error traces to a call like `EnumDisplayMonitors(None, None, callback_fn, None)` where `callback_fn` is a regular nested Python function.

## Root Cause

**Python 3.12 tightened ctypes validation.** When a WinAPI function is declared with `argtypes` specifying a `WINFUNCTYPE` callback type, Python 3.12+ strictly validates that the actual callback passed matches the declared signature. In Python 3.11 and earlier, passing a plain Python function as a callback was silently accepted even if its parameter types didn't exactly match.

The mismatch occurs when:
1. A `WINFUNCTYPE` is declared with specific parameter types (e.g. `ctypes.POINTER(RECT)` for a `rect` parameter)
2. The callback function uses a different type for the same parameter (e.g. `ctypes.c_void_p` instead of `ctypes.POINTER(RECT)`)

## Fix

Wrap the callback at the call site with the declared `WINFUNCTYPE`:

```python
# BAD (Python 3.12 crash):
if not user32.EnumDisplayMonitors(None, None, callback_fn, None):
    ...

# GOOD:
MONITORENUMPROC = self.MONITORENUMPROC  # or wherever the WINFUNCTYPE was stored
if not user32.EnumDisplayMonitors(None, None, MONITORENUMPROC(callback_fn), None):
    ...
```

Or, if the callback is defined with exact types matching the WINFUNCTYPE, you can pass it directly. The key is parameter type consistency.

## Example Pattern

```python
# In __init__ or set-up:
self.MONITORENUMPROC = ctypes.WINFUNCTYPE(
    ctypes.c_int,           # return type
    ctypes.c_void_p,        # hmonitor
    ctypes.c_void_p,        # hdc_monitor
    ctypes.POINTER(RECT),   # rect  ← must match callback
    ctypes.c_void_p,        # data
)

# In the method using it:
def _get_windows_display_names(self) -> list[str]:
    def enum_monitor_proc(
        hmonitor: ctypes.c_void_p,
        hdc_monitor: ctypes.c_void_p,
        rect: ctypes.c_void_p,       # ← declared as void_p, WINFUNCTYPE says POINTER(RECT)
        data: ctypes.c_void_p,
    ) -> int:
        ...

    # Python 3.12 fix: wrap with WINFUNCTYPE
    MONITORENUMPROC = self.MONITORENUMPROC
    if not self.user32.EnumDisplayMonitors(None, None, MONITORENUMPROC(enum_monitor_proc), None):
        logging.warning("EnumDisplayMonitors failed.")
```

## Detection

When you see `ctypes.ArgumentError` with a message containing `expected WinFunctionType instance instead of function`, check:

1. Is the code running under Python 3.12+? (Check `python3 --version` or look for `python312.dll` in PyInstaller bundles)
2. Does the failing line pass a callback function to a WinAPI?
3. Does the callback signature exactly match the `WINFUNCTYPE` declared in `argtypes`?

## Related: Other Python 3.12 ctypes Changes

Python 3.12 also made other ctypes stricter:
- `ctypes.Structure` field type mismatches now raise errors instead of warnings
- `ctypes.c_void_p` / `ctypes.POINTER(...)` distinctions are enforced more strictly in callback signatures

## Verification

After applying the fix:
- The app should start without the `ctypes.ArgumentError` crash
- If the error persists, check ALL callback-based WinAPI calls in the code — not just the one in the traceback
- Other `WINFUNCTYPE` declarations (e.g. `SetWinEventHook` callbacks) may also need the same wrapping pattern
