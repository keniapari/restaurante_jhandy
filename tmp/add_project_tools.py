from copy import deepcopy
from pathlib import Path

from docx import Document


SOURCE = Path(r"C:\laragon\www\control_emmafashion\output\PERFIL_TESIS_GRADO-Quinaya4-Marco-Teorico.docx")
OUTPUT = Path(r"C:\laragon\www\control_emmafashion\output\PERFIL_TESIS_GRADO-Quinaya4-Marco-Teorico-Herramientas.docx")


def insert_paragraph_before(reference, text: str, style_name: str):
    paragraph = deepcopy(reference)
    for child in list(paragraph._p):
        paragraph._p.remove(child)
    reference._p.addprevious(paragraph._p)
    paragraph.style = style_name
    paragraph.add_run(text)
    return paragraph


document = Document(SOURCE)

if any(paragraph.text.strip() == "Laravel Fortify." for paragraph in document.paragraphs):
    document.save(OUTPUT)
    raise SystemExit

git_heading = next(
    paragraph for paragraph in document.paragraphs if paragraph.text.strip() == "Git."
)

new_sections = [
    (
        "TypeScript.",
        "TypeScript es el lenguaje utilizado en la interfaz para complementar JavaScript con tipos de datos. En Emma Fashion permite detectar errores durante el desarrollo de las páginas y componentes de Vue.js, organizar mejor el código y facilitar el mantenimiento de formularios, tablas, menús y módulos administrativos.",
    ),
    (
        "Laravel Fortify.",
        "Laravel Fortify proporciona las funciones de autenticación del sistema. En el proyecto se utiliza para controlar el inicio de sesión, la recuperación de contraseñas, la verificación del correo electrónico y la autenticación en dos pasos, fortaleciendo la seguridad de las cuentas de los usuarios.",
    ),
    (
        "Laravel Socialite.",
        "Laravel Socialite permite integrar el acceso mediante cuentas externas. En Emma Fashion se utiliza para ofrecer el inicio de sesión con Google, simplificando la autenticación del usuario y aprovechando un proveedor confiable para validar su identidad.",
    ),
    (
        "DOMPDF.",
        "DOMPDF es la biblioteca empleada para generar documentos PDF desde la aplicación Laravel. En el sistema permite presentar y descargar reportes de compras y ventas en un formato adecuado para su consulta, impresión y respaldo.",
    ),
]

for heading, body in new_sections:
    insert_paragraph_before(git_heading, heading, "Heading 3")
    insert_paragraph_before(git_heading, body, "Normal")

document.save(OUTPUT)
print(OUTPUT)
