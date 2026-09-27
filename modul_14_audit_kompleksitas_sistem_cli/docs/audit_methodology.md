# Metodologi Audit Kompleksitas Sistem CLI

## 1. Tujuan
Memverifikasi secara empiris bahwa kompleksitas waktu dan ruang suatu
fungsi sesuai dengan estimasi teoritis (Big-O), serta memastikan fungsi
tersebut memenuhi Service Level Agreement (SLA) yang ditetapkan.

## 2. Pendekatan: Empirical vs Theoretical Big-O

| Aspek        | Theoretical Big-O                     | Empirical Big-O (audit ini)              |
|--------------|-----------------------------------------|-------------------------------------------|
| Sumber       | Analisis manual kode/algoritma          | Hasil pengukuran nyata (`time.perf_counter`, `tracemalloc`) |
| Akurasi      | Ideal, mengabaikan konstanta            | Dipengaruhi hardware, cache, GC           |
| Kegunaan     | Dasar desain algoritma                  | Validasi implementasi & deteksi regresi   |

Audit ini menjalankan setiap fungsi target pada beberapa skala `N`
(`load_generator.py`), mencatat waktu & memori (`time_auditor.py`,
`memory_auditor.py`), lalu mencocokkan pertumbuhan hasil pengukuran
terhadap kurva Big-O kandidat menggunakan regresi log-log
(`complexity_auditor.py`).

## 3. Tahapan Audit

1. **Load Generation** — menghasilkan data uji pada skala `N` yang
   bertambah (default: 100 → 1.000.000).
2. **Scenario Execution** — menjalankan fungsi pada kondisi *Best
   Case*, *Average Case*, dan *Worst Case*.
3. **Measurement** — mencatat waktu eksekusi (mikrodetik) dan puncak
   penggunaan memori (`tracemalloc`).
4. **Curve Fitting** — mengestimasi kelas kompleksitas yang paling
   cocok dengan data empiris.
5. **SLA Evaluation** — membandingkan hasil terhadap ambang batas di
   `config/SLA_benchmarks.py` dan menentukan status Lulus/Gagal.
6. **Reporting** — mengekspor hasil ke PDF/Markdown/JSON dan
   menampilkannya di dashboard CLI.

## 4. Deteksi Memory Leak

Fungsi dijalankan berulang kali (`REPEAT_COUNT`) pada `N` yang sama.
Jika puncak memori terus naik secara konsisten melebihi
`MEMORY_LEAK_TOLERANCE_MB` antar-iterasi, fungsi ditandai berpotensi
mengalami *memory leak*.

## 5. Kriteria Lulus/Gagal

Suatu fungsi dinyatakan **PASS** hanya jika ketiga kriteria berikut
terpenuhi secara bersamaan:

- Waktu eksekusi ≤ `max_time_ms`
- Puncak memori ≤ `max_memory_mb`
- Kelas kompleksitas empiris tidak lebih buruk dari `max_growth_class`
