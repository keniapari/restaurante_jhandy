from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


SOURCE = Path(r"C:\Users\HP\Documents\PERFIL_TESIS_GRADO-Quinaya4.docx")
OUTPUT = Path(r"C:\laragon\www\control_emmafashion\documentos\PERFIL_TESIS_GRADO-Quinaya4_CORREGIDO_COMPLETO.docx")


def replace_paragraph_text(paragraph, text: str) -> None:
    for child in list(paragraph._p):
        if child.tag != qn("w:pPr"):
            paragraph._p.remove(child)
    paragraph.add_run(text)


def replace_cell_text(cell, text: str) -> None:
    paragraph = cell.paragraphs[0]
    replace_paragraph_text(paragraph, text)
    for extra in cell.paragraphs[1:]:
        replace_paragraph_text(extra, "")


def find_paragraph(document: Document, starts_with: str):
    for paragraph in document.paragraphs:
        if paragraph.text.strip().lower().startswith(starts_with.lower()):
            return paragraph
    raise ValueError(f"No se encontró el párrafo: {starts_with}")


def insert_after(reference, text: str):
    new_paragraph = deepcopy(reference._p)
    for child in list(new_paragraph):
        if child.tag != qn("w:pPr"):
            new_paragraph.remove(child)
    reference._p.addnext(new_paragraph)
    from docx.text.paragraph import Paragraph

    paragraph = Paragraph(new_paragraph, reference._parent)
    paragraph.add_run(text)
    return paragraph


def set_page_field(paragraph) -> None:
    for child in list(paragraph._p):
        if child.tag != qn("w:pPr"):
            paragraph._p.remove(child)

    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = " PAGE "
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instruction, separate, text, end])
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER


document = Document(SOURCE)
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# Sprint Backlog 3: HU-09 suma 1 día y HU-10 suma 10 días (total 11).
sprint_backlog_3 = document.tables[18]
new_times = ["0,5", "0,5", "2", "3", "3", "2"]
for row, time_value in zip(sprint_backlog_3.rows[1:], new_times, strict=True):
    replace_cell_text(row.cells[3], time_value)

# Sprint Review 3: dos casos rechazados que comprueban validaciones reales.
sprint_review_3 = document.tables[19]
replace_cell_text(
    sprint_review_3.rows[2].cells[2],
    "Nombre: María\nApellido: Pérez\nCI/NIT: 8343333\nTeléfono: 74534567\nCorreo: mario@gmail.com (correo ya registrado)\nDirección: Villa Dolores",
)
replace_cell_text(
    sprint_review_3.rows[2].cells[3],
    "El sistema rechaza la actualización e informa que el correo ya está registrado.",
)
replace_cell_text(sprint_review_3.rows[2].cells[4], "Rechazado")

replace_cell_text(
    sprint_review_3.rows[4].cells[3],
    "El sistema rechaza la venta e informa que la cantidad solicitada supera las existencias disponibles.",
)
replace_cell_text(sprint_review_3.rows[4].cells[4], "Rechazado")

# Notas y numeración correlativa de tablas y figuras.
replace_paragraph_text(
    [
        paragraph
        for paragraph in document.paragraphs
        if paragraph.text.strip().lower().startswith(
            "nota: la tabla muestra las tareas realizadas para el desarrollo de los módulos de proveedores y compras."
        )
    ][-1],
    "Nota: La tabla muestra las tareas realizadas para el desarrollo de los módulos de clientes y ventas.",
)
replace_paragraph_text(
    [
        paragraph
        for paragraph in document.paragraphs
        if paragraph.text.strip().startswith('Figura 23: Pruebas unitarias de caja blanca "Sprint 2"')
    ][-1],
    'Tabla 18: Pruebas unitarias de caja blanca "Sprint 2"',
)
replace_paragraph_text(
    [
        paragraph
        for paragraph in document.paragraphs
        if paragraph.text.strip().startswith("Tabla 19: Sprint Backlog 3")
    ][-1],
    "Tabla 19: Sprint Backlog 3",
)
replace_paragraph_text(
    [
        paragraph
        for paragraph in document.paragraphs
        if paragraph.text.strip().startswith('Tabla 20: Pruebas unitarias de caja blanca "Sprint 3"')
    ][-1],
    'Tabla 20: Pruebas unitarias de caja blanca "Sprint 3"',
)
replace_paragraph_text(
    find_paragraph(document, "Figura 24:Interfaz de registro de una venta"),
    "Figura 28: Interfaz de registro de una venta «Sprint 3»",
)
replace_paragraph_text(
    find_paragraph(document, "figura 26:Diagrama de casos de uso"),
    "Figura 29: Diagrama de casos de uso «Sprint 4»",
)
replace_paragraph_text(
    find_paragraph(document, "figura 27: Diagrama de clases"),
    "Figura 30: Diagrama de clases «Sprint 4»",
)
replace_paragraph_text(
    find_paragraph(document, "figura 28:Interfaz control de inventario"),
    "Figura 31: Interfaz de control de inventario «Sprint 4»",
)
replace_paragraph_text(
    find_paragraph(document, "Tabla 21: Sprint Backlog 4"),
    "Tabla 21: Sprint Backlog 4",
)
replace_paragraph_text(
    find_paragraph(document, "Tabla 21:Pruebas unitarias de caja blanca"),
    "Tabla 22: Pruebas unitarias de caja blanca «Sprint 4»",
)

# Eliminar las entradas antiguas 19 y 20 que quedaron desactualizadas.
for paragraph in list(document.paragraphs):
    if paragraph.style.name == "table of figures" and (
        paragraph.text.strip().startswith("Tabla 19:")
        or paragraph.text.strip().startswith("Tabla 20:")
    ):
        paragraph._element.getparent().remove(paragraph._element)

# Completar los índices de tablas y figuras sin modificar sus tablas o imágenes.
table_index_anchor = next(
    p for p in document.paragraphs if p.style.name == "table of figures" and p.text.strip().startswith("Tabla 17:")
)
inserted = insert_after(table_index_anchor, 'Tabla 18: Pruebas unitarias de caja blanca "Sprint 2"\t56')
inserted = insert_after(inserted, "Tabla 19: Sprint Backlog 3\t58")
inserted = insert_after(inserted, 'Tabla 20: Pruebas unitarias de caja blanca "Sprint 3"\t61')
inserted = insert_after(inserted, "Tabla 21: Sprint Backlog 4\t62")
insert_after(inserted, 'Tabla 22: Pruebas unitarias de caja blanca "Sprint 4"\t65')

figure_index_anchor = next(
    p for p in document.paragraphs if p.style.name == "table of figures" and p.text.strip().startswith("Figura 27:")
)
inserted = insert_after(figure_index_anchor, "Figura 28: Interfaz de registro de una venta «Sprint 3»\t60")
inserted = insert_after(inserted, "Figura 29: Diagrama de casos de uso «Sprint 4»\t64")
inserted = insert_after(inserted, "Figura 30: Diagrama de clases «Sprint 4»\t64")
insert_after(inserted, "Figura 31: Interfaz de control de inventario «Sprint 4»\t65")

# Campo PAGE real en cada pie de página y actualización de campos al abrir Word.
processed_footers: set[int] = set()
for section in document.sections:
    section.footer.is_linked_to_previous = False
    footer = section.footer
    footer_identity = id(footer._element)
    if footer_identity in processed_footers:
        continue
    processed_footers.add(footer_identity)
    for extra_paragraph in list(footer.paragraphs[1:]):
        extra_paragraph._element.getparent().remove(extra_paragraph._element)
    paragraph = footer.paragraphs[0]
    set_page_field(paragraph)

settings = document.settings._element
update_fields = settings.find(qn("w:updateFields"))
if update_fields is None:
    update_fields = OxmlElement("w:updateFields")
    settings.append(update_fields)
update_fields.set(qn("w:val"), "true")

document.save(OUTPUT)
print(OUTPUT)
