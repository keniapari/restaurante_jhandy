from docx import Document
from pathlib import Path

p = Path(r"C:\Users\HP\.codex\visualizations\2026\07\28\019faabb-03f0-7721-a83a-520605149e89\PERFIL_TESIS_GRADO_Quinaya4_CORREGIDO.docx")
doc = Document(p)
last = ""
for para in doc.paragraphs:
    drawings = para._p.xpath('.//a:blip')
    if drawings:
        for blip in drawings:
            rid = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
            part = doc.part.related_parts[rid]
            print(last[:120], '=>', rid, part.partname)
    if para.text.strip():
        last = para.text.strip()
