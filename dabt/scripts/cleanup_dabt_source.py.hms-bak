#!/usr/bin/env python3
"""Clean up the dabt-materials source directory by removing junk files."""
import os
import shutil

src = "/root/dabt-materials"

# 1. Delete Shipkowski Materials entirely (confirmed byte-identical duplicate)
shipkowski = os.path.join(src, "Shipkowski Materials")
if os.path.exists(shipkowski):
    print(f"Removing Shipkowski Materials...")
    shutil.rmtree(shipkowski)
    print("  Done.")

# 2. Delete (1) variant files
print("Removing (1) variant files...")
for root, dirs, files in os.walk(src):
    for f in files:
        if " (1)" in f:
            path = os.path.join(root, f)
            os.remove(path)
            print(f"  Removed: {path}")
print("  Done.")

# 3. Delete ZIP archives
print("Removing ZIP archives...")
for root, dirs, files in os.walk(src):
    for f in files:
        if f.endswith(".zip"):
            path = os.path.join(root, f)
            os.remove(path)
            print(f"  Removed: {path}")
print("  Done.")

# 4. Delete junk files
junk_patterns = [
    "2018 Study Group Schedule",
    "Sign up sheet",
    "answer template",
    "The password for Klaassen",
]
print("Removing junk files...")
for root, dirs, files in os.walk(src):
    for f in files:
        for pattern in junk_patterns:
            if pattern in f:
                path = os.path.join(root, f)
                os.remove(path)
                print(f"  Removed: {path}")
                break
print("  Done.")

# 5. Delete decorative images
image_patterns = [
    "Evaluating-the-Risks-of-Drug-Exposure-in-Human-Pregnancies.jpg",
    "DNA Damage Response Pathway.png",
    "Acinus and lobule.jpg",
]
print("Removing decorative images...")
for root, dirs, files in os.walk(src):
    for f in files:
        for pattern in image_patterns:
            if f == pattern:
                path = os.path.join(root, f)
                if os.path.exists(path):
                    os.remove(path)
                    print(f"  Removed: {path}")
                break
print("  Done.")

# 6. Remove empty directories
print("Removing empty directories...")
for root, dirs, files in os.walk(src, topdown=False):
    if root == src:
        continue  # don't try to remove top-level
    try:
        if not os.listdir(root):
            os.rmdir(root)
            print(f"  Removed empty dir: {root}")
    except (PermissionError, OSError):
        pass
print("  Done.")

# Summary
print("\n=== Cleanup Complete ===")
total_files = sum(len(files) for _, _, files in os.walk(src))
total_size = 0
for root, dirs, files in os.walk(src):
    for f in files:
        try:
            total_size += os.path.getsize(os.path.join(root, f))
        except:
            pass
print(f"Remaining files: {total_files}")
print(f"Remaining size: {total_size / (1024**3):.1f} GB")
