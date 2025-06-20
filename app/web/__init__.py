# -*- coding: utf-8 -*-
# app/web/__init__.py

from flask import Flask
import os

def crear_app_web():
    """
    Crea y configura la instancia de la aplicación web Flask.
    """
    # Define la ruta absoluta a la carpeta de plantillas y estáticos
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

    # Pasa las rutas absolutas al constructor de Flask
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    # Puedes cargar configuraciones aquí si las necesitas
    # from app.config import Configuracion
    # app.config.from_object(Configuracion)

    # Importa y registra las rutas de la aplicación web
    from app import rutas
    app.register_blueprint(rutas.bp_web)

    return app

