#!/usr/bin/env python3
"""News-image entry for make.fun news-image-20261117 (Python 3.13,
standard library only).

The image is entry.png beside this file: a newspaper front page,
"THE GLOBAL DISPATCH", drawn by draw.py in this repository, summing
up the world news of Tuesday 17 November 2026. The program copies it
to the output directory as entry.png; the grader runs it twice and
both runs must produce the same bytes, which a plain copy guarantees.

Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dest = OUT_DIR / "entry.png"
    shutil.copyfile(HERE / "entry.png", dest)
    print(f"entry.png copied to {dest}")


if __name__ == "__main__":
    main()
