#!/usr/bin/env python3
"""Zip a Magisk module directory into a flashable module archive.

Usage: python build_module.py <module_dir> <out_zip>

Keeps relative paths with forward slashes (required by Magisk), skips
editor/OS junk, and stores module.prop first.
"""
import os
import sys
import zipfile

SKIP_DIRS = {".git", ".idea", "__pycache__", ".vscode"}
SKIP_FILES = {".DS_Store", "Thumbs.db", "desktop.ini"}


def collect(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name in SKIP_FILES:
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            files.append((rel, full))
    files.sort(key=lambda item: (item[0] != "module.prop", item[0]))
    return files


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    root, out = sys.argv[1], sys.argv[2]
    if not os.path.isfile(os.path.join(root, "module.prop")):
        raise SystemExit("error: %s has no module.prop" % root)
    files = collect(root)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for rel, full in files:
            z.write(full, rel)
    print("built %s (%d files, %.2f MiB)" % (out, len(files), os.path.getsize(out) / 1048576))
    for rel, _ in files[:6]:
        print("   ", rel)


if __name__ == "__main__":
    main()
