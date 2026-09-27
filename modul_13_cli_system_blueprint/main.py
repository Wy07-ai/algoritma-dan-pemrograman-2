#!/usr/bin/env python3
"""
main.py
--------
Entry Point Utama (Kernel Executor).

Contoh penggunaan:
    python main.py add "Beli buku" --desc "Untuk kuliah Algo2"
    python main.py list
    python main.py get 1
    python main.py update 1 --name "Beli buku baru"
    python main.py delete 1
    python main.py export --format json --out data/export.json
    python main.py sync
    python main.py status
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from config.settings import settings
from src.services.data_service import DataService
from src.services.export_service import ExportService
from src.services.sync_service import SyncService
from src.system.kernel import Kernel
from src.ui_engine.status_bar import StatusBar
from src.ui_engine.view_router import ViewRouter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=settings.app_name,
        description="Modul 13: CLI System Blueprint - Full-Stack CLI System",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Tambah item baru")
    p_add.add_argument("name", type=str)
    p_add.add_argument("--desc", type=str, default="")

    p_get = sub.add_parser("get", help="Ambil satu item berdasarkan ID")
    p_get.add_argument("id", type=int)

    sub.add_parser("list", help="Tampilkan semua item")

    p_update = sub.add_parser("update", help="Perbarui item")
    p_update.add_argument("id", type=int)
    p_update.add_argument("--name", type=str, default=None)
    p_update.add_argument("--desc", type=str, default=None)

    p_delete = sub.add_parser("delete", help="Hapus item")
    p_delete.add_argument("id", type=int)

    p_export = sub.add_parser("export", help="Ekspor semua item ke berkas")
    p_export.add_argument("--format", choices=["json", "csv"], default="json")
    p_export.add_argument("--out", type=str, default=None)

    sub.add_parser("sync", help="Sinkronisasi data ke snapshot lokal")
    sub.add_parser("status", help="Tampilkan status sistem & sesi aktif")

    return parser


def run(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    kernel = Kernel()
    ctx = kernel.boot()

    data_service = DataService(ctx.repository, ctx.cache)
    export_service = ExportService()
    sync_service = SyncService(settings.data_dir / "sync")
    view = ViewRouter()
    status_bar = StatusBar(settings.app_name, settings.app_version)

    exit_code = 0
    try:
        if args.command == "add":
            item = data_service.create_item(args.name, args.desc)
            print(view.render_message(f"Item dibuat dengan id={item['id']}"))
            print(view.render_item(item))

        elif args.command == "get":
            item = data_service.get_item(args.id)
            print(view.render_item(item) if item else view.render_message("Item tidak ditemukan", ok=False))

        elif args.command == "list":
            items = data_service.list_items()
            print(view.render_item_list(items))

        elif args.command == "update":
            ok = data_service.update_item(args.id, name=args.name, description=args.desc)
            print(view.render_message(f"Item id={args.id} diperbarui" if ok else f"Item id={args.id} tidak ditemukan", ok=ok))

        elif args.command == "delete":
            ok = data_service.delete_item(args.id)
            print(view.render_message(f"Item id={args.id} dihapus" if ok else f"Item id={args.id} tidak ditemukan", ok=ok))

        elif args.command == "export":
            items = data_service.list_items()
            out_path = Path(args.out) if args.out else settings.data_dir / f"export.{args.format}"
            if args.format == "json":
                path = export_service.export_to_json(items, out_path)
            else:
                path = export_service.export_to_csv(items, out_path)
            print(view.render_message(f"{len(items)} item diekspor ke {path}"))

        elif args.command == "sync":
            items = data_service.list_items()
            result = sync_service.sync(items)
            print(view.render_message(f"Sinkronisasi selesai: {result['item_count']} item"))

        elif args.command == "status":
            print(status_bar.render(ctx.session.state))

        ctx.session.touch(args.command)

    except ValueError as exc:
        print(view.render_message(str(exc), ok=False))
        exit_code = 1
    finally:
        kernel.shutdown()

    return exit_code


if __name__ == "__main__":
    sys.exit(run())
