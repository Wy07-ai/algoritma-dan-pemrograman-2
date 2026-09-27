"""
pyinstaller_build.py
---------------------
Skrip otomatisasi untuk mengompilasi dan mengemas seluruh kode sumber
Python menjadi satu berkas biner/eksekusi mandiri (.exe / .bin) memakai
PyInstaller.

Catatan: PyInstaller harus terpasang (`pip install pyinstaller`) di
environment build. Skrip ini hanya menyusun & menjalankan perintahnya,
bukan menggantikan PyInstaller itu sendiri.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from config.release_settings import BUILD_SETTINGS, DEFAULT_RELEASE  # noqa: E402


class BuildError(RuntimeError):
    """Dilempar saat proses build executable gagal."""


def check_pyinstaller_available() -> bool:
    """Cek apakah PyInstaller terpasang di environment saat ini."""
    return shutil.which("pyinstaller") is not None


def build_command(entry_point: str | None = None) -> list[str]:
    """Menyusun argumen command-line untuk PyInstaller berdasar BUILD_SETTINGS."""
    entry = entry_point or BUILD_SETTINGS["entry_point"]
    cmd = ["pyinstaller", entry, "--name", BUILD_SETTINGS["output_name"]]

    if BUILD_SETTINGS.get("onefile"):
        cmd.append("--onefile")
    if not BUILD_SETTINGS.get("console", True):
        cmd.append("--noconsole")
    if BUILD_SETTINGS.get("icon_path"):
        cmd.extend(["--icon", BUILD_SETTINGS["icon_path"]])

    cmd.extend(["--distpath", BUILD_SETTINGS["target_dir"]])
    return cmd


def run_build(entry_point: str | None = None, dry_run: bool = False) -> dict:
    """
    Menjalankan proses build. Jika `dry_run=True`, hanya mengembalikan
    perintah yang akan dijalankan tanpa benar-benar mengeksekusi PyInstaller
    (berguna untuk testing / CI tanpa PyInstaller terpasang).
    """
    cmd = build_command(entry_point)

    if dry_run or not check_pyinstaller_available():
        return {
            "executed": False,
            "reason": "dry_run aktif" if dry_run else "PyInstaller tidak ditemukan",
            "command": " ".join(cmd),
        }

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise BuildError(f"Build gagal:\n{result.stderr}")

    return {
        "executed": True,
        "command": " ".join(cmd),
        "output_path": str(Path(BUILD_SETTINGS["target_dir"]) / BUILD_SETTINGS["output_name"]),
        "release": DEFAULT_RELEASE.as_banner(),
    }


if __name__ == "__main__":
    report = run_build(dry_run=True)
    print("[pyinstaller_build] Rencana build:")
    for k, v in report.items():
        print(f"  {k}: {v}")
