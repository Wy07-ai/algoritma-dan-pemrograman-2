"""
auto_typer.py
--------------
Mengotomatisasi pengetikan perintah di terminal secara terkontrol,
sehingga demo fitur A-Z dapat berjalan tanpa risiko kesalahan ketik
(typo) di depan penguji/dosen saat sesi sidang.
"""

from __future__ import annotations

import sys
import time


def type_out(text: str, delay: float = 0.03, newline: bool = True) -> None:
    """
    Mencetak `text` karakter demi karakter seolah sedang diketik secara
    live di terminal. `delay` adalah jeda (detik) antar-karakter.
    """
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    if newline:
        sys.stdout.write("\n")
        sys.stdout.flush()


def type_prompt(command: str, prompt: str = "$ ", delay: float = 0.03) -> None:
    """Mencetak prompt shell diikuti perintah yang diketik otomatis."""
    sys.stdout.write(prompt)
    sys.stdout.flush()
    type_out(command, delay=delay)


def countdown(seconds: int, label: str = "Memulai demo dalam") -> None:
    """Hitung mundur sebelum sesi demo dimulai, agar presenter siap."""
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\r{label}: {remaining}s ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * 40 + "\r")


if __name__ == "__main__":
    countdown(3)
    type_prompt("app search --query demo")
    print("(output simulasi hasil pencarian akan tampil di sini)")
