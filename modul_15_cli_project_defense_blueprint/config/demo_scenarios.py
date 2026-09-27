"""
demo_scenarios.py
------------------
Skenario alur demonstrasi interaktif yang dipakai oleh Live Demo Simulator
(src/simulator/) saat sesi presentasi / sidang proyek berlangsung.

Setiap skenario adalah daftar langkah: perintah yang "diketik" otomatis
di terminal beserta narasi singkat yang ditampilkan sebelum eksekusi.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class DemoStep:
    narration: str      # Penjelasan singkat sebelum langkah dijalankan
    command: str         # Perintah CLI yang disimulasikan diketik
    delay_after: float = 1.0   # Jeda (detik) setelah langkah selesai


@dataclass
class DemoScenario:
    name: str
    description: str
    steps: List[DemoStep]


SCENARIO_QUICK_TOUR = DemoScenario(
    name="quick_tour",
    description="Tur singkat menampilkan fitur utama aplikasi CLI.",
    steps=[
        DemoStep("Menampilkan bantuan umum aplikasi", "app --help"),
        DemoStep("Menjalankan modul pencarian data", "app search --query demo"),
        DemoStep("Menjalankan modul pengurutan data", "app sort --algo quicksort"),
        DemoStep("Menampilkan ringkasan audit performa", "app audit --report"),
    ],
)

SCENARIO_FULL_DEFENSE = DemoScenario(
    name="full_defense",
    description="Skenario lengkap A-Z untuk sesi sidang/defense.",
    steps=[
        DemoStep("Menampilkan splash screen aplikasi", "app --version"),
        DemoStep("Memuat konfigurasi sistem", "app config show"),
        DemoStep("Menjalankan pipeline data end-to-end", "app pipeline run --sample big"),
        DemoStep("Menampilkan hasil audit kompleksitas Big-O", "app audit --complexity"),
        DemoStep("Mengekspor laporan hasil sidang ke PDF", "app report export --format pdf"),
        DemoStep("Menutup aplikasi secara graceful", "app shutdown"),
    ],
)

ALL_SCENARIOS = {
    SCENARIO_QUICK_TOUR.name: SCENARIO_QUICK_TOUR,
    SCENARIO_FULL_DEFENSE.name: SCENARIO_FULL_DEFENSE,
}


def get_scenario(name: str) -> DemoScenario:
    if name not in ALL_SCENARIOS:
        raise KeyError(
            f"Skenario '{name}' tidak ditemukan. "
            f"Pilihan tersedia: {list(ALL_SCENARIOS.keys())}"
        )
    return ALL_SCENARIOS[name]
