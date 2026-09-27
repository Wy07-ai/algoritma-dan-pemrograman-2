"""
config/settings.py
-------------------
Memuat konfigurasi environment untuk sistem Audit Kompleksitas.
Semua nilai bisa di-override lewat environment variable (.env),
agar tidak ada nilai yang hardcoded secara tersembunyi.
"""

import os

# --- Threshold waktu eksekusi (dalam milidetik) ---
MAX_EXECUTION_TIME_MS = float(os.getenv("AUDIT_MAX_TIME_MS", 500))

# --- Batas alokasi memori (dalam megabyte) ---
MAX_MEMORY_MB = float(os.getenv("AUDIT_MAX_MEMORY_MB", 128))

# --- Skala N default yang diuji oleh harness ---
DEFAULT_N_SCALES = [100, 1_000, 10_000, 100_000, 1_000_000]

# --- Jumlah pengulangan (repetisi) tiap pengukuran agar hasil stabil ---
REPEAT_COUNT = int(os.getenv("AUDIT_REPEAT_COUNT", 5))

# --- Toleransi deteksi memory leak (kenaikan memori antar-iterasi, dalam MB) ---
MEMORY_LEAK_TOLERANCE_MB = float(os.getenv("AUDIT_LEAK_TOLERANCE_MB", 1.0))

# --- Direktori keluaran laporan ---
REPORTS_OUTPUT_DIR = os.getenv("AUDIT_REPORTS_DIR", "audit_reports")

# --- Nama & versi aplikasi (dipakai di laporan) ---
APP_NAME = "Audit Kompleksitas Sistem CLI"
APP_VERSION = "1.0.0"
