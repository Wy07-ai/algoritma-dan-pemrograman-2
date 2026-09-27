# 🚀 Algoritma dan Pemrograman 2 (Advanced CLI & Algorithmic Systems)

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Architecture](https://img.shields.io/badge/architecture-Decoupled%20%2F%20Modular-success.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Selamat datang di repositori **Algoritma dan Pemrograman 2**. Repositori ini berisi **14 modul sistem komprehensif** yang dirancang menggunakan _software engineering best practices_, arsitektur perangkat lunak berbasis CLI (_Command Line Interface_), optimasi struktur data, analisis kompleksitas ($Big-O$), hingga _automated benchmarking & resilience system_.

---

## 📅 Progress & Roadmap Praktikum

| Pertemuan | Topik Materi                                                   | Nama Modul / Folder                        |          Status          |
| :-------: | :------------------------------------------------------------- | :----------------------------------------- | :----------------------: |
|  **M1**   | Advanced IPO Problem Analysis & Decoupled Architecture         | `modul_01_advanced_ipo_system`             |        ✅ selesai        |
|  **M2**   | Modular Algorithm Design & Event Bus Pattern                   | `modul_02_modular_algorithm_design`        |        ✅ selesai        |
|  **M3**   | Rekursi vs Iterasi, Call Stack & Tail Call Optimization        | `modul_03_recursion_vs_iteration`          |        ✅ selesai        |
|  **M4**   | Algorithmic Scale & Big-O Stress Testing Engine                | `modul_04_algorithmic_scale`               |        ✅ selesai        |
|  **M5**   | Search Algorithm Anatomy & Search Space Inspection             | `modul_05_search_algorithm_anatomy`        |        ✅ selesai        |
|  **M6**   | Basic Sorting Blueprints, Stability & Telemetry Inspector      | `modul_06_basic_sorting_blueprints`        |        ✅ selesai        |
|  **M7**   | Algorithm Integration Blueprint & Multi-Pipeline Orchestrator  | `modul_07_algorithm_integration`           |        ✅ selesai        |
|  **M9**   | Architecting Robust Software & Circuit Breaker Fault-Tolerance | `modul_09_architecting_robust_software`    |        ✅ selesai        |
|  **M10**  | Dictionary & Set Optimization, Hash Collisions & Bloom Filters | `modul_10_dictionary_and_set_optimization` |        ✅ selesai        |
|  **M11**  | Modern Data Pipelines & Memory-Efficient Stream Processing     | `modul_11_modern_data_pipelines`           |        ✅ selesai        |
|  **M12**  | CLI Architecture Blueprint & Subcommand Dispatcher Engine      | `modul_12_cli_architecture_blueprint`      |        ✅ selesai        |
|  **M13**  | CLI System Blueprint, Kernel Bootstrapper & Persistence        | `modul_13_cli_system_blueprint`            |        ✅ selesai        |
|  **M14**  | Audit Kompleksitas Sistem CLI, Latency & SLA Verification      | `modul_14_audit_kompleksitas_sistem_cli`   |        ✅ selesai        |
|  **M15**  | CLI Project Defense Blueprint, Binary Packaging & Auto-Demo    | `modul_15_cli_project_defense_blueprint`   |        ✅ selesai        |

---

## 📐 Arsitektur Sistem Global

Seluruh modul dirancang menggunakan pendekatan **Decoupled Layer Architecture** dan **Modular Design Pattern**, memisahkan secara tegas antara _Presentation Layer_ (CLI Terminal UI), _Domain/Business Logic_, _Data Processing Pipeline_, dan _Infrastructure/Storage_.

---

🛠️ Panduan Instalasi & Penggunaan

1. Prasyarat Sistem
   Python: v3.10 atau versi lebih baru 🐍

Git: Untuk kloning repositori 📦

2. Kloning Repositori
   Bash
   git clone [https://github.com/wyonugrahav2/algoritma-dan-pemrograman-2.git](https://github.com/wyonugrahav2/algoritma-dan-pemrograman-2.git)
   cd algoritma-dan-pemrograman-2
3. Lingkungan Virtual & Dependensi
   Bash

## Membuat Virtual Environment

python -m venv venv

## Aktivasi Lingkungan Virtual

## Windows:

venv\Scripts\activate

## Linux / MacOS:

source venv/bin/activate

## Instalasi Dependensi

pip install -r requirements.txt
🏃 Cara Menjalankan Modul
Setiap modul dilengkapi dengan main.py yang berfungsi sebagai entry point independen. Kamu dapat menjalankan modul spesifik langsung dari terminal:

Bash

## Contoh: Menjalankan Modul 04 (Stress Test Big-O)

python modul_04_algorithmic_scale/main.py

## Contoh: Menjalankan Modul 06 (Visualizer Sorting)

python modul_06_basic_sorting_blueprints/main.py

## Contoh: Menjalankan Modul 15 (Defense Dashboard)

python modul_15_cli_project_defense_blueprint/main.py
🧪 Pengujian (Testing Suite)
Repositori ini dilengkapi dengan unit testing dan integration testing komprehensif. Untuk menjalankan pengujian di seluruh modul:

Bash

## Menjalankan seluruh unit test

pytest

## Menjalankan test dengan laporan cakupan kode (coverage)

pytest --cov=src
📝 Lisensi
Proyek ini dilisensikan di bawah MIT License — bebas digunakan dan dikembangkan untuk keperluan edukasi dan riset. 📄

---

### Cara Update ke GitHub 🚀

Ganti seluruh isi file `readme.md` di VS Code kamu dengan kode di atas, lalu jalankan perintah ini di terminal:

```bash
git add readme.md
git commit -m "docs: add progress roadmap table with empty status 📊"
git push origin main
```
