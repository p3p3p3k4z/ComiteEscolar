# -*- coding: utf-8 -*-
# debug_flask.py - Script para debuggear las rutas de Flask

from app.web import crear_app_web

# Crea la instancia de la aplicación Flask
app_flask = crear_app_web()

if __name__ == '__main__':
    # Imprime todas las rutas registradas
    print("=== RUTAS REGISTRADAS EN FLASK ===")
    for rule in app_flask.url_map.iter_rules():
        print(f"Ruta: {rule.rule} -> Función: {rule.endpoint}")
    print("=" * 40)
    
    # Ejecuta la aplicación
    print("Iniciando servidor Flask en http://127.0.0.1:5000")
    app_flask.run(debug=True, port=5000)
