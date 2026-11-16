from __future__ import annotations

import sys
from pathlib import Path
from zipfile import ZipFile

from docx import Document


def clean(text: str) -> str:
    return " ".join(text.replace("\u00a0", " ").split())


def main(path: str) -> None:
    source = Path(path)
    doc = Document(source)
    print(f"FILE: {source.name}")
    print(f"PARAGRAPHS: {len(doc.paragraphs)} TABLES: {len(doc.tables)}")

    print("\n=== OUTLINE / RELEVANT PARAGRAPHS ===")
    keywords = (
        "capítulo iii", "capitulo iii", "sprint", "retrospectiva",
        "trazabilidad", "alcance", "exclusiones", "base de datos",
        "reglas del negocio", "pruebas", "figura", "tabla",
    )
    for index, paragraph in enumerate(doc.paragraphs):
        text = clean(paragraph.text)
        style = paragraph.style.name if paragraph.style else ""
        if text and (style.lower().startswith("heading") or style.lower().startswith("título") or any(k in text.lower() for k in keywords)):
            print(f"P{index:04d} [{style}] {text}")

    print("\n=== TABLE SUMMARIES ===")
    for table_index, table in enumerate(doc.tables, start=1):
        rows = []
        for row in table.rows:
            cells = [clean(cell.text) for cell in row.cells]
            rows.append(" | ".join(cells))
        joined = " || ".join(rows)
        if any(k in joined.lower() for k in ("sprint", "historia", "resultado", "retrospectiva", "trazabilidad", "alcance", "modelo", "días", "dias")):
            print(f"\nTABLE {table_index} ({len(table.rows)}x{len(table.columns)})")
            for row in rows[:20]:
                print(row)
            if len(rows) > 20:
                print(f"... {len(rows) - 20} more rows")

    with ZipFile(source) as archive:
        names = set(archive.namelist())
        print("\n=== STRUCTURE ===")
        print("comments:", "word/comments.xml" in names)
        print("footnotes:", "word/footnotes.xml" in names)
        print("endnotes:", "word/endnotes.xml" in names)


if __name__ == "__main__":
    main(sys.argv[1])
