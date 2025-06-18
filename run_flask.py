# -*- coding: utf-8 -*-
# run_flask.py

from app.web import crear_app_web

# Crea la instancia de la aplicación Flask
app_flask = crear_app_web()

if __name__ == '__main__':
    # Ejecuta la aplicación Flask en modo depuración
    # En producción, usarías un servidor WSGI como Gunicorn o uWSGI
    # Usa un puerto diferente al de FastAPI (8000), por ejemplo 5000.
    # Con 'Flask[async]' instalado, esto manejará las vistas async def.
    app_flask.run(debug=True, port=5000)

