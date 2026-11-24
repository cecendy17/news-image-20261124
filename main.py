#!/usr/bin/env python3
"""Copy the pre-rendered entry image to the make.fun output directory."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if out_dir.endswith(".png"):
        dest = out_dir
    else:
        dest = os.path.join(out_dir, "entry.png")
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"), dest)
    print(dest)

if __name__ == "__main__":
    main()
