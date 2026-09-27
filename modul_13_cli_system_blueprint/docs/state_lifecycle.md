# State Lifecycle — Modul 13: CLI System Blueprint

## Diagram Alur: Init → Run → Terminate

```
   ┌────────┐        boot()        ┌────────┐      shutdown() /       ┌────────────┐
   │  INIT  │ ────────────────────▶│  RUN   │ ─── SIGINT / normal ───▶│ TERMINATED │
   └────────┘                      └────────┘        exit             └────────────┘
        │                               │
        │ - load settings               │ - eksekusi command
        │ - connect & migrate DB        │ - session.touch(command)
        │ - init repository/cache       │ - cache read-through
        │ - session.start()             │
        │ - install signal handler      │
```

## Rincian Tiap Fase

### 1. INIT
- `Kernel.boot()` dipanggil sekali di awal proses `main.py`.
- Konfigurasi dimuat dari `.env` (jika ada) via `config/settings.py`.
- `LocalDB.connect()` membuka koneksi SQLite dan `migrate()` memastikan
  skema tabel `entities` tersedia (idempotent — aman dipanggil berkali-kali).
- `SessionManager.start()` memuat sesi lama (jika masih berada dalam TTL)
  atau membuat sesi baru dengan `session_id` unik.
- `SignalHandler.install()` mendaftarkan handler untuk `SIGINT`/`SIGTERM`.

### 2. RUN
- Command yang dipilih user (`add`, `list`, `get`, `update`, `delete`,
  `export`, `sync`, `status`) dieksekusi lewat service layer terkait.
- Setiap command yang berhasil dijalankan mencatat jejaknya lewat
  `SessionManager.touch(command_name)`.
- Jika proses menerima `Ctrl+C` di tengah eksekusi, `SignalHandler`
  langsung memanggil `Kernel.shutdown()` sebelum proses benar-benar mati.

### 3. TERMINATE
- Dipicu baik oleh alur normal (`finally: kernel.shutdown()` di `main.py`)
  maupun oleh sinyal OS.
- Urutan graceful shutdown:
  1. `SessionManager.end()` — menandai waktu sesi berakhir & menyimpan state.
  2. `Repository.flush()` — memastikan seluruh transaksi SQLite ter-commit.
  3. `CacheStore.clear()` — mengosongkan cache di RAM.
- Proses baru benar-benar keluar (`sys.exit`) setelah ketiga langkah di atas
  selesai, sehingga data tidak korup meski aplikasi dihentikan paksa.
