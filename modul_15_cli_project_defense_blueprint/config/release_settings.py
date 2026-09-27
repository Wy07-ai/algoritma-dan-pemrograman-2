"""
release_settings.py
--------------------
Memuat metadata rilis (Semantic Versioning) dan identitas pengembang
untuk keperluan packaging, dokumentasi, dan sesi sidang/demo proyek.
"""

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class ReleaseMetadata:
    app_name: str = "CLI Project Defense Suite"
    version: str = "1.0.0"          # Semantic Versioning: MAJOR.MINOR.PATCH
    codename: str = "Phoenix"
    build_date: str = field(default_factory=lambda: date.today().isoformat())
    author: str = "Tim Pengembang Algoritma & Pemrograman 2"
    license: str = "MIT"
    python_requires: str = ">=3.10"
    repository: str = "local://modul_15_cli_project_defense_blueprint"

    def as_banner(self) -> str:
        return (
            f"{self.app_name} v{self.version} ({self.codename})\n"
            f"Build: {self.build_date} | Author: {self.author} | "
            f"License: {self.license}"
        )


# Threshold & opsi build executable
BUILD_SETTINGS = {
    "entry_point": "main.py",
    "output_name": "cli_defense_app",
    "onefile": True,
    "console": True,
    "icon_path": None,
    "target_dir": "dist/",
}

# Konfigurasi Docker
DOCKER_SETTINGS = {
    "image_name": "cli-project-defense",
    "image_tag": "1.0.0",
    "base_image": "python:3.11-slim",
    "container_workdir": "/app",
}

DEFAULT_RELEASE = ReleaseMetadata()
