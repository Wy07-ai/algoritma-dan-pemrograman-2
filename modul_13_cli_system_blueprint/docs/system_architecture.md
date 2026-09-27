# System Architecture — Modul 13: CLI System Blueprint

## Diagram Blok Komponen Internal

```
                        ┌───────────────────────┐
                        │        main.py         │
                        │   (Kernel Executor)     │
                        └───────────┬─────────────┘
                                    │ boot()
                                    ▼
                        ┌───────────────────────┐
                        │   src/system/kernel.py  │
                        │  (Bootstrapper Utama)   │
                        └───┬───────┬────────┬────┘
                            │       │        │
             ┌──────────────┘       │        └──────────────┐
             ▼                      ▼                        ▼
 ┌────────────────────┐ ┌────────────────────┐ ┌───────────────────────┐
 │ session_manager.py  │ │ signal_handler.py   │ │ storage/repository.py │
 │ (Status Sesi)        │ │ (Graceful Shutdown)  │ │ (Abstraksi Storage)    │
 └────────────────────┘ └────────────────────┘ └───────────┬────────────┘
                                                             │
                                              ┌──────────────┴───────────────┐
                                              ▼                              ▼
                                  ┌────────────────────┐      ┌────────────────────┐
                                  │ storage/local_db.py │      │ storage/cache_store │
                                  │ (SQLite persistence)│      │ (In-memory LRU)      │
                                  └────────────────────┘      └────────────────────┘

                        ┌───────────────────────────────────┐
                        │        src/services/*.py            │
                        │  data_service | export_service |     │
                        │  sync_service                        │
                        └───────────────┬───────────────────┘
                                        │
                                        ▼
                        ┌───────────────────────────────────┐
                        │       src/ui_engine/*.py             │
                        │  view_router.py | status_bar.py      │
                        └───────────────────────────────────┘
```

## Alur Kerja Singkat

1. `main.py` mem-parsing argumen CLI, lalu memanggil `Kernel.boot()`.
2. `Kernel` memuat `config/settings.py` & `config/database_config.py`,
   menginisialisasi `LocalDB`, `Repository`, `CacheStore`, dan `SessionManager`,
   kemudian memasang `SignalHandler` agar Ctrl+C tidak merusak data.
3. Command handler di `main.py` memanggil service yang relevan
   (`DataService`, `ExportService`, `SyncService`).
4. Hasil dari service diformat oleh `ViewRouter` / `StatusBar` sebelum
   ditampilkan ke terminal.
5. Saat proses berakhir (baik normal maupun karena sinyal OS),
   `Kernel.shutdown()` memastikan `Repository.flush()` dan penutupan
   sesi berjalan sebelum aplikasi benar-benar keluar.

## Prinsip Desain

- **Separation of Concerns**: `services/` tidak pernah mengimpor `local_db.py`
  secara langsung — semua akses data lewat `repository.py`.
- **Graceful Shutdown**: seluruh state (session, cache, database) memiliki
  jalur "commit" eksplisit yang dipanggil di `Kernel.shutdown()`.
- **Config Terpusat**: semua nilai ambang batas/nama file berada di
  `config/settings.py` dan `config/database_config.py`, tidak hardcoded.
