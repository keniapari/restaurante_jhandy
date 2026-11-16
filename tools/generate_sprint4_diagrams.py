from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

OUT = Path(r"C:\laragon\www\control_emmafashion\documento_corregido\diagramas_sprint4")
OUT.mkdir(parents=True, exist_ok=True)

FONT = r"C:\Windows\Fonts\arial.ttf"
FONT_B = r"C:\Windows\Fonts\arialbd.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


PURPLE = "#7A3B8F"
HEADER = "#E9DDF0"
LAVENDER = "#E7D8ED"
BLUE = "#CFE2F3"
LIGHT_BLUE = "#B9DDF2"
BLACK = "#111111"


def arrow(draw, start, end, color=BLACK, width=2, dashed=False):
    x1, y1 = start
    x2, y2 = end
    if dashed:
        steps = 18
        for i in range(0, steps, 2):
            a = i / steps
            b = min((i + 1) / steps, 1)
            draw.line((x1 + (x2-x1)*a, y1 + (y2-y1)*a, x1 + (x2-x1)*b, y1 + (y2-y1)*b), fill=color, width=width)
    else:
        draw.line((x1, y1, x2, y2), fill=color, width=width)
    angle = math.atan2(y2-y1, x2-x1)
    for delta in (2.55, -2.55):
        draw.line((x2, y2, x2 + 12*math.cos(angle+delta), y2 + 12*math.sin(angle+delta)), fill=color, width=width)


def uml_box(draw, x, y, w, title, attrs, methods, stereotype=None):
    title_h = 52 if stereotype else 42
    line_h = 25
    attrs_h = max(36, 16 + line_h * len(attrs))
    methods_h = max(36, 16 + line_h * len(methods))
    h = title_h + attrs_h + methods_h
    draw.rectangle((x, y, x+w, y+h), fill="white", outline=PURPLE, width=3)
    draw.rectangle((x, y, x+w, y+title_h), fill=HEADER, outline=PURPLE, width=3)
    if stereotype:
        draw.text((x+w/2, y+8), stereotype, fill=BLACK, font=font(15), anchor="ma")
        draw.text((x+w/2, y+30), title, fill=BLACK, font=font(20, True), anchor="ma")
    else:
        draw.text((x+w/2, y+12), title, fill=BLACK, font=font(20, True), anchor="ma")
    sep1 = y + title_h
    sep2 = sep1 + attrs_h
    draw.line((x, sep2, x+w, sep2), fill=PURPLE, width=2)
    yy = sep1 + 10
    for value in attrs:
        draw.text((x+14, yy), value, fill=BLACK, font=font(16))
        yy += line_h
    yy = sep2 + 10
    for value in methods:
        draw.text((x+14, yy), value, fill=BLACK, font=font(16))
        yy += line_h
    return (x, y, x+w, y+h)


def class_diagram():
    img = Image.new("RGB", (1900, 1060), "white")
    d = ImageDraw.Draw(img)
    d.text((950, 28), "Diagrama de clases del Sprint 4", fill=BLACK, font=font(30, True), anchor="ma")

    producto = uml_box(d, 55, 110, 385, "Producto", [
        "- id: int", "- nombre: string", "- genero: string",
        "- precio_venta: decimal", "- estado: string",
    ], [
        "+ inventario(): HasOne", "+ variantes(): HasMany",
        "+ categoria(): BelongsTo", "+ marca(): BelongsTo",
    ])
    inventario = uml_box(d, 515, 110, 410, "Inventario", [
        "- id: int", "- producto_id: int", "- stock_actual: int", "- disponible: boolean",
        "/ total_entradas: int", "/ total_salidas: int",
    ], [
        "+ producto(): BelongsTo", "+ movimientos(): HasMany",
        "+ getTotalEntradasAttribute(): int", "+ getTotalSalidasAttribute(): int",
    ])
    movimiento = uml_box(d, 1000, 110, 485, "InventarioMovimiento", [
        "- id: int", "- inventario_id: int", "- user_id: int?", "- tipo: string",
        "- cantidad: int", "- motivo: string?", "- origen_tipo: string?", "- origen_id: int?",
    ], [
        "+ inventario(): BelongsTo", "+ user(): BelongsTo",
        "+ scopeWithExistingOrigin(): Builder",
    ])
    usuario = uml_box(d, 1050, 760, 350, "Usuario", ["- id: int", "- name: string"], ["+ movimientos(): HasMany"])
    reportes = uml_box(d, 1515, 110, 340, "ReportesController", [], [
        "+ compras(): Response", "+ ventas(): Response", "+ comprasVistaPdf(): Response",
        "+ ventasVistaPdf(): Response", "+ comprasPdf(): HttpResponse", "+ ventasPdf(): HttpResponse",
        "- getComprasData(): array", "- getVentasData(): array", "- getRangoFechas(): string",
    ], "<<controller>>")

    # associations
    d.line((producto[2], 260, inventario[0], 260), fill=BLACK, width=2)
    d.text((producto[2]+7, 226), "1", fill=BLACK, font=font(16))
    d.text((inventario[0]-40, 267), "0..1", fill=BLACK, font=font(16))

    d.line((inventario[2], 300, movimiento[0], 300), fill=BLACK, width=2)
    d.text((inventario[2]+7, 266), "1", fill=BLACK, font=font(16))
    d.text((movimiento[0]-42, 307), "0..*", fill=BLACK, font=font(16))

    d.line((1242, movimiento[3], 1242, usuario[1]), fill=BLACK, width=2)
    d.text((1252, movimiento[3]+10), "0..*", fill=BLACK, font=font(16))
    d.text((1252, usuario[1]-34), "0..1", fill=BLACK, font=font(16))
    d.text((1260, (movimiento[3]+usuario[1])/2), "realiza", fill=BLACK, font=font(16))

    d.text(((reportes[0]+reportes[2])/2, reportes[3]+22), "Depende de Compra, Venta, Proveedor, Categoría y Usuario", fill=PURPLE, font=font(14), anchor="ma")

    d.text((60, 1015), "Nota: los filtros de fecha, proveedor, usuario y categoría pertenecen a la solicitud; no son atributos persistentes.", fill="#444444", font=font(16))
    path = OUT / "Figura_29_Diagrama_clases_Sprint_4_corregido.png"
    img.save(path, quality=95)
    return path


def ellipse(draw, box, text, fill=LAVENDER, outline=PURPLE, size=18):
    draw.ellipse(box, fill=fill, outline=outline, width=2)
    x1, y1, x2, y2 = box
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font(size)) > (x2-x1-28) and current:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    total = len(lines) * (size + 3)
    yy = (y1+y2-total)/2
    for line in lines:
        draw.text(((x1+x2)/2, yy), line, fill=BLACK, font=font(size), anchor="ma")
        yy += size + 3
    return ((x1+x2)/2, (y1+y2)/2)


def actor(draw, x, y, label):
    draw.ellipse((x-16, y-62, x+16, y-30), fill="#D69BC5", outline=PURPLE, width=2)
    draw.line((x, y-30, x, y+28), fill=PURPLE, width=3)
    draw.line((x-35, y-8, x+35, y-8), fill=PURPLE, width=3)
    draw.line((x, y+28, x-32, y+70), fill=PURPLE, width=3)
    draw.line((x, y+28, x+32, y+70), fill=PURPLE, width=3)
    draw.text((x, y+82), label, fill=BLACK, font=font(17), anchor="ma")


def use_case_diagram():
    img = Image.new("RGB", (1900, 1080), "white")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((190, 25, 1845, 1025), radius=8, outline="#666666", width=2)
    actor(d, 95, 460, "Usuario autorizado")

    main = {
        "Visualizar inventario": (300, 135, 610, 225),
        "Consultar movimientos de inventario": (300, 300, 610, 400),
        "Cambiar disponibilidad del producto": (300, 485, 610, 585),
        "Generar reporte de compras": (300, 680, 610, 775),
        "Generar reporte de ventas": (300, 865, 610, 960),
    }
    centers = {name: ellipse(d, box, name) for name, box in main.items()}
    for center in centers.values():
        d.line((130, 450, center[0]-155, center[1]), fill="#555555", width=2)

    inv_cases = {
        "Buscar productos": (760, 110, 1050, 190),
        "Consultar entradas": (760, 220, 1050, 300),
        "Consultar salidas": (760, 330, 1050, 410),
        "Consultar existencias actuales": (760, 440, 1050, 530),
    }
    for name, box in inv_cases.items():
        c = ellipse(d, box, name, BLUE)
        arrow(d, (610, 180), (box[0], c[1]), PURPLE, 2, True)
        d.text(((610+box[0])/2, (180+c[1])/2-10), "<<include>>", fill=PURPLE, font=font(13), anchor="ma")

    movement = ellipse(d, (760, 560, 1050, 650), "Ver detalle del movimiento", BLUE)
    arrow(d, (610, 350), (760, movement[1]), PURPLE, 2, True)
    d.text((690, 470), "<<include>>", fill=PURPLE, font=font(13), anchor="ma")

    report_cases = {
        "Filtrar compras por fechas proveedor y categoría": (690, 680, 1050, 770),
        "Consultar totales de compras": (1120, 680, 1420, 770),
        "Visualizar y exportar compras en PDF": (1490, 680, 1815, 770),
        "Filtrar ventas por fechas usuario y categoría": (690, 860, 1050, 950),
        "Consultar totales de ventas": (1120, 860, 1420, 950),
        "Visualizar y exportar ventas en PDF": (1490, 860, 1815, 950),
    }
    report_centers = {name: ellipse(d, box, name, LIGHT_BLUE, "#2E86AB") for name, box in report_cases.items()}
    purchase = centers["Generar reporte de compras"]
    sale = centers["Generar reporte de ventas"]
    links = [
        (purchase, report_centers["Filtrar compras por fechas proveedor y categoría"]),
        (report_centers["Filtrar compras por fechas proveedor y categoría"], report_centers["Consultar totales de compras"]),
        (report_centers["Consultar totales de compras"], report_centers["Visualizar y exportar compras en PDF"]),
        (sale, report_centers["Filtrar ventas por fechas usuario y categoría"]),
        (report_centers["Filtrar ventas por fechas usuario y categoría"], report_centers["Consultar totales de ventas"]),
        (report_centers["Consultar totales de ventas"], report_centers["Visualizar y exportar ventas en PDF"]),
    ]
    for a, b in links:
        arrow(d, (a[0]+155, a[1]), (b[0]-160, b[1]), "#2E86AB", 2, True)
    path = OUT / "Figura_28_Diagrama_casos_uso_Sprint_4_corregido.png"
    img.save(path, quality=95)
    return path


if __name__ == "__main__":
    print(class_diagram())
    print(use_case_diagram())
