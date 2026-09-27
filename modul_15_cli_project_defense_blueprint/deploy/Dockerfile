# Dockerfile — modul_15_cli_project_defense_blueprint
# Blueprint lingkungan sistem operasi terisolasi agar aplikasi dapat
# dijalankan di perangkat apa pun tanpa masalah perbedaan dependensi.

FROM python:3.11-slim

LABEL maintainer="Tim Pengembang Algoritma & Pemrograman 2"
LABEL description="CLI Project Defense Blueprint - reproducible environment"

WORKDIR /app

# Salin metadata dependensi lebih dulu agar layer cache Docker optimal
COPY pyproject.toml ./

# Salin seluruh source code proyek
COPY . .

# Instal proyek (mode editable tidak diperlukan di container rilis)
RUN pip install --no-cache-dir .

ENTRYPOINT ["python", "main.py"]
