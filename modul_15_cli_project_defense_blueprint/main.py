#!/usr/bin/env python3
"""
main.py
--------
Entry Point (Defense Runner / Presentation Mode) untuk
modul_15_cli_project_defense_blueprint.

Perintah yang tersedia:
    --version                    Tampilkan splash screen & versi rilis
    dashboard                    Tampilkan defense dashboard (ringkasan fitur)
    demo --scenario <nama>       Jalankan skenario demo otomatis
    build --target executable    Build executable via PyInstaller (dry-run aman)
    build --target docker        Build Docker image (dry-run aman)
    docs generate                Ekstrak docstring -> Markdown
    docs slides                  Cetak slide deck ringkasan audit
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from config.release_settings import DEFAULT_RELEASE  # noqa: E402
from config.demo_scenarios import get_scenario  # noqa: E402
from src.ui.splash_screen import show_splash  # noqa: E402
from src.ui.defense_dashboard import render_dashboard  # noqa: E402
from src.simulator.scenario_runner import run_scenario  # noqa: E402
from src.packager.pyinstaller_build import run_build  # noqa: E402
from src.packager.docker_manager import build_image  # noqa: E402
from src.generator.doc_generator import generate as generate_docs  # noqa: E402
from src.generator.slide_deck_builder import build_deck, AuditMetric  # noqa: E402


def cmd_dashboard(_args) -> None:
    print(render_dashboard())


def cmd_demo(args) -> None:
    scenario = get_scenario(args.scenario)
    run_scenario(scenario, speed=args.speed, verbose=True)


def cmd_build(args) -> None:
    if args.target == "executable":
        report = run_build(dry_run=args.dry_run)
    elif args.target == "docker":
        report = build_image(dry_run=args.dry_run)
    else:
        raise SystemExit(f"Target build tidak dikenal: {args.target}")

    print(f"[build:{args.target}]")
    for k, v in report.items():
        print(f"  {k}: {v}")


def cmd_docs(args) -> None:
    root = Path(__file__).resolve().parent
    if args.docs_action == "generate":
        out = generate_docs(root, root / "docs" / "GENERATED_CODE_DOCS.md")
        print(f"Dokumentasi kode ditulis ke: {out}")
    elif args.docs_action == "slides":
        sample_metrics = [
            AuditMetric("binary_search", 0.02, 0.5, "O(log N)", "PASS"),
            AuditMetric("quick_sort", 3.1, 1.0, "O(N log N)", "PASS"),
            AuditMetric("hash_lookup", 0.005, 0.3, "O(1)", "PASS"),
        ]
        deck = build_deck(DEFAULT_RELEASE.app_name, DEFAULT_RELEASE.version,
                           DEFAULT_RELEASE.author, sample_metrics)
        print(deck)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="app",
        description="CLI Project Defense Suite - Modul 15",
    )
    parser.add_argument("--version", action="store_true",
                         help="Tampilkan splash screen & informasi versi")

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("dashboard", help="Tampilkan defense dashboard").set_defaults(func=cmd_dashboard)

    demo_p = sub.add_parser("demo", help="Jalankan skenario demo otomatis")
    demo_p.add_argument("--scenario", default="quick_tour",
                         choices=["quick_tour", "full_defense"])
    demo_p.add_argument("--speed", type=float, default=0.02,
                         help="Kecepatan ketik simulasi (detik/karakter)")
    demo_p.set_defaults(func=cmd_demo)

    build_p = sub.add_parser("build", help="Build artefak rilis")
    build_p.add_argument("--target", choices=["executable", "docker"], required=True)
    build_p.add_argument("--dry-run", action="store_true", default=True,
                          help="Jangan benar-benar mengeksekusi build (default aktif)")
    build_p.set_defaults(func=cmd_build)

    docs_p = sub.add_parser("docs", help="Generate dokumentasi / slide")
    docs_p.add_argument("docs_action", choices=["generate", "slides"])
    docs_p.set_defaults(func=cmd_docs)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.version or not args.command:
        show_splash(DEFAULT_RELEASE)
        if not args.command:
            parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
