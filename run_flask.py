# run_flask.py

from app.web import create_app

# Crea la instancia de la aplicación Flask
app = create_app()

if __name__ == '__main__':
    # Ejecuta la aplicación Flask en modo depuración
    # En producción, usarías un servidor WSGI como Gunicorn o uWSGI
    app.run(debug=True, port=5000)