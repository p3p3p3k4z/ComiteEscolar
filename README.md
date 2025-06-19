# Comite Escolar

###Importante!!!
crear un .env

### Docker
En caso de reiniciar, si es la primera vez ignorar las primeras 2 lineas

```bash
docker compose down -v # Detiene y elimina contenedores, redes y volúmenes (reinicia la DB desde cero)
sudo rm -rf pg_data_sgcpf_host/   ##Importante por si e cambio la base

docker compose up -d --build   # Levanta los servicios Docker docker compose up -d --build
sleep 60 #Esto lo pongo porque el docker tarda en levanrse con docker ps se puede checar eso
sudo chmod -R 777 pg_data_sgcpf_host/ *

```
Una vez levantada la base ya puedes continuar ...

**Variables de Entorno:**
    Crea un archivo `.env` en la raíz de tu proyecto y configura la URL de la base de datos (PostgreSQL).

```bash
DATABASE_URL=postgresql://sgcpf_user:sgcpf_password@localhost:5432/sgcpf_db
```

## Cómo ejecutar la aplicación

### Entorno Virtual 

1.  **Navega al directorio raíz del proyecto en tu terminal.**
2.  **Crea un entorno virtual:**

    ```bash
    python3 -m venv venv
    ```

3.  **Activa el entorno virtual:**

    ```bash
    source venv/bin/activate
    ```

4.  **Instala las dependencias necesarias:**

    ```bash
    pip install "Flask[async]" FastAPI "uvicorn[standard]" SQLAlchemy psycopg2-binary python-dotenv requests pytest httpx black isort flake8
    ```
    o tambien 
    
    ```bash
    pip install -r requirements.txt
    ```


### API Web (FastAPI)

1.  **Asegúrate de tener el entorno virtual activado.**
2.  **Navega al directorio raíz del proyecto **
3.  **Ejecuta el servidor FastAPI con el siguiente comando:**

    ```bash
    uvicorn api.main:app --reload
    ```
    o tambien
    
    ```bash
    python3 run_fastapi.py
    ```

### Interfaz Web (Flask)

1.  **Asegúrate de tener el entorno virtual activado.**
2.   **Navega al directorio raíz del proyecto .**
3.  **Ejecuta la aplicación Flask:**

    ```bash
    flask --app web/app.py run --debug
    ```
    o tambien
    
     ```bash
    python3 run_flask.py
    ```

    La interfaz web estará disponible en `http://127.0.0.1:5000` (por defecto). 

---

### 🗄️ Gestión de la Base de Datos con pgAdmin

Una vez que docker compose up -d esté en ejecución, puedes acceder a pgAdmin en http://localhost:8085 

Para conectar PgAdmin a tu base de datos PostgreSQL del proyecto SGCPF, sigue estos pasos:

    Asegúrate de que PgAdmin esté corriendo (si lo tienes en Docker Compose, verifica que su contenedor esté levantado junto con el de la base de datos).

    Una vez en la interfaz de PgAdmin, haz clic en "Add New Server" (o "Registrar nuevo servidor" / "Agregar nuevo servidor").

    En la pestaña "General":

        Name: SGCPF Database (o el nombre que prefieras para identificar esta conexión, por ejemplo, Comite Escolar DB).

    En la pestaña "Connection":

        Host name/address: sgcpf_db
        
        Port: 5432 (Este es el puerto por defecto de PostgreSQL).

        Maintenance database: sgcpf_db (Este es el nombre de la base de datos a la que te quieres conectar, según tu init.sql).

        Username: sgcpf_user (Tu usuario de base de datos definido en docker-compose.yml).

        Password: sgcpf_password (Tu contraseña de base de datos definida en docker-compose.yml).

        Marca "Save password?" para no tener que introducirla cada vez.

    Haz clic en "Save" (o "Guardar").
    
--

## Propuesta de estructura del proyecto

```bash
sgcpf/
├── app/
│   ├── __init__.py
│   ├── config.py                 # Configuración de la aplicación (DB, JWT, etc.)
│   ├── modelos/                   # Capa de Dominio/Modelos de Negocio (POO)
│   │   ├── __init__.py
│   │   ├── user.py               # Clase Usuario, Administrador, Tesorero, etc.
│   │   ├── committee.py          # Clase Comite
│   │   ├── project.py            # Clase Proyecto, ProyectoInfraestructura
│   │   ├── meeting.py            # Clase Reunion, ActaReunion, Asistencia
│   │   ├── financial.py          # Clase Movimiento (Ingreso/Egreso), Transaccion, ReporteFinanciero
│   │   ├── event.py              # Clase Evento
│   │   ├── survey.py             # Clase Encuesta
│   │   ├── proposal.py           # Clase Propuesta, Queja, Votacion
│   │   └── document.py           # Clase Documento
│   │
│   ├── servicios/               
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── committee_service.py
│   │   ├── project_service.py
│   │   ├── meeting_service.py
│   │   ├── financial_service.py
│   │   ├── event_service.py
│   │   ├── survey_service.py
│   │   ├── proposal_service.py
│   │   └── document_service.py
│   │
│   ├── repositorios/             # Capa de Persistencia (DAOs/Repositorios)
│   │   ├── __init__.py
│   │   ├── base_repository.py    # Clase base para operaciones CRUD genéricas
│   │   ├── user_repository.py
│   │   ├── committee_repository.py
│   │   ├── project_repository.py
│   │   ├── meeting_repository.py
│   │   ├── financial_repository.py
│   │   ├── event_repository.py
│   │   ├── survey_repository.py
│   │   ├── proposal_repository.py
│   │   └── document_repository.py
│   │
│   ├── api/                      # Capa de Presentación (FastAPI - API RESTful)
│   │   ├── __init__.py
│   │   ├── main.py               # Instancia de FastAPI y routers principales
│   │   ├── dependencies.py       # Dependencias para autenticación, inyección de repositorios, etc.
│   │   ├── auth.py               # Rutas de autenticación
│   │   ├── users.py              # Rutas para gestión de usuarios
│   │   ├── committees.py         # Rutas para gestión de comités
│   │   ├── projects.py           # Rutas para gestión de proyectos
│   │   ├── meetings.py           # Rutas para gestión de reuniones
│   │   ├── financials.py         # Rutas para gestión financiera
│   │   ├── events.py             # Rutas para gestión de eventos
│   │   ├── surveys.py            # Rutas para gestión de encuestas
│   │   ├── proposals.py          # Rutas para gestión de propuestas/quejas
│   │   └── documents.py          # Rutas para gestión de documentos
│   │
│   ├── web/                      # Capa de Presentación (Flask - Frontend Web)
│   │   ├── __init__.py
│   │   ├── routes.py             # Rutas de Flask para vistas HTML (si aplica SSR)
│   │   ├── templates/            # Plantillas HTML (Jinja2)
│   │   │   ├── base.html
│   │   │   ├── index.html
│   │   │   └── ...
│   │   └── static/               # Archivos estáticos (CSS, JS, imágenes)
│   │       ├── css/
│   │       ├── js/
│   │       └── img/
│   │
│   └── utils/                    # Utilidades y funciones auxiliares
│       ├── __init__.py
│       ├── security.py           # Hashing de contraseñas, JWT (si no se usa FastAPI auth directamente)
│       ├── validators.py         # Funciones de validación de datos
│       └── notifications.py      # Envío de correos electrónicos, etc.
│
├── tests/                        # Pruebas unitarias e integración
│   ├── unit/
│   ├── integration/
│   └── test_main.py
│
├── venv/                         # Entorno virtual
├── .env                          # Variables de entorno
├── requirements.txt              # Dependencias del proyecto
├── run_flask.py                  # Script para iniciar la aplicación Flask
├── run_fastapi.py                # Script para iniciar la aplicación FastAPI
└── README.md                     
```

---

## Minitutorial de Github
Github es una herramienta que nos permite la documentación y control de versiones del código

#### Obtén el repositorio
Esto nos ayuda a obtener todo el repositorio en nuestra PC personal y poder tener acceso al código
```bash
git clone https://github.com/p3p3p3k4z/CompiladorEq5.git
```
#### Crea tu Primer Commit
Esto te ayudara a poder subir tus cambios o tu código a github. Recuerda hacer esto en la carpeta donde esta tu espacio de trabajo

**1.Inicia Git**
```bash
git init
```

**2.Añadir archivos**
Añade todos los archivos de tu espacio de trabajo
```bash
git add .
```
Añade un archivo
```bash
git add main.py
```
Añade una carpeta
```bash
git add carpeta/
```

**3.Hacer tu commit**
Aquí darás un breve mensaje que fue lo que cambiaste
```bash
git commit -m "archivos corregidos"
```

**4.Añadir el repositorio**
```bash
git remote add origin https://github.com/p3p3p3k4z/CompiladorEq5.git
```
si se equivoca con el repositorio
git remote set-url origin https://github.com/p3p3p3k4z/CompiladorEq5.git
```bash
git remote set-url origin https://github.com/p3p3p3k4z/CompiladorEq5.git
```

**5.Subir tus cambios**
```bash
git push -u origin main
```
En caso de Fallas
```bash
git push -u origin main --force
```

A continuación te pedirá tu usuario, después tu contraseña o llave.
Felicidades!!! Ya sabes usar github

#### Hacer cambios
```bash
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

#### Recibir cambios
Cuando alguien actualiza su codigo es necesario recibir el codigo mas actualizado
```bash
git pull origin main
```
#### Regresar a una version anterior
```bash
git clone <url-del-repositorio>
git checkout version_1
git log --oneline
git reset --hard <commit-id>
git push --force origin version_1
```
#### Crear una nueva rama
```bash
git checkout -b <nombre-de-la-nueva-rama>
git push origin <rama_creada>
```

### Mezclar ramas
```bash
git checkout main
git pull origin main
git merge AgregarProyecto
git push origin main
```
#### General llave
Esto es en caso de no admitir la contraseña
<https://github.com/settings/tokens>
