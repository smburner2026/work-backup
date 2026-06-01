# Writing Complex Text to SSH Targets via Base64

## The problem

When working from a Hermes agent (VPS) that needs to write files to an SSH target (WSL compute backend), standard shell approaches fail:

- `echo "text" | ssh host "cat > file"` — fails on apostrophes, quotes, backticks, $, &, braces
- `cat > file << 'EOF' ... EOF` — fails if the text itself contains the delimiter word
- `printf '%s' "text" | ssh host "tee file > /dev/null"` — same escaping problems
- SCP from temp file — works but requires intermediate file management

**Any method that passes text through a bash shell will break** on translation text containing: apostrophes, backticks, em-dashes, parentheses, curly braces, dollar signs, ampersands, or Unicode characters that bash interprets.

## The fix: base64 transport

Base64 is pure ASCII and survives any shell quoting without escaping issues.

### Technique — write via Python subprocess

```python
import subprocess, base64

content = """... ANY text with ANY special characters ..."""
encoded = base64.b64encode(content.encode('utf-8')).decode('ascii')

# Create new file:
cmd = f"echo '{encoded}' | base64 -d > /path/to/output.txt"

# Append to existing file:
cmd = f"echo '{encoded}' | base64 -d >> /path/to/output.txt"

subprocess.run(["ssh", "local-machine", cmd])
```

### Step by step

1. Place your text in a Python variable (triple-quoted string)
2. `base64.b64encode(content.encode('utf-8')).decode('ascii')` — gives you a pure ASCII string
3. Surround it in `echo '...'` — single quotes are safe because the base64 alphabet contains no single quotes
4. Pipe to `base64 -d >|` on the remote side
5. Use `>` for first write, `>>` for subsequent appends

### Why this works

- Base64 alphabet: `A-Z a-z 0-9 + / =` — none of these are shell-special when single-quoted
- Single quotes in bash prevent ALL expansion — no variable substitution, no command substitution, no backslash interpretation
- The only character that breaks single quotes is a single quote itself, which base64 never produces

### Variations

- **Very large texts (100KB+)**: Works fine. The SSH command length limit is ~2MB. For truly enormous content, split into multiple writes.
- **Binary content**: Same technique — base64 handles binary transparently.
- **Multiple SSH targets**: The pattern is `ssh <target> "echo '...' | base64 -d > path"` — works with any SSH host.
- **From a pure bash environment** (no Python): `base64 <<< "text" | ssh host "base64 -d > file"` but this embeds a trailing newline.

## Alternatives not worth pursuing

| Method | Problem |
|--------|---------|
| Heredoc in SSH | Text may contain delimiter word |
| Heredoc via `ssh host bash -s <<'EOF'` | EOF collision, requires temp file for large text |
| `printf '%s'` | Backtick in translation text breaks it |
| SCP temp file | Works but requires cleanup; overkill for a single text block |
| rsync | Overkill; designed for directory sync |
