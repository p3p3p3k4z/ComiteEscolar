# run_flask.py

from app.login import acceso_sistema

# Crea la instancia de la aplicación Flask
app_flask = acceso_sistema()

if __name__ == '__main__':
    # Ejecuta la aplicación Flask en modo depuración
    # En producción, usarías un servidor WSGI como Gunicorn o uWSGI
    app_flask.run(debug=True, port=5000)