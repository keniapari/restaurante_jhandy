from docx import Document

doc = Document(r"C:\Users\HP\Documents\PERFIL_TESIS_GRADO-Quinaya4.docx")
keywords = (
    'Diagnost', 'Descripci', 'Formulaci', 'Objetivo', 'Aplicaci', 'CAPITULO',
    'Sprint', 'figura', 'Figura', 'Ejecuci', 'Definici', 'modelo', 'Modelo',
)
for index, paragraph in enumerate(doc.paragraphs):
    text = ' '.join(paragraph.text.split())
    if text and any(keyword in text for keyword in keywords):
        print(f"P{index:04d} [{paragraph.style.name}] {text[:240]}")

print('\nTABLES')
for index, table in enumerate(doc.tables):
    text = ' | '.join(' '.join(cell.text.split()) for row in table.rows for cell in row.cells)
    if any(keyword.lower() in text.lower() for keyword in ('HU-01', 'HU-07', 'HU-08', 'Producto Backlog')):
        print(f"T{index:03d} {text[:900]}")
