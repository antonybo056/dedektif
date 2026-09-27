"""Dedektif oyununu başlatır:  python main.py"""
import sys
from pathlib import Path

from oyun.oyun import Oyun

if __name__ == "__main__":
    for akis in (sys.stdout, sys.stdin):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    Oyun(Path(__file__).with_name("kayit.json")).calistir()
