# app/web/routes.py

from flask import Blueprint, render_template

# Crea un Blueprint para organizar las rutas web
bp = Blueprint('web', __name__)

@bp.route('/')
def hello_world():
    """
    Ruta de ejemplo para mostrar "Hola Mundo".
    Renderiza una plantilla simple (que crearemos en la memoria para este ejemplo).
    """
    # En un proyecto real, tendrías un archivo HTML en app/web/templates/
    # Por ahora, simplemente retornamos una cadena HTML.
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hola Mundo Flask</title>
        <link href="[https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css](https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css)" rel="stylesheet">
        <style>
            body {
                font-family: 'Inter', sans-serif;
            }
        </style>
    </head>
    <body class="bg-gray-100 flex items-center justify-center h-screen">
        <div class="bg-white p-8 rounded-lg shadow-md text-center">
            <h1 class="text-3xl font-bold text-gray-800 mb-4">¡Hola Mundo desde Flask!</h1>
            <p class="text-gray-600">Esta es una página de ejemplo de la capa web.</p>
        </div>
    </body>
    </html>
    """