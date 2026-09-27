"""
test_build_integrity.py
-------------------------
Memastikan hasil kompilasi berkas biner/container dapat berjalan
lancar tanpa missing dependencies, dengan menguji logika penyusunan
perintah build (bukan menjalankan build sungguhan agar test tetap cepat
dan tidak butuh PyInstaller/Docker terpasang).
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.packager.pyinstaller_build import build_command, run_build  # noqa: E402
from src.packager.docker_manager import build_image_command, build_image  # noqa: E402


def test_pyinstaller_command_contains_entry_point():
    cmd = build_command("main.py")
    assert "main.py" in cmd
    assert "--onefile" in cmd


def test_pyinstaller_dry_run_does_not_execute():
    report = run_build(dry_run=True)
    assert report["executed"] is False
    assert "command" in report


def test_docker_build_command_has_correct_tag():
    cmd = build_image_command()
    assert "docker" in cmd
    assert "build" in cmd
    assert any(":" in c for c in cmd)  # image:tag present


def test_docker_dry_run_does_not_execute():
    report = build_image(dry_run=True)
    assert report["executed"] is False
    assert "command" in report


if __name__ == "__main__":
    test_pyinstaller_command_contains_entry_point()
    test_pyinstaller_dry_run_does_not_execute()
    test_docker_build_command_has_correct_tag()
    test_docker_dry_run_does_not_execute()
    print("Semua test build integrity LULUS.")
