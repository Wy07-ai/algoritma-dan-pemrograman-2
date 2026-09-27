"""
main.py
--------
Entry Point Utama (CLI Audit Runner) untuk Modul 14: Audit Kompleksitas
Sistem CLI.

Contoh pemakaian:
    python main.py --functions linear_search binary_search bubble_sort quick_sort
    python main.py --functions quick_sort --scales 100 1000 10000 --repeat 3
    python main.py --functions linear_search --export json pdf
"""

import argparse
import sys

from config import settings
from src.harness.scenario_runner import SCENARIOS, ScenarioRunner
from src.reports.json_exporter import JSONExporter
from src.reports.pdf_generator import PDFReportGenerator
from src.ui.audit_dashboard import AuditDashboard

# ---------------------------------------------------------------------
# Fungsi target contoh (mewakili implementasi dari Modul 05 & 06).
# Dalam proyek nyata, fungsi-fungsi ini diimpor dari modul terkait;
# di sini disertakan versi ringkas agar audit dapat dijalankan mandiri.
# ---------------------------------------------------------------------

def linear_search(data, target=-1):
    for i, v in enumerate(data):
        if v == target:
            return i
    return -1


def binary_search(data, target=-1):
    sorted_data = sorted(data)
    lo, hi = 0, len(sorted_data) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_data[mid] == target:
            return mid
        elif sorted_data[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def bubble_sort(data):
    arr = list(data)
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def quick_sort(data):
    arr = list(data)
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)


TARGET_REGISTRY = {
    "linear_search": linear_search,
    "binary_search": binary_search,
    "bubble_sort": bubble_sort,
    "quick_sort": quick_sort,
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Audit Kompleksitas Sistem CLI — jalankan audit performa & SLA."
    )
    parser.add_argument(
        "--functions", nargs="+", choices=list(TARGET_REGISTRY.keys()),
        default=list(TARGET_REGISTRY.keys()),
        help="Fungsi yang akan diaudit (default: semua).",
    )
    parser.add_argument(
        "--scenarios", nargs="+", choices=list(SCENARIOS.keys()),
        default=list(SCENARIOS.keys()),
        help="Skenario yang dijalankan (default: semua).",
    )
    parser.add_argument(
        "--scales", nargs="+", type=int, default=None,
        help="Skala N kustom, contoh: --scales 100 1000 10000",
    )
    parser.add_argument(
        "--repeat", type=int, default=None,
        help=f"Jumlah repetisi pengukuran (default: {settings.REPEAT_COUNT}).",
    )
    parser.add_argument(
        "--export", nargs="*", choices=["json", "pdf"], default=[],
        help="Format ekspor laporan setelah audit selesai.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    targets = {name: TARGET_REGISTRY[name] for name in args.functions}
    runner = ScenarioRunner(n_scales=args.scales, repeat=args.repeat)
    dashboard = AuditDashboard(runner=runner)

    results = dashboard.run(targets, scenarios=args.scenarios)

    # Konversi hasil ke dict murni untuk keperluan ekspor
    exportable = {
        func_name: {scenario: report.to_dict() for scenario, report in scenarios.items()}
        for func_name, scenarios in results.items()
    }

    if "json" in args.export:
        path = JSONExporter().export(exportable)
        print(f"\nLaporan JSON tersimpan di: {path}")

    if "pdf" in args.export:
        path = PDFReportGenerator().generate(exportable)
        print(f"Laporan PDF tersimpan di: {path}")

    # Exit code non-zero jika ada fungsi yang gagal SLA di skenario manapun
    any_fail = any(
        report.sla_result["status"] == "FAIL"
        for scenarios in results.values()
        for report in scenarios.values()
    )
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
