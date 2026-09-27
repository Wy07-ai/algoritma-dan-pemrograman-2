"""
splash_screen.py
------------------
Layar pembuka CLI dengan ASCII Art untuk memberi kesan profesional
saat aplikasi pertama kali dijalankan, termasuk di sesi sidang.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from config.release_settings import DEFAULT_RELEASE  # noqa: E402

ASCII_LOGO = r"""
   ____ _     ___   ____       __
  / ___| |   |_ _| |  _ \  ___ / _| ___ _ __  ___  ___
 | |   | |    | |  | | | |/ _ \ |_ / _ \ '_ \/ __|/ _ \
 | |___| |___ | |  | |_| |  __/  _|  __/ | | \__ \  __/
  \____|_____|___| |____/ \___|_|  \___|_| |_|___/\___|
"""


def render_splash(release=DEFAULT_RELEASE) -> str:
    """Menyusun teks splash screen lengkap sebagai string siap-cetak."""
    lines = [
        ASCII_LOGO,
        release.as_banner(),
        "-" * 60,
        "Tekan Ctrl+C kapan saja untuk keluar dengan aman (graceful shutdown).",
        "-" * 60,
    ]
    return "\n".join(lines)


def show_splash(release=DEFAULT_RELEASE) -> None:
    print(render_splash(release))


if __name__ == "__main__":
    show_splash()
