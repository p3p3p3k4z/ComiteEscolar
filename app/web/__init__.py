# app/web/__init__.py

from flask import Flask

def create_app():
    """
    Crea y configura la instancia de la aplicación Flask.
    """
    app = Flask(__name__)

    # Puedes cargar configuraciones aquí si las necesitas
    # app.config.from_object('app.config.Config')

    # Importa y registra las rutas de la aplicación web
    from . import routes
    app.register_blueprint(routes.bp)

    return app
