#!/usr/bin/env python3
"""Read source lines 1-400 and prepare them for translation"""
import subprocess

source_path = "/home/vthen/work/post-colonial-vietnam/sources/vstb/translations/ch9-clean.txt"
output_path = "/home/vthen/work/post-colonial-vietnam/sources/vstb/translations/ch9-translated.txt"

# Read lines 1-400
result = subprocess.run(
    ["ssh", "local-machine", f"sed -n '1,200p' {source_path}"],
    capture_output=True, text=True, timeout=30
)
print(result.stdout[:100])
