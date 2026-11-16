from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import shutil
import textwrap

from docx import Document
from docx.enum.text import WD_COLOR_INDEX
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"C:\Users\HP\.codex\visualizations\2026\07\28\019faabb-03f0-7721-a83a-520605149e89")
DOCX = ROOT / "PERFIL_TESIS_GRADO_Quinaya4_CORREGIDO.docx"
QA = ROOT / "revision-tesis"


def font(size: int, bold: bool = False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path(r"C:\Windows\Fonts") / name), size)


def wrapped(draw, text, box, size=31, bold=False, fill="#172554"):
    x1, y1, x2, y2 = box
    max_chars = max(12, int((x2 - x1) / (size * 0.56)))
    lines = textwrap.wrap(text, width=max_chars)
    fnt = font(size, bold)
    heights = [draw.textbbox((0, 0), line, font=fnt)[3] for line in lines]
    total = sum(heights) + max(0, len(lines) - 1) * 6
    y = y1 + ((y2 - y1) - total) / 2
    for line, height in zip(lines, heights):
        width = draw.textbbox((0, 0), line, font=fnt)[2]
        draw.text((x1 + ((x2 - x1) - width) / 2, y), line, font=fnt, fill=fill)
        y += height + 6


def actor(draw, x, y, label, color="#7c3aed"):
    draw.ellipse((x - 28, y - 90, x + 28, y - 34), fill=color, outline="#ffffff", width=4)
    draw.line((x, y - 34, x, y + 55), fill=color, width=8)
    draw.line((x - 55, y, x + 55, y), fill=color, width=8)
    draw.line((x, y + 55, x - 52, y + 125), fill=color, width=8)
    draw.line((x, y + 55, x + 52, y + 125), fill=color, width=8)
    wrapped(draw, label, (x - 150, y + 130, x + 150, y + 210), 28, True)


def ellipse(draw, center, label, fill, outline, width=360, height=100):
    x, y = center
    box = (x - width // 2, y - height // 2, x + width // 2, y + height // 2)
    draw.ellipse(box, fill=fill, outline=outline, width=4)
    wrapped(draw, label, box, 26, True)
    return box


def line(draw, p1, p2, dashed=False, color="#64748b"):
    if not dashed:
        draw.line((*p1, *p2), fill=color, width=4)
        return
    x1, y1 = p1
    x2, y2 = p2
    steps = 18
    for i in range(0, steps, 2):
        a = i / steps
        b = min((i + 1) / steps, 1)
        draw.line((x1 + (x2 - x1) * a, y1 + (y2 - y1) * a,
                   x1 + (x2 - x1) * b, y1 + (y2 - y1) * b), fill=color, width=3)


def make_sprint1(path):
    img = Image.new("RGB", (2400, 1350), "#fffafd")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((280, 70, 2110, 1250), radius=28, fill="#ffffff", outline="#c4b5fd", width=5)
    d.text((330, 92), "Sistema de control Emma Fashion — Sprint 1", font=font(36, True), fill="#312e81")
    admin = (150, 500)
    seller = (2250, 390)
    client = (2250, 930)
    actor(d, *admin, "Administradora", "#7c3aed")
    actor(d, *seller, "Encargada de ventas", "#db2777")
    actor(d, *client, "Cliente", "#16a34a")
    cases = [
        ((600, 260), "Iniciar sesión", "#ede9fe", "#8b5cf6"),
        ((1040, 220), "Gestionar usuarios", "#ede9fe", "#8b5cf6"),
        ((1480, 220), "Gestionar roles y permisos", "#ede9fe", "#8b5cf6"),
        ((620, 500), "Gestionar categorías", "#dbeafe", "#3b82f6"),
        ((1040, 500), "Gestionar marcas", "#dbeafe", "#3b82f6"),
        ((1460, 500), "Gestionar tallas", "#dbeafe", "#3b82f6"),
        ((620, 760), "Gestionar colores", "#dbeafe", "#3b82f6"),
        ((1040, 760), "Gestionar productos", "#dbeafe", "#3b82f6"),
        ((1460, 760), "Ver catálogo", "#dcfce7", "#22c55e"),
    ]
    for c, label, fill, outline in cases:
        ellipse(d, c, label, fill, outline)
    for target in [(600,260),(1040,220),(1480,220),(620,500),(1040,500),(1460,500),(620,760),(1040,760),(1460,760)]:
        line(d, (250, 500), (target[0]-180, target[1]))
    line(d, (2145, 390), (780, 260))
    line(d, (2145, 390), (1640, 760))
    line(d, (2145, 930), (1640, 760))
    d.text((730, 1080), "Cada gestión está asociada directamente a un usuario responsable.", font=font(32, True), fill="#4c1d95")
    img.save(path, quality=96)


def make_sprint2(path):
    img = Image.new("RGB", (2400, 1350), "#fffdf8")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((280, 70, 2110, 1250), radius=28, fill="#ffffff", outline="#f9a8d4", width=5)
    d.text((330, 92), "Sistema de control Emma Fashion — Sprint 2", font=font(36, True), fill="#831843")
    actor(d, 150, 560, "Administradora", "#7c3aed")
    provider = [
        ((630, 250), "Registrar proveedor"), ((1040, 250), "Listar proveedores"),
        ((1450, 250), "Buscar proveedor"), ((630, 430), "Consultar proveedor"),
        ((1040, 430), "Editar proveedor"), ((1450, 430), "Anular proveedor"),
    ]
    purchase = [
        ((600, 700), "Registrar compra"), ((1000, 700), "Listar compras"),
        ((1400, 700), "Buscar compra"), ((1800, 700), "Consultar compra"),
        ((600, 900), "Editar compra"), ((1000, 900), "Anular compra"),
        ((1400, 900), "Imprimir comprobante"),
    ]
    included = [((630, 1120), "Calcular total"), ((1050, 1120), "Actualizar inventario"), ((1600, 1120), "Revertir existencias")]
    for c, label in provider:
        ellipse(d, c, label, "#fef3c7", "#f59e0b", 340, 92)
    for c, label in purchase:
        ellipse(d, c, label, "#fce7f3", "#ec4899", 350, 96)
    for c, label in included:
        ellipse(d, c, label, "#e0f2fe", "#0ea5e9", 350, 94)
    for c, _ in provider + purchase:
        line(d, (250, 560), (c[0]-175, c[1]))
    line(d, (600, 748), (630, 1073), True)
    line(d, (600, 748), (1050, 1073), True)
    line(d, (1000, 948), (1600, 1073), True)
    d.text((710, 1010), "«include»", font=font(23, True), fill="#0369a1")
    d.text((1110, 1010), "«include»", font=font(23, True), fill="#0369a1")
    d.text((1360, 1000), "«include»", font=font(23, True), fill="#0369a1")
    img.save(path, quality=96)


def highlight_paragraph(paragraph):
    for run in paragraph.runs:
        run.font.highlight_color = WD_COLOR_INDEX.YELLOW


def finalize_text():
    doc = Document(DOCX)
    replacements = {
        "Ejecución del primer Sprint 1": "3.3 Ejecución del Sprint 1",
        "3.4.1 Ejecución del Sprint 2": "3.4 Ejecución del Sprint 2",
        "Ejecución del Sprint 2": "3.4 Ejecución del Sprint 2",
        "Lista de tareas Sprint 2": "3.4.2.1 Lista de tareas del Sprint 2",
        "Diagrama de casos de uso del Sprint 2": "3.4.3 Diagrama de casos de uso del Sprint 2",
        "Diagrama de clases del Sprint 2": "3.4.4 Diagrama de clases del Sprint 2",
        "Implementación del Sprint 2": "3.4.5 Implementación del Sprint 2",
        "Sprint Review Sprint 2": "3.4.6 Sprint Review del Sprint 2",
    }
    for p in doc.paragraphs:
        key = p.text.strip()
        if key in replacements:
            p.text = replacements[key]
            p.style = "Heading 2" if replacements[key].startswith("3.4 ") or replacements[key].startswith("3.3 ") else "Heading 3"
            highlight_paragraph(p)
        if key == "3.4.1 Definición de hecho del Sprint 2":
            p.style = "Heading 3"
            highlight_paragraph(p)
        if key == "3.4.2 Sprint Backlog del Sprint 2":
            p.style = "Heading 3"
            highlight_paragraph(p)
    doc.save(DOCX)


def replace_media(replacements):
    temp = DOCX.with_suffix(".tmp.docx")
    with ZipFile(DOCX, "r") as src, ZipFile(temp, "w", ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = replacements.get(item.filename, src.read(item.filename))
            dst.writestr(item, data)
    shutil.move(temp, DOCX)


def main():
    QA.mkdir(parents=True, exist_ok=True)
    sprint1 = QA / "diagrama-casos-uso-sprint-1-corregido.png"
    sprint2 = QA / "diagrama-casos-uso-sprint-2-corregido.png"
    make_sprint1(sprint1)
    make_sprint2(sprint2)
    finalize_text()
    replace_media({
        "word/media/image11.png": sprint1.read_bytes(),
        "word/media/image20.png": sprint2.read_bytes(),
    })
    print(DOCX)


if __name__ == "__main__":
    main()
