import sys
from docx import Document

for path in sys.argv[1:]:
    print(f"\n===== {path} =====")
    document = Document(path)
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            print(text)
    for table_index, table in enumerate(document.tables, start=1):
        print(f"\n--- TABLA {table_index} ---")
        for row in table.rows:
            cells = [cell.text.strip().replace("\n", " | ") for cell in row.cells]
            print(" || ".join(cells))
