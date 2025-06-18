# -*- coding: utf-8 -*-
# app/web/__init__.py

from flask import Flask
import os

def crear_app_web():
    """
    Crea y configura la instancia de la aplicación web Flask.
    """
    # Define la ruta absoluta a la carpeta de plantillas.
    # Esto es más robusto y evita problemas de "TemplateNotFound".
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    # Puedes cargar configuraciones aquí si las necesitas
    # from app.config import Configuracion
    # app.config.from_object(Configuracion)

    # Importa y registra las rutas de la aplicación web
    # ¡Asegúrate de que el archivo se llama 'rutas.py' en tu sistema de archivos!
    from . import rutas
    app.register_blueprint(rutas.bp_web)

    return app

