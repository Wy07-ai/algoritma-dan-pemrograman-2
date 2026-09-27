"""
src/reports/pdf_generator.py
------------------------------
Pembuat laporan audit resmi dalam format PDF, berstandar dokumen
teknis: ringkasan, tabel per-fungsi (waktu/memori/Big-O/status SLA).
Menggunakan `reportlab`. Jika tidak tersedia, otomatis fallback
menulis laporan sebagai Markdown biasa.
"""

import os
from datetime import datetime, timezone
from typing import Any, Dict

from config import settings

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
    )
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class PDFReportGenerator:
    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or settings.REPORTS_OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, audit_data: Dict[str, Any], filename: str = None) -> str:
        if filename is None:
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            filename = f"audit_report_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)

        if REPORTLAB_AVAILABLE:
            self._generate_pdf(audit_data, filepath)
        else:
            filepath = filepath.replace(".pdf", ".md")
            self._generate_markdown_fallback(audit_data, filepath)

        return filepath

    # -- Implementasi PDF sesungguhnya --------------------------------
    def _generate_pdf(self, audit_data: Dict[str, Any], filepath: str) -> None:
        doc = SimpleDocTemplate(filepath, pagesize=A4,
                                 leftMargin=2 * cm, rightMargin=2 * cm,
                                 topMargin=2 * cm, bottomMargin=2 * cm)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph(f"Laporan Audit — {settings.APP_NAME}", styles["Title"]))
        story.append(Paragraph(
            f"Versi {settings.APP_VERSION} • Dibuat: "
            f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
            styles["Normal"],
        ))
        story.append(Spacer(1, 0.5 * cm))

        for func_name, scenarios in audit_data.items():
            story.append(Paragraph(f"Fungsi: {func_name}", styles["Heading2"]))

            table_data = [["Skenario", "N", "Waktu Rata2 (ms)", "Peak Memori (MB)", "Big-O Estimasi", "Status SLA"]]
            for scenario_name, report in scenarios.items():
                for row in report.get("per_n_results", []):
                    table_data.append([
                        scenario_name,
                        str(row["n"]),
                        f"{row['time']['mean_ms']:.3f}",
                        f"{row['memory']['peak_mb']:.3f}",
                        report.get("complexity_fit", {}).get("best_fit", "-"),
                        report.get("sla_result", {}).get("status", "-"),
                    ])

            table = Table(table_data, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2b2d42")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
            ]))
            story.append(table)
            story.append(Spacer(1, 0.7 * cm))

        doc.build(story)

    # -- Fallback jika reportlab tidak ada -----------------------------
    def _generate_markdown_fallback(self, audit_data: Dict[str, Any], filepath: str) -> None:
        lines = [f"# Laporan Audit — {settings.APP_NAME}\n",
                 f"Versi {settings.APP_VERSION} • Dibuat: "
                 f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n"]
        for func_name, scenarios in audit_data.items():
            lines.append(f"\n## Fungsi: {func_name}\n")
            lines.append("| Skenario | N | Waktu Rata2 (ms) | Peak Memori (MB) | Big-O | Status |")
            lines.append("|---|---|---|---|---|---|")
            for scenario_name, report in scenarios.items():
                for row in report.get("per_n_results", []):
                    lines.append(
                        f"| {scenario_name} | {row['n']} | {row['time']['mean_ms']:.3f} "
                        f"| {row['memory']['peak_mb']:.3f} "
                        f"| {report.get('complexity_fit', {}).get('best_fit', '-')} "
                        f"| {report.get('sla_result', {}).get('status', '-')} |"
                    )
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


if __name__ == "__main__":
    demo_data = {
        "linear_search": {
            "average_case": {
                "per_n_results": [
                    {"n": 100, "time": {"mean_ms": 0.01}, "memory": {"peak_mb": 0.01}},
                    {"n": 10_000, "time": {"mean_ms": 1.2}, "memory": {"peak_mb": 0.5}},
                ],
                "complexity_fit": {"best_fit": "O(N)"},
                "sla_result": {"status": "PASS"},
            }
        }
    }
    gen = PDFReportGenerator(output_dir="/tmp/audit_reports_demo")
    print("Laporan tersimpan di:", gen.generate(demo_data))
