# -*- coding: utf-8 -*-
# app/web/rutas.py

from flask import Blueprint, render_template
from datetime import date
# Importaciones necesarias para interactuar con el servicio de proyectos desde Flask
from app.servicios.proyecto_servicio import ServicioProyecto
from app.repositorios.proyecto_repo import RepositorioProyecto
from app.servicios.usuario_servicio import ServicioUsuario
from app.repositorios.usuario_repo import RepositorioUsuario
from app.db import Session as DBSession # Importar Session desde app.db


# Crea un Blueprint para organizar las rutas web
bp_web = Blueprint('web', __name__)

@bp_web.route('/')
def pagina_principal():
    """
    Ruta principal (raíz) de la aplicación web.
    Esta será la página de inicio general, renderizando 'index.html'.
    """
    mensaje_bienvenida = "Bienvenido al Sistema de Gestión del Comité de Padres de Familia (SGCPF)."
    return render_template('index.html', mensaje=mensaje_bienvenida)

@bp_web.route('/proyectos')
async def lista_proyectos_escolares(): # Marcado como async para compatibilidad con Flask[async]
    """
    Ruta para la página que lista los proyectos escolares.
    Obtiene los datos de proyectos directamente de la base de datos a través del servicio.
    """
    proyectos_para_html = []
    error_mensaje = None
    db_session = None # Inicializar a None

    try:
        # Abre una nueva sesión de base de datos para esta solicitud Flask
        db_session = DBSession()
        repositorio_proyectos = RepositorioProyecto(db_session)
        repositorio_usuarios = RepositorioUsuario(db_session)
        servicio_proyectos = ServicioProyecto(repositorio_proyectos, repositorio_usuarios)

        # Obtiene los proyectos de la base de datos
        # No se usa 'await' aquí porque los métodos del servicio son síncronos.
        proyectos_obtenidos = servicio_proyectos.obtener_todos_los_proyectos()

        # Prepara los datos para la plantilla Flask
        for p in proyectos_obtenidos:
            responsable_nombre = "Desconocido"
            if p.id_usuario_responsable:
                # Accede al atributo 'usuario_responsable' cargado por la relación ORM
                if p.usuario_responsable:
                    responsable_nombre = f"{p.usuario_responsable.nombre} {p.usuario_responsable.apellido}"
            
            proyectos_para_html.append({
                "id": p.id,
                "nombre": p.nombre,
                "descripcion": p.nombre, # Usar el nombre como descripción simple por ahora
                "fecha_inicio": p.fecha_inicio,
                "fecha_fin": p.fecha_fin,
                "estado": p.estado,
                "responsable": responsable_nombre
            })
    except Exception as e:
        error_mensaje = f"No se pudieron cargar los proyectos: {e}"
        print(f"Error al cargar proyectos en Flask: {e}")
    finally:
        if db_session:
            db_session.close() # Asegúrate de cerrar la sesión de la base de datos

    return render_template('proyectos.html', proyectos=proyectos_para_html, error=error_mensaje)

@bp_web.route('/bienvenido')
def pagina_bienvenida():
    """
    Ruta para la página de bienvenida genérica.
    Renderiza 'index.html' con un mensaje personalizado.
    """
    mensaje = "¡Bienvenido de nuevo al Sistema de Gestión del Comité de Padres de Familia!"
    return render_template('index.html', mensaje=mensaje)

# Puedes añadir más rutas aquí si es necesario
