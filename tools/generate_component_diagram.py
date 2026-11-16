from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

OUT = Path(r"C:\laragon\www\control_emmafashion\documento_corregido\diagramas_sprint4")
OUT.mkdir(parents=True, exist_ok=True)
FONT = r"C:\Windows\Fonts\arial.ttf"
FONT_B = r"C:\Windows\Fonts\arialbd.ttf"


def f(size, bold=False, italic=False):
    if italic:
        path = r"C:\Windows\Fonts\ariali.ttf"
    else:
        path = FONT_B if bold else FONT
    return ImageFont.truetype(path, size)


INK = "#272727"
PURPLE = "#77506F"
PINK = "#F1D7D9"
PINK2 = "#F8E7E8"
CREAM = "#F5EBDD"
PACKAGE = "#FAFAFA"


def component(draw, x, y, w, h, title, description="", fill=PINK):
    draw.rounded_rectangle((x+5, y+6, x+w+5, y+h+6), radius=5, fill="#D6D0D0")
    draw.rounded_rectangle((x, y, x+w, y+h), radius=4, fill=fill, outline=PURPLE, width=2)
    header_h = 45
    draw.line((x, y+header_h, x+w, y+header_h), fill=PURPLE, width=1)
    draw.text((x+w/2, y+13), title, fill=INK, font=f(17, True), anchor="ma")
    # UML component icon
    ix, iy = x+w-34, y+11
    draw.rectangle((ix, iy, ix+17, iy+20), outline=PURPLE, width=2)
    draw.rectangle((ix-5, iy+4, ix+4, iy+9), fill=fill, outline=PURPLE, width=1)
    draw.rectangle((ix-5, iy+12, ix+4, iy+17), fill=fill, outline=PURPLE, width=1)
    if description:
        words = description.split()
        lines, current = [], ""
        for word in words:
            trial = (current + " " + word).strip()
            if draw.textlength(trial, font=f(14, italic=True)) > w-30 and current:
                lines.append(current)
                current = word
            else:
                current = trial
        if current:
            lines.append(current)
        yy = y + 57
        for line in lines[:4]:
            draw.text((x+15, yy), line, fill="#666666", font=f(14, italic=True))
            yy += 19
    return (x, y, x+w, y+h)


def datastore(draw, x, y, w, h, title, description):
    draw.rounded_rectangle((x+5, y+6, x+w+5, y+h+6), radius=4, fill="#D8D2C9")
    draw.rounded_rectangle((x, y, x+w, y+h), radius=4, fill=CREAM, outline="#6E6459", width=2)
    draw.line((x, y+42, x+w, y+42), fill="#6E6459", width=1)
    draw.text((x+w/2, y+12), title, fill=INK, font=f(17, True), anchor="ma")
    draw.text((x+14, y+57), description, fill="#666666", font=f(14, italic=True))
    return (x, y, x+w, y+h)


def center(box):
    return ((box[0]+box[2])/2, (box[1]+box[3])/2)


def dependency(draw, start, end, label=""):
    x1, y1 = start
    x2, y2 = end
    steps = 24
    for i in range(0, steps, 2):
        a, b = i/steps, min((i+1)/steps, 1)
        draw.line((x1+(x2-x1)*a, y1+(y2-y1)*a, x1+(x2-x1)*b, y1+(y2-y1)*b), fill="#777777", width=2)
    angle = math.atan2(y2-y1, x2-x1)
    for delta in (2.55, -2.55):
        draw.line((x2, y2, x2+12*math.cos(angle+delta), y2+12*math.sin(angle+delta)), fill="#777777", width=2)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        draw.rectangle((mx-55, my-13, mx+55, my+11), fill="white")
        draw.text((mx, my-9), label, fill="#555555", font=f(13), anchor="ma")


img = Image.new("RGB", (1900, 1120), "white")
d = ImageDraw.Draw(img)
d.text((950, 24), "Diagrama de componentes de Emma Fashion", fill=INK, font=f(30, True), anchor="ma")
d.rounded_rectangle((20, 70, 1880, 1085), radius=4, outline="#555555", width=2)
d.text((38, 80), "cmp Sistema web Emma Fashion", fill=INK, font=f(15, True))

# Cliente y compilación
navegador = component(d, 70, 220, 235, 105, "Navegador web", "Accede a las páginas y envía solicitudes HTTP")
vite = component(d, 70, 715, 235, 105, "Vite", "Compila los recursos de Vue TypeScript y Tailwind")

# Contenedor frontend
d.rounded_rectangle((365, 120, 940, 535), radius=6, fill=PACKAGE, outline="#777777", width=2)
d.text((390, 135), "Frontend", fill=INK, font=f(18, True))
vue = component(d, 405, 185, 225, 100, "Vue 3", "Construye las páginas y componentes de la interfaz")
inertia = component(d, 675, 185, 225, 100, "Inertia.js 3", "Comunica Vue con las respuestas de Laravel")
typescript = component(d, 405, 335, 225, 100, "TypeScript", "Define tipos para páginas formularios y datos")
tailwind = component(d, 675, 335, 225, 100, "Tailwind CSS 4", "Aplica los estilos responsivos de la interfaz")

# Contenedor backend
d.rounded_rectangle((365, 585, 1210, 1025), radius=6, fill=PACKAGE, outline="#777777", width=2)
d.text((390, 600), "Backend", fill=INK, font=f(18, True))
laravel = component(d, 405, 650, 230, 105, "Laravel 13", "Framework principal del servidor en PHP 8.3")
routes = component(d, 675, 650, 230, 105, "Rutas y middleware", "Controlan acceso mediante roles y permisos")
controllers = component(d, 945, 650, 230, 105, "Controladores", "Procesan solicitudes y retornan respuestas Inertia")
requests = component(d, 405, 835, 230, 105, "Form Requests", "Validan los datos enviados por los formularios")
models = component(d, 675, 835, 230, 105, "Modelos Eloquent", "Representan entidades relaciones e inventario")
wayfinder = component(d, 945, 835, 230, 105, "Wayfinder", "Genera funciones TypeScript para las rutas Laravel")

# Servicios y datos
fortify = component(d, 1290, 175, 240, 105, "Fortify y Socialite", "Gestionan autenticación y acceso mediante Google")
dompdf = component(d, 1580, 175, 235, 105, "DomPDF", "Genera los reportes de compras y ventas en PDF")
lucide = component(d, 1290, 350, 240, 105, "Lucide y Reka UI", "Proporcionan iconos y componentes visuales")
blade = component(d, 1580, 350, 235, 105, "Vistas Blade", "Plantilla raíz y comprobantes PDF")
storage = datastore(d, 1310, 650, 235, 95, "Almacenamiento", "Imágenes de productos")
mysql = datastore(d, 1310, 845, 235, 95, "Base de datos", "MySQL")
env = component(d, 1600, 845, 215, 95, "Configuración .env", "Configura MySQL correo y servicios")

# Dependencias principales. Se muestran solo las necesarias para mantener el diagrama legible.
dependency(d, (navegador[2], 270), (365, 270), "HTTP")
dependency(d, (vue[2], 235), (inertia[0], 235), "páginas")
dependency(d, (typescript[0]+112, typescript[1]), (vue[0]+112, vue[3]), "tipos")
dependency(d, (tailwind[0]+112, tailwind[1]), (inertia[0]+112, inertia[3]), "estilos")
dependency(d, (vite[2], 765), (365, 455), "compila")
dependency(d, (inertia[0]+112, inertia[3]), (laravel[0]+115, laravel[1]), "Inertia")
dependency(d, (laravel[2], 702), (routes[0], 702))
dependency(d, (routes[2], 702), (controllers[0], 702))
dependency(d, (controllers[0]+55, controllers[3]), (requests[2], 885), "valida")
dependency(d, (controllers[0]+155, controllers[3]), (models[2], 885), "consulta")
dependency(d, (wayfinder[0]+112, wayfinder[1]), (routes[0]+112, routes[3]), "rutas")
dependency(d, (models[2], 890), (mysql[0], 890), "Eloquent")
dependency(d, (controllers[2], 680), (fortify[0], 240), "autentica")
dependency(d, (controllers[2], 720), (dompdf[0], 240), "genera PDF")
dependency(d, (vue[2], 215), (lucide[0], 400), "componentes UI")
dependency(d, (dompdf[0]+115, dompdf[3]), (blade[0]+115, blade[1]), "plantillas")
dependency(d, (controllers[2], 702), (storage[0], 702), "archivos")
dependency(d, (env[0], 890), (mysql[2], 890), "configura")

d.text((950, 1050), "Arquitectura verificada con las dependencias y módulos implementados en el proyecto.", fill="#555555", font=f(15), anchor="ma")

path = OUT / "Figura_8_Diagrama_componentes_Emma_Fashion.png"
img.save(path, quality=95)
print(path)
