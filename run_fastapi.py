# run_fastapi.py

import uvicorn
import os

if __name__ == "__main__":
    # Define el directorio de datos de PostgreSQL para excluirlo del reloader
    # Asegúrate de que esta ruta sea correcta y que coincida con el volumen en tu docker-compose.yml
    # Es el directorio en tu MÁQUINA LOCAL donde Docker guarda los datos.
    directorio_datos_pg = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pg_data_sgcpf_host')

    # Ejecuta la aplicación FastAPI usando Uvicorn.
    # Excluimos el directorio de datos de PostgreSQL del monitoreo de recarga
    # para evitar el error de permisos.
    # Se usa 'reload_excludes' (en plural) para compatibilidad con Uvicorn.
    uvicorn.run(
        "app.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_excludes=[directorio_datos_pg] # ¡CORREGIDO: Ahora es 'reload_excludes'!
    )
