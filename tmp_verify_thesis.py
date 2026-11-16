from pathlib import Path
from docx import Document
from docx.oxml.ns import qn

path = Path(r"C:\Users\HP\.codex\visualizations\2026\07\28\019faabb-03f0-7721-a83a-520605149e89\PERFIL_TESIS_GRADO_Quinaya4_CORREGIDO.docx")
doc = Document(path)
highlights = 0
checks = {
    'objetivo_sin_comillas': False,
    'definicion_sprint_2': False,
    'figuras_mayuscula': True,
    'sprint_3_hu09': False,
    'sprint_3_hu10': False,
}
for paragraph in doc.paragraphs:
    text = ' '.join(paragraph.text.split())
    for run in paragraph.runs:
        highlight = run._r.find('.//' + qn('w:highlight'))
        if highlight is not None and highlight.get(qn('w:val')) == 'yellow':
            highlights += 1
    if text.startswith('Desarrollar una aplicación web para mejorar'):
        checks['objetivo_sin_comillas'] = not text.startswith(('“', '"')) and not text.endswith(('”', '"'))
    if text.startswith('El Sprint 2 se considera terminado'):
        checks['definicion_sprint_2'] = True
    if text.startswith('figura '):
        checks['figuras_mayuscula'] = False
for table in doc.tables:
    table_text = ' '.join(cell.text for row in table.rows for cell in row.cells)
    if 'Gestión de clientes' in table_text and 'HU-09' in table_text:
        checks['sprint_3_hu09'] = True
    if 'Gestión de ventas' in table_text and 'HU-10' in table_text:
        checks['sprint_3_hu10'] = True

print('paragraphs', len(doc.paragraphs))
print('tables', len(doc.tables))
print('sections', len(doc.sections))
print('yellow_highlights', highlights)
print(checks)
assert highlights > 20
assert all(checks.values())
