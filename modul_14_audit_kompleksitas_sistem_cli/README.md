# Modul 14 — Audit Kompleksitas Sistem CLI

Audit komprehensif terhadap performa, efisiensi algoritma, dan konsumsi
memori pada sistem CLI. Sistem ini menguji fungsi target secara
empiris pada berbagai skala data (`N`), mengestimasi kelas
kompleksitas Big-O dari hasil pengukuran nyata, lalu mengevaluasinya
terhadap Service Level Agreement (SLA) yang telah ditetapkan.

## Fitur Utama

- **Time Auditor** — profiler mikrodetik (`time.perf_counter`).
- **Memory Auditor** — pengukur puncak RAM & pendeteksi indikasi
  *memory leak* (`tracemalloc`).
- **Complexity Auditor** — estimasi Big-O empiris via regresi linear
  pada kandidat kurva pertumbuhan (`O(1)` s.d. `O(2^N)`).
- **Load Generator & Scenario Runner** — menjalankan Best/Average/Worst
  Case pada skala `N` dari 100 hingga 1.000.000.
- **SLA Evaluator** — menentukan status **PASS/FAIL** berdasarkan
  ambang waktu, memori, dan kelas kompleksitas.
- **Dashboard CLI & Score Presenter** — ringkasan visual di terminal.
- **Report Exporter** — ekspor ke JSON mentah dan PDF resmi
  (fallback ke Markdown jika `reportlab` tidak tersedia).

## Instalasi

```bash
pip install -r requirements.txt   # atau: pip install reportlab
```

## Menjalankan Audit

```bash
# Audit semua fungsi contoh dengan skala & repetisi default
python main.py

# Audit fungsi tertentu saja
python main.py --functions quick_sort binary_search

# Kustom skala N dan repetisi
python main.py --functions bubble_sort --scales 100 1000 5000 --repeat 3

# Jalankan hanya skenario tertentu
python main.py --functions linear_search --scenarios worst_case

# Ekspor laporan
python main.py --export json pdf
```

Laporan akan tersimpan di direktori `audit_reports/` (dapat diubah
lewat `AUDIT_REPORTS_DIR` di `.env`).

## Menjalankan Unit Test

```bash
python -m pytest tests/ -v
```

## Struktur Proyek

```
modul_14_audit_kompleksitas_sistem_cli/
├── config/                # Threshold SLA, batas waktu & memori
├── docs/                  # Metodologi audit & baseline performa
├── src/
│   ├── auditors/          # time_auditor, memory_auditor, complexity_auditor
│   ├── harness/           # load_generator, scenario_runner
│   ├── reports/           # pdf_generator, json_exporter
│   └── ui/                # audit_dashboard, score_presenter
├── tests/                 # test_auditor_accuracy, test_sla_evaluator
├── main.py                # Entry point CLI
└── pyproject.toml
```

## Mengaudit Fungsi Anda Sendiri

Daftarkan fungsi baru di `TARGET_REGISTRY` pada `main.py`, lalu (opsional)
tambahkan aturan SLA khusus di `config/SLA_benchmarks.py`:

```python
SLA_REGISTRY["fungsi_saya"] = SLARule(
    max_time_ms=100, max_memory_mb=32, max_growth_class="O(N log N)"
)
```
