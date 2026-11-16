from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.shared import Inches


ROOT = Path(r"C:\Users\HP\.codex\visualizations\2026\07\28\019faabb-03f0-7721-a83a-520605149e89")
DOCX = ROOT / "PERFIL_TESIS_GRADO_Quinaya4_CORREGIDO.docx"
QA = ROOT / "revision-tesis"


def highlight(paragraph):
    for run in paragraph.runs:
        run.font.highlight_color = WD_COLOR_INDEX.YELLOW


def insert_image_before(paragraph, image_path):
    new_p = paragraph._parent.add_paragraph()
    paragraph._p.addprevious(new_p._p)
    new_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    new_p.paragraph_format.keep_with_next = True
    run = new_p.add_run()
    run.add_picture(str(image_path), width=Inches(6.8))


doc = Document(DOCX)
for p in doc.paragraphs:
    text = p.text.strip()
    if text == "CAPITULO III":
        p.paragraph_format.page_break_before = True
        p.paragraph_format.keep_with_next = True
    if text == "PROPUESTA DE INNOVACIÓN O SOLUCIÓN AL PROBLEMA":
        p.paragraph_format.keep_with_next = True
    if text in {"3.3.1 Ejecución del primer Sprint 1", "3.3.1 Ejecución del Sprint 1"}:
        p.text = "3.3 Ejecución del Sprint 1"
        p.style = "Heading 2"
        highlight(p)
    if text.startswith("Figura 9."):
        insert_image_before(p, QA / "diagrama-casos-uso-sprint-1-corregido.png")
    if text.startswith("Figura 18."):
        insert_image_before(p, QA / "diagrama-casos-uso-sprint-2-corregido.png")
    if text.startswith("Nota. El diagrama representa las acciones que el dueño del negocio"):
        p.text = ("Nota. El diagrama representa las funciones que la administradora puede realizar "
                  "en la gestión de proveedores y compras, incluyendo registrar, consultar, editar, "
                  "anular, imprimir comprobantes y actualizar o revertir el inventario.")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        highlight(p)

doc.save(DOCX)
print(DOCX)
