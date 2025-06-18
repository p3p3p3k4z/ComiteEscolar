# -*- coding: utf-8 -*-
# run_fastapi.py

import uvicorn
import os

if __name__ == "__main__":
    # Define el directorio de datos de PostgreSQL para excluirlo del reloader.
    # ¡IMPORTANTE: DEBE SER UNA RUTA RELATIVA AL DIRECTORIO DE EJECUCIÓN DEL SCRIPT!
    # Dado que 'run_fastapi.py' y 'pg_data_sgcpf_host' están en la misma raíz,
    # la ruta relativa es simplemente el nombre del directorio.
    directorio_datos_pg_relativo = 'pg_data_sgcpf_host'

    # Ejecuta la aplicación FastAPI usando Uvicorn.
    # Excluimos el directorio de datos de PostgreSQL del monitoreo de recarga
    # para evitar el error de permisos y el error de rutas no relativas.
    uvicorn.run(
        "app.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_excludes=[directorio_datos_pg_relativo] # Ahora es la ruta relativa
    )
