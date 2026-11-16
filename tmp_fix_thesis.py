from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.section import WD_SECTION_START
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

SOURCE = Path(r"C:\Users\HP\Documents\PERFIL_TESIS_GRADO-Quinaya4.docx")
OUTPUT = Path(r"C:\Users\HP\.codex\visualizations\2026\07\28\019faabb-03f0-7721-a83a-520605149e89\PERFIL_TESIS_GRADO_Quinaya4_CORREGIDO.docx")

doc = Document(SOURCE)

YELLOW = 'FFFF00'

def shade_run(run):
    highlight = OxmlElement('w:highlight')
    highlight.set(qn('w:val'), 'yellow')
    rpr = run._element.get_or_add_rPr()
    for old in rpr.findall(qn('w:highlight')):
        rpr.remove(old)
    rpr.append(highlight)

def replace_paragraph(paragraph, text, highlight=True):
    paragraph.clear()
    run = paragraph.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(12)
    if highlight:
        shade_run(run)
    return paragraph

def insert_paragraph_after(paragraph, text, style=None, highlight=True):
    new_p = OxmlElement('w:p')
    paragraph._p.addnext(new_p)
    new_paragraph = paragraph._parent.add_paragraph()
    new_paragraph._p.getparent().remove(new_paragraph._p)
    new_p.addnext(new_paragraph._p)
    new_paragraph._p.getparent().remove(new_p)
    if style:
        new_paragraph.style = style
    replace_paragraph(new_paragraph, text, highlight)
    return new_paragraph

def set_page_number(section, fmt='decimal', start=None):
    footer = section.footer
    footer.is_linked_to_previous = False
    for p in footer.paragraphs:
        p._element.getparent().remove(p._element)
    p = footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    fld_char1 = OxmlElement('w:fldChar')
    fld_char1.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = ' PAGE '
    fld_char2 = OxmlElement('w:fldChar')
    fld_char2.set(qn('w:fldCharType'), 'end')
    run._r.extend([fld_char1, instr, fld_char2])
    sect_pr = section._sectPr
    for old in sect_pr.findall(qn('w:pgNumType')):
        sect_pr.remove(old)
    pg_num = OxmlElement('w:pgNumType')
    pg_num.set(qn('w:fmt'), fmt)
    if start is not None:
        pg_num.set(qn('w:start'), str(start))
    sect_pr.append(pg_num)

# Page numbering: preliminary section in lowercase Roman; content in decimal.
if doc.sections:
    set_page_number(doc.sections[0], 'lowerRoman', 1)
if len(doc.sections) > 1:
    set_page_number(doc.sections[1], 'decimal', 1)
for section in doc.sections[2:]:
    set_page_number(section, 'decimal', None)

# Heading level 3 and 4, and keep every heading with the following content.
for style_name in ('Heading 3', 'Heading 4'):
    style = doc.styles[style_name]
    style.font.name = 'Arial'
    style.font.size = Pt(12)
    style.font.bold = True
    style.font.italic = style_name == 'Heading 4'
    style.font.color.rgb = RGBColor(0, 0, 0)
    style.paragraph_format.keep_with_next = True
    style.paragraph_format.space_before = Pt(12)
    style.paragraph_format.space_after = Pt(6)

for paragraph in doc.paragraphs:
    if paragraph.style.name.startswith('Heading'):
        paragraph.paragraph_format.keep_with_next = True
        paragraph.paragraph_format.page_break_before = False

# Normalize badly spaced heading numbering and titles.
heading_fixes = {
    '1 .1 .1   Diagnostico': '1.1.1 Diagnóstico',
    '1. 1. 2  Justificación': '1.1.2 Justificación',
    '1. 1. 2 .1   Justificación  técnica': '1.1.2.1 Justificación técnica',
    '1. 1. 2. 2   Justificación  social': '1.1.2.2 Justificación social',
    '1. 1. 2. 3   Justificación  económica': '1.1.2.3 Justificación económica',
    'Objetivo de la investigación': '1.3 Objetivos de la investigación',
    'Objetivos específicos': '1.3.2 Objetivos específicos',
}
for paragraph in doc.paragraphs:
    normalized = ' '.join(paragraph.text.split())
    for old, new in heading_fixes.items():
        if normalized == ' '.join(old.split()):
            replace_paragraph(paragraph, new)
            break

# Chapter I: problem descriptions, question, objective and ordered specific objectives.
problem_texts = [
    'La tienda Emma Fashion no cuenta con un registro digital y actualizado de sus productos. La información relacionada con categorías, marcas, tallas, colores, precios y disponibilidad se consulta mediante la observación directa de las prendas. Esto dificulta localizar los productos y brindar información rápida a los clientes.',
    'Las compras de mercadería se registran manualmente en cuadernos, donde se anotan las prendas adquiridas, las cantidades, los precios y el monto total. Este procedimiento genera demoras al buscar información de compras anteriores, posibles errores en los cálculos y dificultad para actualizar las existencias.',
    'Las ventas se registran manualmente en cuadernos, anotando la prenda vendida y su precio. Esta forma de trabajo ocasiona demoras al consultar información, dificulta la atención al cliente y puede producir equivocaciones en los registros.',
    'El inventario se controla mediante la revisión física de las prendas ubicadas en estantes, maniquíes y depósito. Además, los totales de ventas se calculan manualmente mediante la revisión de los cuadernos. Esta situación dificulta conocer las existencias actualizadas y puede generar pérdida de tiempo y errores en los resultados.',
]
specific_objectives = [
    'Diseñar un módulo de gestión de productos que permita registrar prendas de vestir con sus respectivas categorías, marcas, tallas, colores, precios, estados e imágenes.',
    'Implementar un módulo de compras que permita registrar la mercadería adquirida, sus cantidades, precios y proveedores.',
    'Implementar un módulo de ventas que permita registrar las prendas vendidas, calcular automáticamente el total y facilitar la atención al cliente.',
    'Implementar un módulo de inventario y reportes que permita controlar las entradas, salidas y existencias, además de obtener información actualizada para apoyar la toma de decisiones.',
]
paragraphs = doc.paragraphs
for i, paragraph in enumerate(paragraphs):
    text = ' '.join(paragraph.text.split())
    if text == '1.2.1 Descripción del problema':
        body = []
        j = i + 1
        while j < len(paragraphs) and '1.2.2' not in paragraphs[j].text:
            if paragraphs[j].text.strip():
                body.append(paragraphs[j])
            j += 1
        for target, new_text in zip(body[:4], problem_texts):
            replace_paragraph(target, new_text)
        for extra in body[4:]:
            replace_paragraph(extra, '')
    elif text.startswith('¿Cómo mejorar el control de compras'):
        replace_paragraph(paragraph, '¿Cómo mejorar el control de compras, ventas e inventario en la tienda de ropa Emma Fashion, ubicada en la localidad de Eterazama, durante la gestión 2026?')
    elif 'Desarrollar una aplicación web para' in text and 'Emma Fashion' in text and 'gestión 2026' in text:
        replace_paragraph(paragraph, 'Desarrollar una aplicación web para mejorar el control de compras, ventas e inventario en la tienda de ropa Emma Fashion, ubicada en la localidad de Eterazama, durante la gestión 2026.')

# Replace the four objective paragraphs.
for i, paragraph in enumerate(doc.paragraphs):
    if 'Diseñar un módulo de gestión de productos' in paragraph.text:
        targets = [p for p in doc.paragraphs[i:i+8] if p.text.strip()][:4]
        for target, text in zip(targets, specific_objectives):
            replace_paragraph(target, text)
        break

# Chapter II: application web definition with linking phrase.
for i, paragraph in enumerate(doc.paragraphs):
    if '2.2.1 Aplicación Web' in paragraph.text:
        following = [p for p in doc.paragraphs[i+1:i+7] if p.text.strip()]
        if following:
            replace_paragraph(following[0], 'De acuerdo con los autores consultados, una aplicación web es un sistema informático al que se accede mediante un navegador y que permite registrar, consultar, procesar y actualizar información a través de internet o de una red local. Su funcionamiento se distribuye entre una interfaz utilizada por el usuario y un servidor encargado de procesar los datos y comunicarse con la base de datos.')
        if len(following) > 1:
            replace_paragraph(following[1], 'En el presente proyecto, este concepto se aplica mediante una aplicación web que permite gestionar productos, proveedores, clientes, compras, ventas, inventario, usuarios y reportes de la tienda Emma Fashion.')
        break

# Add linking words to obvious direct-quote paragraphs and set long quotes as blocks.
for paragraph in doc.paragraphs:
    text = paragraph.text.strip()
    if len(text.split()) > 40 and ('“' in text or '”' in text):
        paragraph.paragraph_format.left_indent = Pt(36)
        paragraph.paragraph_format.right_indent = Pt(0)
        paragraph.paragraph_format.first_line_indent = Pt(0)
        paragraph.paragraph_format.line_spacing = 2
        for run in paragraph.runs:
            shade_run(run)
    elif text.startswith(('Wilman Patricio', 'Altube Vera', 'Aguirregomezcorta')) and 'Según' not in text and 'De acuerdo' not in text:
        replace_paragraph(paragraph, 'Según ' + text)

# Chapter III substantive corrections.
replacements = {
    'El Sprint 1 se considera terminado cuando se hayan implementado correctamente': 'El Sprint 1 se considera terminado cuando la autenticación y los módulos de usuarios, roles y permisos, categorías, marcas, tallas, colores y productos se encuentran implementados y funcionan correctamente. El sistema debe permitir registrar, listar, buscar, consultar y editar la información, aplicar las validaciones definidas y controlar el acceso de acuerdo con los permisos asignados. Además, los productos activos deben mostrarse en el catálogo y cada producto debe contar con su respectivo control de inventario.',
    'La ejecución del Sprint 2 se enfoca en la implementación de funciones': 'La ejecución del Sprint 2 se enfocó en el desarrollo de los módulos de gestión de proveedores y compras. Las actividades fueron organizadas mediante las historias de usuario HU-07 y HU-08. Este sprint permitió registrar los proveedores de la tienda, gestionar las compras de mercadería y actualizar automáticamente las entradas del inventario.',
}
for paragraph in doc.paragraphs:
    for prefix, new_text in replacements.items():
        if paragraph.text.strip().startswith(prefix):
            replace_paragraph(paragraph, new_text)

# Insert missing Sprint 2 Definition of Done immediately before its backlog heading.
for paragraph in list(doc.paragraphs):
    if paragraph.text.strip().lower() == 'sprint backlog':
        previous_text = paragraph._p.getprevious()
        # Select the Sprint 2 occurrence by nearby prior paragraph.
        prior = ''
        p = paragraph._p.getprevious()
        for _ in range(3):
            if p is not None:
                prior += ''.join(p.itertext())
                p = p.getprevious()
        if 'Sprint 2' in prior:
            heading = paragraph.insert_paragraph_before('3.4.1 Definición de hecho')
            heading.style = doc.styles['Heading 3']
            for run in heading.runs:
                shade_run(run)
            body = paragraph.insert_paragraph_before('El Sprint 2 se considera terminado cuando los módulos de gestión de proveedores y compras se encuentran implementados y funcionan correctamente. El sistema debe permitir registrar, listar, buscar, consultar, editar y anular proveedores; registrar compras relacionadas con proveedores y productos existentes; calcular automáticamente subtotales y totales; actualizar las entradas del inventario; conservar el historial de compras y generar comprobantes imprimibles. Las funcionalidades deben cumplir los criterios de aceptación establecidos en las historias de usuario HU-07 y HU-08.')
            for run in body.runs:
                shade_run(run)
            replace_paragraph(paragraph, '3.4.2 Sprint Backlog')
            paragraph.style = doc.styles['Heading 3']
            break

# Fix Sprint 3 HU codes and wording in table 18 (zero-based).
if len(doc.tables) > 18:
    table = doc.tables[18]
    for row in table.rows:
        for cell in row.cells:
            if cell.text.strip() == 'HU-07':
                replace_paragraph(cell.paragraphs[0], 'HU-09')
            elif cell.text.strip() == 'HU-08':
                replace_paragraph(cell.paragraphs[0], 'HU-10')

# Remove duplicated activation/deactivation task in Sprint Backlog 1 table.
if len(doc.tables) > 14:
    table = doc.tables[14]
    seen = False
    for row in table.rows:
        row_text = ' '.join(cell.text for cell in row.cells)
        if 'Implementar la activación y desactivación de usuarios.' in row_text:
            if not seen:
                seen = True
            else:
                for cell in row.cells:
                    if 'Implementar la activación' in cell.text:
                        replace_paragraph(cell.paragraphs[0], 'Implementar la actualización de datos personales y el cambio de contraseña, validando la contraseña actual.')
                    elif cell.text.strip() == '1':
                        for run in cell.paragraphs[0].runs:
                            shade_run(run)
                break

# Replace destructive terms in Sprint 2 backlog table.
if len(doc.tables) > 16:
    for row in doc.tables[16].rows:
        for cell in row.cells:
            original = cell.text
            revised = original.replace('eliminar proveedores', 'anular proveedores conservando el historial')
            revised = revised.replace('eliminar compras', 'anular compras y revertir las existencias')
            if revised != original:
                replace_paragraph(cell.paragraphs[0], revised)

# Capitalize Figure captions, normalize separator, align captions and notes with images.
for paragraph in doc.paragraphs:
    text = paragraph.text.strip()
    lower = text.lower()
    if lower.startswith('figura '):
        remainder = text[len('figura '):].strip()
        if ':' in remainder:
            number, title = remainder.split(':', 1)
            new_text = f'Figura {number.strip()}. {title.strip()}'
        else:
            new_text = 'Figura ' + remainder
        replace_paragraph(paragraph, new_text)
        paragraph.style = doc.styles['Caption']
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.paragraph_format.keep_with_next = True
    elif lower.startswith('nota:'):
        new_text = 'Nota. ' + text.split(':', 1)[1].strip()
        replace_paragraph(paragraph, new_text)
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Center image paragraphs and keep neighboring captions/notes together.
for paragraph in doc.paragraphs:
    if paragraph._p.xpath('.//w:drawing') or paragraph._p.xpath('.//w:pict'):
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.paragraph_format.keep_with_next = True

# Remove excessive blank paragraphs at the beginning of Chapter III.
for i, paragraph in enumerate(doc.paragraphs):
    if paragraph.text.strip() == 'CAPITULO III':
        for blank in doc.paragraphs[max(0, i-8):i]:
            if not blank.text.strip() and not blank._p.xpath('.//w:drawing'):
                parent = blank._element.getparent()
                if parent is not None:
                    parent.remove(blank._element)
        break

# General typography and orphan prevention.
for paragraph in doc.paragraphs:
    paragraph.paragraph_format.widow_control = True
    if paragraph.style.name not in ('Title',):
        for run in paragraph.runs:
            if not run.font.name:
                run.font.name = 'Arial'

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUTPUT)
print(OUTPUT)
