from pathlib import Path

from docx import Document


SOURCE = Path(r"C:\Users\HP\Documents\PERFIL_TESIS_GRADO-Quinaya4.docx")
OUTPUT = Path(r"C:\laragon\www\control_emmafashion\output\PERFIL_TESIS_GRADO-Quinaya4-Marco-Teorico.docx")


TOOLS = [
    (
        "Inertia.js.",
        "Inertia.js es la herramienta que permite integrar Laravel con Vue.js sin separar el proyecto en dos aplicaciones independientes. En el sistema Emma Fashion se utiliza para enviar la información procesada por los controladores de Laravel hacia las páginas desarrolladas en Vue.js, mantener una navegación fluida y actualizar las interfaces sin recargar completamente el navegador.",
    ),
    (
        "Tailwind CSS.",
        "Tailwind CSS es un framework de estilos basado en clases de utilidad. En el proyecto se emplea para diseñar formularios, tablas, tarjetas, menús, botones y vistas adaptables a computadoras y dispositivos móviles. Su utilización facilita la creación de una interfaz uniforme, moderna y acorde con la imagen visual de Emma Fashion.",
    ),
    (
        "Laragon.",
        "Laragon es el entorno de desarrollo local utilizado para ejecutar la aplicación durante su construcción y sus pruebas. Proporciona los servicios necesarios para trabajar con PHP, Laravel y MySQL desde una computadora con Windows, permitiendo iniciar el servidor, administrar la base de datos y verificar el funcionamiento del sistema antes de su publicación.",
    ),
    (
        "Composer.",
        "Composer es el gestor de dependencias utilizado por PHP. En el proyecto permite instalar y administrar Laravel y las bibliotecas requeridas por la aplicación. También mantiene registradas las versiones de los paquetes para que el entorno de desarrollo pueda reproducirse de manera ordenada.",
    ),
    (
        "Node.js y npm.",
        "Node.js proporciona el entorno necesario para procesar las herramientas del frontend, mientras que npm administra los paquetes de JavaScript utilizados por Vue.js, Inertia.js, Tailwind CSS y otros componentes de la interfaz. En Emma Fashion se emplean para instalar dependencias y ejecutar la compilación de los recursos visuales de la aplicación.",
    ),
    (
        "Vite.",
        "Vite es la herramienta de compilación utilizada para procesar los archivos de Vue.js, TypeScript y Tailwind CSS. Durante el desarrollo ofrece una actualización rápida de los cambios y, al preparar la aplicación, genera archivos optimizados para mejorar la carga de las páginas en el navegador.",
    ),
    (
        "Git.",
        "Git es el sistema de control de versiones empleado para registrar los cambios realizados en el código fuente. Su uso permite mantener un historial del desarrollo, identificar modificaciones y recuperar versiones anteriores cuando sea necesario, reduciendo el riesgo de pérdida del trabajo realizado.",
    ),
    (
        "Pest.",
        "Pest es la herramienta de pruebas automatizadas utilizada en el proyecto Laravel. Permite verificar el funcionamiento de procesos como el registro de productos, compras, ventas, inventario, usuarios y permisos. Estas pruebas ayudan a detectar errores y comprobar que las funciones principales continúen operando correctamente después de realizar cambios en el sistema.",
    ),
]


def main() -> None:
    document = Document(SOURCE)

    if any(paragraph.text.strip() == "Inertia.js." for paragraph in document.paragraphs):
        raise RuntimeError("El documento ya contiene la ampliación de herramientas.")

    paragraphs = document.paragraphs
    section_index = next(
        index
        for index, paragraph in enumerate(paragraphs)
        if paragraph.text.strip() == "Herramientas de Desarrollo e Implementación del Proyecto"
    )
    following_paragraph = paragraphs[section_index + 1]
    if not following_paragraph.text.strip():
        following_paragraph.text = (
            "Para el desarrollo e implementación de la aplicación web de Emma Fashion se utilizaron "
            "herramientas de análisis, programación, diseño de interfaces, administración de dependencias, "
            "compilación, control de versiones y pruebas. Estas herramientas permitieron construir los "
            "módulos de productos, compras, ventas, inventario, usuarios, proveedores, clientes y reportes."
        )
        following_paragraph.style = document.styles["Normal"]

    storage_heading = next(
        paragraph
        for paragraph in document.paragraphs
        if paragraph.text.strip() == "Medios de almacenamiento"
    )

    for heading, description in TOOLS:
        storage_heading.insert_paragraph_before(heading, style="Heading 3")
        storage_heading.insert_paragraph_before(description, style="Normal")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
