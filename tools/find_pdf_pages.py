from pathlib import Path

import pdfplumber


pdf_path = Path(
    r"C:\laragon\www\control_emmafashion\documentos\PERFIL_TESIS_GRADO-Quinaya4_CORREGIDO_COMPLETO.pdf"
)
needles = [
    "ÍNDICE DE TABLAS",
    "Ejecución de Sprint 3",
    "Sprint Backlog 3",
    "Pruebas unitarias de caja blanca",
    "Ejecución del Sprint 4",
]

with pdfplumber.open(pdf_path) as document:
    for page_number, page in enumerate(document.pages, start=1):
        text = page.extract_text() or ""
        for needle in needles:
            if needle.casefold() in text.casefold():
                print(page_number, needle)
