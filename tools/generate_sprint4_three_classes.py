from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(r"C:\laragon\www\control_emmafashion\documento_corregido\diagramas_sprint4")
OUT.mkdir(parents=True, exist_ok=True)
FONT = r"C:\Windows\Fonts\arial.ttf"
FONT_B = r"C:\Windows\Fonts\arialbd.ttf"
PURPLE = "#7A3B8F"
HEADER = "#E9DDF0"
BLACK = "#111111"


def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def box(draw, x, y, w, title, attrs, methods, stereotype=None):
    title_h = 58 if stereotype else 46
    line_h = 28
    attrs_h = max(42, 18 + len(attrs) * line_h)
    methods_h = max(42, 18 + len(methods) * line_h)
    h = title_h + attrs_h + methods_h
    draw.rectangle((x, y, x+w, y+h), fill="white", outline=PURPLE, width=3)
    draw.rectangle((x, y, x+w, y+title_h), fill=HEADER, outline=PURPLE, width=3)
    if stereotype:
        draw.text((x+w/2, y+7), stereotype, fill=BLACK, font=font(16), anchor="ma")
        draw.text((x+w/2, y+33), title, fill=BLACK, font=font(21, True), anchor="ma")
    else:
        draw.text((x+w/2, y+13), title, fill=BLACK, font=font(21, True), anchor="ma")
    sep = y + title_h + attrs_h
    draw.line((x, sep, x+w, sep), fill=PURPLE, width=2)
    yy = y + title_h + 10
    for text in attrs:
        draw.text((x+15, yy), text, fill=BLACK, font=font(17))
        yy += line_h
    yy = sep + 10
    for text in methods:
        draw.text((x+15, yy), text, fill=BLACK, font=font(17))
        yy += line_h
    return (x, y, x+w, y+h)


img = Image.new("RGB", (1800, 720), "white")
d = ImageDraw.Draw(img)

inventario = box(d, 30, 45, 480, "Inventario", [
    "- id: int",
    "- producto_id: int",
    "- stock_actual: int",
    "- disponible: boolean",
    "/ total_entradas: int",
    "/ total_salidas: int",
], [
    "+ producto(): BelongsTo",
    "+ movimientos(): HasMany",
    "+ getTotalEntradasAttribute(): int",
    "+ getTotalSalidasAttribute(): int",
])

movimiento = box(d, 660, 45, 500, "InventarioMovimiento", [
    "- id: int",
    "- inventario_id: int",
    "- user_id: int?",
    "- tipo: string",
    "- cantidad: int",
    "- motivo: string?",
    "- origen_tipo: string?",
    "- origen_id: int?",
], [
    "+ inventario(): BelongsTo",
    "+ user(): BelongsTo",
    "+ scopeWithExistingOrigin(): Builder",
])

reportes = box(d, 1310, 45, 460, "ReportesController", [], [
    "+ compras(): Response",
    "+ ventas(): Response",
    "+ comprasVistaPdf(): Response",
    "+ ventasVistaPdf(): Response",
    "+ comprasPdf(): HttpResponse",
    "+ ventasPdf(): HttpResponse",
    "- getComprasData(): array",
    "- getVentasData(): array",
    "- getRangoFechas(): string",
], "<<controller>>")

# Asociación real entre las dos clases de inventario.
line_y = 285
d.line((inventario[2], line_y, movimiento[0], line_y), fill=BLACK, width=2)
d.text((inventario[2]+10, line_y-34), "1", fill=BLACK, font=font(17))
d.text((movimiento[0]-48, line_y+8), "0..*", fill=BLACK, font=font(17))
d.text(((inventario[2]+movimiento[0])/2, line_y-30), "registra", fill=BLACK, font=font(17), anchor="ma")

# El controlador de reportes no es una tabla y recibe los filtros desde la solicitud.
d.text((1540, reportes[3]+28), "Los filtros se reciben mediante Request", fill=PURPLE, font=font(16), anchor="ma")

path = OUT / "Figura_29_Diagrama_clases_Sprint_4_tres_clases.png"
img.save(path, quality=95)
print(path)
