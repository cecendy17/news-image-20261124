#!/usr/bin/env python3
"""Copy entry.png to the make.fun output directory (deterministic)."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.png")
if os.path.isdir(OUT_DIR) or OUT_DIR.endswith(os.sep):
    DST = os.path.join(OUT_DIR, "entry.png")
else:
    DST = OUT_DIR
os.makedirs(os.path.dirname(DST) or ".", exist_ok=True)
shutil.copyfile(SRC, DST)
print(DST)
