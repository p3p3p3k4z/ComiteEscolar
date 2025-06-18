# -*- coding: utf-8 -*-
# app/web/__init__.py

from flask import Flask

def crear_app_web():
    """
    Crea y configura la instancia de la aplicación web Flask.
    """
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Puedes cargar configuraciones aquí si las necesitas
    # from app.config import Configuracion
    # app.config.from_object(Configuracion)

    # Importa y registra las rutas de la aplicación web
    # ¡Asegúrate de que el archivo se llama 'rutas.py' en tu sistema de archivos!
    from . import routes
    app.register_blueprint(routes.bp_web)

    return app

