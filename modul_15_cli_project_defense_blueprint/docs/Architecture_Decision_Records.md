# Architecture Decision Records (ADR)
### Modul 15 — CLI Project Defense Blueprint

Dokumen ini mencatat alasan teknis di balik pemilihan algoritma, struktur
data, dan pola arsitektur yang digunakan pada fase rilis akhir proyek.

---

## ADR-001: Pemisahan Packaging dan Presentation Layer

**Status:** Diterima

**Konteks:** Proyek membutuhkan dua kebutuhan berbeda di akhir siklus
pengembangan — mengemas aplikasi menjadi artefak yang dapat didistribusikan
(executable/container), dan menyiapkan materi/skenario untuk sesi sidang.

**Keputusan:** Kedua kebutuhan dipisah ke dalam `src/packager/` (build
artefak) dan `src/simulator/` + `src/ui/` (presentasi/demo), dengan
`src/generator/` sebagai jembatan yang mengonversi hasil audit menjadi
dokumentasi & slide.

**Konsekuensi:** Setiap layer dapat diuji dan diubah secara independen
tanpa memengaruhi layer lainnya (Single Responsibility Principle).

---

## ADR-002: Dry-Run Mode pada Build Scripts

**Status:** Diterima

**Konteks:** PyInstaller dan Docker tidak selalu tersedia di environment
CI/testing, namun logika penyusunan perintah build tetap perlu diverifikasi.

**Keputusan:** `pyinstaller_build.py` dan `docker_manager.py` menyediakan
mode `dry_run=True` yang hanya menyusun command tanpa mengeksekusinya.

**Konsekuensi:** Unit test (`test_build_integrity.py`) dapat berjalan cepat
dan deterministik tanpa dependensi eksternal terpasang.

---

## ADR-003: Skenario Demo Berbasis Data (Bukan Hardcoded Script)

**Status:** Diterima

**Konteks:** Demo saat sidang rawan gagal jika langkah-langkah ditulis
secara imperatif dan tersebar di banyak tempat.

**Keputusan:** Seluruh skenario didefinisikan secara deklaratif sebagai
data (`DemoScenario` + `DemoStep` di `config/demo_scenarios.py`), lalu
dieksekusi oleh `scenario_runner.py` yang generik.

**Konsekuensi:** Menambah skenario baru cukup dengan menambah data, tanpa
mengubah logika eksekusi — mengurangi risiko bug saat presentasi.

---

## ADR-004: Ekstraksi Dokumentasi via AST, Bukan Regex

**Status:** Diterima

**Konteks:** `doc_generator.py` perlu mengekstrak docstring dari seluruh
modul secara andal.

**Keputusan:** Menggunakan modul `ast` bawaan Python untuk mem-parse kode
sumber menjadi pohon sintaksis, alih-alih regex yang rapuh terhadap variasi
format kode.

**Konsekuensi:** Ekstraksi lebih akurat dan tahan terhadap perubahan gaya
penulisan kode, dengan biaya sedikit lebih kompleks dibanding regex.
