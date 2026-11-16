import sys
from docx import Document

path = sys.argv[1]
terms = [term.casefold() for term in sys.argv[2:]]
document = Document(path)
paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs]

for index, text in enumerate(paragraphs):
    if text and any(term in text.casefold() for term in terms):
        print(f"\n--- PÁRRAFO {index} ---")
        for position in range(max(0, index - 2), min(len(paragraphs), index + 7)):
            if paragraphs[position]:
                print(f"[{position}] {paragraphs[position]}")

for table_index, table in enumerate(document.tables, start=1):
    table_text = "\n".join(cell.text for row in table.rows for cell in row.cells)
    if any(term in table_text.casefold() for term in terms):
        print(f"\n=== TABLA {table_index} ===")
        for row in table.rows:
            print(" || ".join(cell.text.strip().replace("\n", " | ") for cell in row.cells))
