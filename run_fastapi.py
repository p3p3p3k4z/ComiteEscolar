# run_fastapi.py

import uvicorn
from app.api.main import app as fastapi_app

if __name__ == "__main__":
    # Ejecuta la aplicación FastAPI usando Uvicorn
    # 'app.api.main:app' se refiere al objeto 'app' dentro del módulo 'app/api/main.py'
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000, reload=True)

