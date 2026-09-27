# Makefile — modul_15_cli_project_defense_blueprint
# Otomatisasi perintah umum: build, demo, run-docker, test.

.PHONY: help build demo demo-full run-docker docker-build test docs

help:
	@echo "Perintah tersedia:"
	@echo "  make build        - Build executable mandiri via PyInstaller"
	@echo "  make demo         - Jalankan skenario demo singkat (quick_tour)"
	@echo "  make demo-full    - Jalankan skenario demo lengkap (full_defense)"
	@echo "  make docker-build - Build Docker image dari deploy/Dockerfile"
	@echo "  make run-docker   - Jalankan aplikasi dalam container Docker"
	@echo "  make test         - Jalankan seluruh unit test"
	@echo "  make docs         - Generate dokumentasi kode otomatis (Markdown)"

build:
	python src/packager/pyinstaller_build.py

demo:
	python src/simulator/scenario_runner.py quick_tour

demo-full:
	python src/simulator/scenario_runner.py full_defense

docker-build:
	python src/packager/docker_manager.py

run-docker:
	docker run --rm -it cli-project-defense:1.0.0

test:
	python -m pytest tests/ -v

docs:
	python src/generator/doc_generator.py
