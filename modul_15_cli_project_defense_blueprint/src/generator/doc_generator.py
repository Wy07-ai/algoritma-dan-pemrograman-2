"""
doc_generator.py
-----------------
Mengekstrak docstring dari seluruh modul Python dalam proyek dan
menyusunnya menjadi dokumentasi terformat Markdown secara otomatis.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ModuleDoc:
    path: Path
    module_doc: str | None
    functions: list[tuple[str, str | None]] = field(default_factory=list)
    classes: list[tuple[str, str | None]] = field(default_factory=list)


def extract_module_doc(file_path: Path) -> ModuleDoc:
    """Membaca satu file .py dan mengekstrak docstring module/class/function."""
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))

    module_doc = ast.get_docstring(tree)
    functions, classes = [], []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.col_offset == 0:
            functions.append((node.name, ast.get_docstring(node)))
        elif isinstance(node, ast.ClassDef):
            classes.append((node.name, ast.get_docstring(node)))

    return ModuleDoc(path=file_path, module_doc=module_doc,
                      functions=functions, classes=classes)


def scan_project(src_dir: Path) -> list[ModuleDoc]:
    """Memindai seluruh berkas .py di bawah `src_dir` (rekursif)."""
    docs = []
    for py_file in sorted(src_dir.rglob("*.py")):
        if py_file.name == "__init__.py":
            continue
        try:
            docs.append(extract_module_doc(py_file))
        except SyntaxError:
            continue
    return docs


def render_markdown(docs: list[ModuleDoc], project_root: Path) -> str:
    """Merender daftar ModuleDoc menjadi satu dokumen Markdown."""
    lines = ["# Dokumentasi Kode Otomatis", ""]
    for doc in docs:
        rel = doc.path.relative_to(project_root)
        lines.append(f"## `{rel}`")
        if doc.module_doc:
            lines.append(doc.module_doc.strip())
        lines.append("")

        if doc.classes:
            lines.append("**Kelas:**")
            for name, cdoc in doc.classes:
                summary = (cdoc or "Tidak ada deskripsi.").strip().splitlines()[0]
                lines.append(f"- `{name}` — {summary}")
            lines.append("")

        if doc.functions:
            lines.append("**Fungsi:**")
            for name, fdoc in doc.functions:
                summary = (fdoc or "Tidak ada deskripsi.").strip().splitlines()[0]
                lines.append(f"- `{name}()` — {summary}")
            lines.append("")

    return "\n".join(lines)


def generate(project_root: Path, output_path: Path) -> Path:
    src_dir = project_root / "src"
    docs = scan_project(src_dir)
    markdown = render_markdown(docs, project_root)
    output_path.write_text(markdown, encoding="utf-8")
    return output_path


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    out = generate(root, root / "docs" / "GENERATED_CODE_DOCS.md")
    print(f"[doc_generator] Dokumentasi ditulis ke: {out}")
