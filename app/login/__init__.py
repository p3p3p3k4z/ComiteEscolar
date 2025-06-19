# -*- coding: utf-8 -*-
# app/login/__init__.py

from flask import Flask
import os

def acceso_sistema():
    """
    Crea y configura la instancia de la aplicación web Flask.
    """
    # Define la ruta absoluta a la carpeta de plantillas y estáticos
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  #
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Pasa las rutas absolutas al constructor de Flask
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    app.secret_key = '26d078ca7a9e48c8d6c36590023ee069b306855530a78312e9d21455552cf337'  # NECESARIO para usar `session`

    # Puedes cargar configuraciones aquí si las necesitas
    # from app.config import Configuracion
    # app.config.from_object(Configuracion)
    #app.config['SECRET_KEY'] = '26d078ca7a9e48c8d6c36590023ee069b306855530a78312e9d21455552cf337'

    # Importa y registra las rutas de la aplicación web
    from app import rutas
    app.register_blueprint(rutas.bp_web)

    return app

