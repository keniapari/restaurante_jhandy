from pathlib import Path
from docx import Document

source = Path(r"C:\Users\HP\Documents\PERFIL_TESIS_GRADO-Quinaya4.docx")
document = Document(source)

print(f"paragraphs={len(document.paragraphs)} tables={len(document.tables)} sections={len(document.sections)}")

terms = [
    "SPRINT 3", "Sprint 3", "Tabla 18", "Tabla 19", "Tabla 20", "Tabla 21",
    "Figura 24", "Figura 25", "proveedores y compras", "DEDICATORIA",
    "AGRADECIMIENTO", "RESUMEN", "SPRINT 4", "Sprint 4",
]

for index, paragraph in enumerate(document.paragraphs):
    text = paragraph.text.strip()
    if text and any(term in text for term in terms):
        print(f"P{index} [{paragraph.style.name!r}] {text}")

for table_index, table in enumerate(document.tables):
    rows = []
    for row in table.rows:
        rows.append(" | ".join(cell.text.replace("\n", " / ").strip() for cell in row.cells))
    joined = "\n".join(rows)
    if any(term in joined for term in terms) or (15 <= table_index <= 24):
        print(f"\nTABLE {table_index} rows={len(table.rows)} cols={len(table.columns)}")
        print(joined[:8000])

for section_index, section in enumerate(document.sections):
    footer_text = " || ".join(p.text for p in section.footer.paragraphs)
    print(f"SECTION {section_index} footer={footer_text!r}")
