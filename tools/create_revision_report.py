from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor


OUTPUT = Path(r"C:\laragon\www\control_emmafashion\documento_corregido\Revision_observaciones_Capitulo_III.docx")


def shade_cell(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=100, start=120, bottom=100, end=120):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def add_pending(doc, title, finding, correction):
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(8)
    paragraph.paragraph_format.space_after = Pt(3)
    label = paragraph.add_run("PENDIENTE  ")
    label.bold = True
    label.font.highlight_color = 7
    title_run = paragraph.add_run(title)
    title_run.bold = True

    paragraph = doc.add_paragraph(finding)
    paragraph.paragraph_format.space_after = Pt(3)
    paragraph = doc.add_paragraph()
    lead = paragraph.add_run("Corrección recomendada: ")
    lead.bold = True
    paragraph.add_run(correction)
    paragraph.paragraph_format.space_after = Pt(7)


def add_status_table(doc):
    rows = [
        ("Totales de los Sprint Backlog", "CORREGIDO", "18 + 8 + 11 + 14 = 51 días."),
        ("Tarea duplicada de usuarios", "CORREGIDO", "Ya no se repite la activación y desactivación."),
        ("Título caja negra", "PARCIAL", "Los títulos están corregidos, pero la nota del Sprint 1 todavía dice caja blanca."),
        ("Casos rechazados", "PENDIENTE", "Solo el Sprint 4 tiene dos; faltan dos en los Sprint 1, 2 y 3."),
        ("Datos personales de prueba", "PENDIENTE", "Aún aparecen un correo personal y una contraseña real."),
        ("Numeración de figuras", "PENDIENTE", "La Figura 30 está repetida en el Sprint 4."),
        ("Retrospectivas", "PENDIENTE", "No se incorporaron las retrospectivas de los cuatro sprints."),
        ("Matriz y documentación faltante", "PENDIENTE", "Faltan trazabilidad, alcance y exclusiones, modelo de base de datos y reglas del negocio."),
        ("Rótulos, referencias e índices", "VERIFICAR EN WORD", "Deben ser campos automáticos y actualizarse con F9."),
    ]
    table = doc.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    widths = [Cm(6.0), Cm(3.4), Cm(7.0)]
    headers = ["Observación", "Estado", "Revisión"]
    header = table.rows[0]
    set_repeat_table_header(header)
    for idx, text in enumerate(headers):
        cell = header.cells[idx]
        cell.width = widths[idx]
        shade_cell(cell, "1F4E78")
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        run = cell.paragraphs[0].add_run(text)
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_margins(cell)
    for observation, status, review in rows:
        cells = table.add_row().cells
        values = (observation, status, review)
        for idx, value in enumerate(values):
            cells[idx].width = widths[idx]
            cells[idx].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            cells[idx].text = value
            set_cell_margins(cells[idx])
        cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cells[1].paragraphs[0].runs[0].bold = True
        if status in {"PENDIENTE", "PARCIAL", "VERIFICAR EN WORD"}:
            for run in cells[1].paragraphs[0].runs:
                run.font.highlight_color = 7
    doc.add_paragraph()


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(2.2)
    section.bottom_margin = Cm(2.2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)

    styles = doc.styles
    styles["Normal"].font.name = "Arial"
    styles["Normal"].font.size = Pt(10.5)
    styles["Normal"].paragraph_format.space_after = Pt(5)
    styles["Title"].font.name = "Arial"
    styles["Title"].font.size = Pt(18)
    styles["Title"].font.bold = True
    styles["Title"].font.color.rgb = RGBColor(0, 0, 0)
    for name, size in (("Heading 1", 14), ("Heading 2", 12)):
        styles[name].font.name = "Arial"
        styles[name].font.size = Pt(size)
        styles[name].font.bold = True
        styles[name].font.color.rgb = RGBColor(0, 0, 0)

    title = doc.add_paragraph(style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.add_run("Revisión de observaciones del Capítulo III")
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.add_run("Proyecto Emma Fashion").bold = True

    p = doc.add_paragraph()
    p.add_run("Resultado general: ").bold = True
    p.add_run("la corrección está avanzada, pero todavía quedan observaciones antes de entregar el documento. ")
    r = p.add_run("Todo lo pendiente se encuentra marcado en amarillo.")
    r.font.highlight_color = 7

    doc.add_heading("Resumen de la revisión", level=1)
    add_status_table(doc)

    doc.add_heading("Aspectos corregidos", level=1)
    corrected = [
        "Los Sprint Backlog suman correctamente 18, 8, 11 y 14 días, para un total de 51 días.",
        "La tarea duplicada de activación y desactivación de usuarios fue eliminada.",
        "Los títulos de las cuatro tablas de pruebas indican pruebas funcionales de caja negra.",
        "La numeración de los apartados del Sprint 1 ya sigue la secuencia 3.3.1 a 3.3.7.",
        "La anterior duplicación de la Figura 24 fue corregida.",
    ]
    for item in corrected:
        doc.add_paragraph(item, style="List Bullet")

    doc.add_heading("Observaciones que todavía faltan corregir", level=1)
    add_pending(
        doc,
        "Terminología de la estimación",
        "La Tabla 1 todavía dice “Planning Pocker, Estimacion del esfuerzo”.",
        "Escribir “Tabla 1: Planning Poker, estimación del esfuerzo”. Cambiar “XtraSmall” por “Extra Small” y “Tiempo (Día)” por “Tiempo (días)”.",
    )
    add_pending(
        doc,
        "Nombre del Product Backlog",
        "La Tabla 14 todavía aparece como “Producto Backlog” y el encabezado usa “Tiempo (Dias)”.",
        "Escribir “Tabla 14: Product Backlog” y “Tiempo (días)”.",
    )
    add_pending(
        doc,
        "Códigos de historias de usuario",
        "En las historias de tallas y colores todavía aparecen HU-4 y HU-5.",
        "Uniformar los códigos como HU-04 y HU-05.",
    )
    add_pending(
        doc,
        "Nota del Sprint 1",
        "Aunque la Tabla 16 dice caja negra, su nota todavía dice “pruebas unitarias de caja blanca”.",
        "Usar: “Nota: Las pruebas funcionales de caja negra del Sprint 1 permitieron verificar el funcionamiento de los módulos implementados mediante datos de entrada válidos e inválidos y la comparación de los resultados obtenidos con los resultados esperados.”",
    )
    add_pending(
        doc,
        "Datos personales y contraseña",
        "En la prueba de inicio de sesión aparecen el correo gimenaquinaya4@gmail.com y la contraseña gimena123.",
        "Sustituirlos por datos ficticios, por ejemplo administradora@emmafashion.test y EmmaTest2026*. Si la contraseña sigue activa, cambiarla también en la aplicación.",
    )
    add_pending(
        doc,
        "Pruebas rechazadas por sprint",
        "Los Sprint 1, 2 y 3 no tienen dos casos rechazados. El Sprint 4 sí incluye dos.",
        "Agregar dos casos rechazados en cada uno de los Sprint 1, 2 y 3, utilizando las validaciones declaradas en las historias de usuario.",
    )
    add_pending(
        doc,
        "Prueba contradictoria del Sprint 3",
        "La prueba “Editar venta” indica 2 existencias y solicita 5 unidades, pero afirma que la venta se actualiza correctamente.",
        "La salida esperada debe rechazar la venta por existencias insuficientes y el resultado debe ser “Rechazado correctamente”.",
    )
    add_pending(
        doc,
        "Pruebas del Sprint 4",
        "La numeración salta del caso 4 al 6. Además, en los casos de reportes y rango inválido se repiten los datos de entrada como salida esperada.",
        "Renumerar los casos y redactar resultados observables: mostrar transacciones, cantidades y montos; para el rango inválido, mostrar un mensaje y no generar el reporte.",
    )
    add_pending(
        doc,
        "Numeración de figuras del Sprint 4",
        "La Figura 30 se utiliza para la interfaz de inventario y nuevamente para el reporte de ventas.",
        "Conservar Figura 30 para inventario, Figura 31 para reporte de compras y Figura 32 para reporte de ventas.",
    )
    add_pending(
        doc,
        "Apartados exigidos por la revisión",
        "No se encontraron las retrospectivas de los cuatro sprints, la matriz de trazabilidad, el alcance y exclusiones, el modelo de la base de datos ni las reglas del negocio.",
        "Incorporar esos apartados antes de la entrega. Las retrospectivas deben relacionar los acuerdos de cada sprint con el siguiente y declarar la deuda técnica al cierre.",
    )
    add_pending(
        doc,
        "Rótulos, referencias cruzadas e índices",
        "El texto pegado no permite comprobar que los títulos de tablas y figuras sean campos automáticos de Word.",
        "Usar Referencias > Insertar título; insertar referencias cruzadas en el texto y actualizar el índice general, el índice de tablas y el índice de figuras con F9.",
    )

    doc.add_heading("Casos rechazados que se pueden agregar", level=1)
    tests = [
        ("Sprint 1", "Inicio de sesión con contraseña incorrecta", "El sistema rechaza el acceso y muestra un mensaje de credenciales inválidas."),
        ("Sprint 1", "Registrar una categoría duplicada", "El sistema rechaza el registro e informa que la categoría ya existe."),
        ("Sprint 2", "Registrar un proveedor con CI/NIT duplicado", "El sistema rechaza el registro e informa que el CI/NIT ya está registrado."),
        ("Sprint 2", "Registrar una compra sin proveedor", "El sistema impide guardar la compra y solicita seleccionar un proveedor."),
        ("Sprint 3", "Vender una cantidad mayor a las existencias", "El sistema rechaza la venta y muestra “Existencias insuficientes”."),
        ("Sprint 3", "Registrar un cliente con CI/NIT duplicado", "El sistema rechaza el registro e informa que el CI/NIT ya existe."),
    ]
    table = doc.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    widths = [Cm(2.5), Cm(6.0), Cm(8.0)]
    for idx, text in enumerate(("Sprint", "Descripción", "Salida esperada")):
        cell = table.rows[0].cells[idx]
        cell.width = widths[idx]
        shade_cell(cell, "1F4E78")
        run = cell.paragraphs[0].add_run(text)
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_margins(cell)
    set_repeat_table_header(table.rows[0])
    for sprint, description, expected in tests:
        cells = table.add_row().cells
        for idx, value in enumerate((sprint, description, expected)):
            cells[idx].width = widths[idx]
            cells[idx].text = value
            cells[idx].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_margins(cells[idx])
        cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run("Conclusión: ").bold = True
    p.add_run("los tiempos y la estructura principal mejoraron, pero deben resolverse todas las marcas amarillas antes de considerar atendidas las observaciones.")

    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    build()
