"""
docker_manager.py
------------------
Pengelola blueprint lingkungan sistem operasi terisolasi (Docker) yang
menjamin aplikasi dapat dijalankan di perangkat apa pun tanpa masalah
perbedaan dependensi (reproducible environment).
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from config.release_settings import DOCKER_SETTINGS  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCKERFILE_PATH = PROJECT_ROOT / "deploy" / "Dockerfile"


class DockerError(RuntimeError):
    """Dilempar saat perintah Docker gagal dieksekusi."""


def docker_available() -> bool:
    return shutil.which("docker") is not None


def image_tag() -> str:
    return f"{DOCKER_SETTINGS['image_name']}:{DOCKER_SETTINGS['image_tag']}"


def build_image_command() -> list[str]:
    return [
        "docker", "build",
        "-t", image_tag(),
        "-f", str(DOCKERFILE_PATH),
        str(PROJECT_ROOT),
    ]


def run_container_command(detach: bool = False) -> list[str]:
    cmd = ["docker", "run"]
    if detach:
        cmd.append("-d")
    cmd.extend(["--rm", "-it", image_tag()])
    return cmd


def build_image(dry_run: bool = False) -> dict:
    cmd = build_image_command()
    if dry_run or not docker_available():
        return {
            "executed": False,
            "reason": "dry_run aktif" if dry_run else "Docker tidak ditemukan di PATH",
            "command": " ".join(cmd),
        }

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise DockerError(f"Docker build gagal:\n{result.stderr}")

    return {"executed": True, "command": " ".join(cmd), "image": image_tag()}


if __name__ == "__main__":
    report = build_image(dry_run=True)
    print("[docker_manager] Rencana build image Docker:")
    for k, v in report.items():
        print(f"  {k}: {v}")
