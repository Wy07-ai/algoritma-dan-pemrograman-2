# Baseline Performa per Fungsi

Baseline ini adalah acuan awal yang dipakai `complexity_auditor.py`
untuk membandingkan tren pertumbuhan waktu terhadap kelas Big-O.

| Fungsi          | Big-O Target | Maks. Waktu (ms) | Maks. Memori (MB) |
|-----------------|--------------|-------------------|---------------------|
| linear_search   | O(N)         | 200               | 64                  |
| binary_search   | O(log N)     | 50                | 32                  |
| bubble_sort     | O(N^2)       | 2000              | 64                  |
| quick_sort      | O(N log N)   | 300               | 64                  |
| (default)       | O(N log N)   | lihat `settings.py` | lihat `settings.py` |

Baseline ini bersifat konfigurasi (bukan hardcoded di kode audit) dan
dapat diperbarui melalui `config/SLA_benchmarks.py` seiring perubahan
target performa sistem.

> Catatan: baseline waktu absolut sangat bergantung pada spesifikasi
> mesin penguji. Yang paling penting untuk divalidasi audit ini adalah
> **bentuk kurva pertumbuhan** (rasio waktu terhadap kenaikan N), bukan
> semata-mata angka absolutnya.
