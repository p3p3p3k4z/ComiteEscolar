# -*- coding: utf-8 -*-
# app/rutas.py

import json
from os import abort
from urllib import response
from flask import Blueprint, render_template, request, redirect, session, url_for, flash, jsonify
from datetime import date , datetime

from app import db
from app.modelos import usuario
from app.servicios.proyecto_servicio import ServicioProyecto
from app.repositorios.proyecto_repo import RepositorioProyecto
from app.servicios.usuario_servicio import ServicioUsuario
from app.repositorios.usuario_repo import RepositorioUsuario
from app.servicios.encuesta_servicio import ServicioEncuesta
from app.repositorios.encuesta_repo import RepositorioEncuesta
from app.db import Session as DBSession

bp_web = Blueprint('web', __name__)

@bp_web.route('/')
def pagina_principal():
    mensaje_bienvenida = "Bienvenido al Sistema de Gestión del Comité de Padres de Familia (SGCPF)."
    return render_template('login/templates/index.html', mensaje=mensaje_bienvenida)

@bp_web.route('/login', methods=['GET', 'POST'])
def login():
    db_session = None
    try:
        db_session = DBSession()
        repositorio_usuarios = RepositorioUsuario(db_session)
        servicio_usuario = ServicioUsuario(repositorio_usuarios)

        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            usuario_autenticado = servicio_usuario.validar_credenciales(email, password)
            if usuario_autenticado:
                flash(f'¡Bienvenido, {usuario_autenticado.nombre}!', 'success')

                if usuario_autenticado.rol == 'PadreDeFamilia':
                    return redirect(url_for('web.dashboard_padre'))
                elif usuario_autenticado.rol == 'Director':
                    return redirect(url_for('web.dashboard_director'))
                elif usuario_autenticado.rol == 'Secretario':
                    return redirect(url_for('web.dashboard_secretario'))
                elif usuario_autenticado.rol == 'Administrador':
                    return redirect(url_for('web.dashboard_admin'))
                elif usuario_autenticado.rol == 'Tesorero':
                    return redirect(url_for('web.dashboard_tesorero'))
                else:
                    flash("Rol de usuario no reconocido. Redirigiendo a la página principal.", "info")
                    return redirect(url_for('web.pagina_principal'))
            else:
                flash('Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.', 'danger')
                return redirect(url_for('web.login'))
    except Exception as e:
        error_message = f"Ocurrió un error al intentar iniciar sesión: {e}"
        print(f"Error en el login: {e}")
        flash(error_message, 'danger')
        return redirect(url_for('web.login'))
    finally:
        if db_session:
            db_session.close()

    return render_template('login/templates/login.html')

@bp_web.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('web.pagina_principal'))

@bp_web.route('/proyectos')
async def lista_proyectos_escolares():
    proyectos_para_html = []
    error_mensaje = None
    db_session = None

    try:
        db_session = DBSession()
        repositorio_proyectos = RepositorioProyecto(db_session)
        repositorio_usuarios = RepositorioUsuario(db_session)
        servicio_proyectos = ServicioProyecto(repositorio_proyectos, repositorio_usuarios)

        proyectos_obtenidos = servicio_proyectos.obtener_todos_los_proyectos()

        for p in proyectos_obtenidos:
            responsable_nombre = "Desconocido"
            if p.id_usuario_responsable and p.usuario_responsable:
                responsable_nombre = f"{p.usuario_responsable.nombre} {p.usuario_responsable.apellido}"

            proyectos_para_html.append({
                "id": p.id,
                "nombre": p.nombre,
                "descripcion": p.nombre,
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
            db_session.close()

    return render_template('web/templates/proyectos.html', proyectos=proyectos_para_html, error=error_mensaje)

@bp_web.route('/proyectos/gestion', methods=['GET', 'POST'])
async def gestion_proyectos():
    """
    Ruta para el panel de gestión de proyectos (CRUD).
    Maneja la visualización del formulario/lista y las operaciones CRUD (Crear, Editar, Eliminar).
    """
    proyectos_para_html = []
    usuarios_data = []
    error_mensaje = None
    success_message = None
    db_session = None

    try:
        db_session = DBSession()
        repositorio_proyectos = RepositorioProyecto(db_session)
        repositorio_usuarios = RepositorioUsuario(db_session)
        servicio_proyectos = ServicioProyecto(repositorio_proyectos, repositorio_usuarios)
        servicio_usuarios = ServicioUsuario(repositorio_usuarios)
        
        if request.method == 'POST':
            operacion = request.form.get('operacion')
            project_id = request.form.get('id_proyecto')

            if operacion == 'crear':
                nombre = request.form['nombre']
                id_usuario_responsable_str = request.form.get('id_usuario_responsable')
                fecha_inicio_str = request.form['fecha_inicio']
                fecha_fin_str = request.form.get('fecha_fin')
                ruta_documento = request.form.get('ruta_documento')

                id_usuario_responsable = int(id_usuario_responsable_str) if id_usuario_responsable_str else None
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else None
                
                try:
                    servicio_proyectos.agregar_proyecto(
                        nombre=nombre,
                        id_usuario_responsable=id_usuario_responsable,
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin,
                        ruta_documento=ruta_documento
                    )
                    success_message = "Proyecto creado exitosamente."
                except ValueError as e:
                    error_mensaje = str(e)
                except Exception as e:
                    error_mensaje = f"Error interno al crear proyecto: {e}"
                    print(f"ERROR al crear proyecto: {e}")


            elif operacion == 'editar':
                if not project_id:
                    error_mensaje = "ID de proyecto no proporcionado para edición."
                else:
                    id_proyecto_int = int(project_id)
                    nombre = request.form.get('nombre')
                    id_usuario_responsable_str = request.form.get('id_usuario_responsable')
                    fecha_inicio_str = request.form.get('fecha_inicio')
                    fecha_fin_str = request.form.get('fecha_fin')
                    ruta_documento = request.form.get('ruta_documento')
                    estado = request.form.get('estado')

                    id_usuario_responsable = int(id_usuario_responsable_str) if id_usuario_responsable_str else None
                    fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else None
                    fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else None

                    try:
                        servicio_proyectos.actualizar_proyecto(
                            id_proyecto=id_proyecto_int,
                            nombre=nombre,
                            id_usuario_responsable=id_usuario_responsable,
                            fecha_inicio=fecha_inicio,
                            fecha_fin=fecha_fin,
                            ruta_documento=ruta_documento,
                            estado=estado
                        )
                        success_message = f"Proyecto con ID {project_id} actualizado exitosamente."
                    except ValueError as e:
                        error_mensaje = str(e)
                    except Exception as e:
                        error_mensaje = f"Error interno al actualizar proyecto: {e}"
                        print(f"ERROR al actualizar proyecto: {e}")

            elif operacion == 'eliminar':
                if not project_id:
                    error_mensaje = "ID de proyecto no proporcionado para eliminar."
                else:
                    try:
                        servicio_proyectos.eliminar_proyecto(int(project_id))
                        success_message = f"Proyecto con ID {project_id} eliminado exitosamente."
                    except ValueError as e:
                        error_mensaje = str(e)
                    except Exception as e:
                        error_mensaje = f"Error interno al eliminar proyecto: {e}"
                        print(f"ERROR al eliminar proyecto: {e}")
            
            # Redirigir para evitar reenvío de formulario y recargar datos
            return redirect(url_for('web.gestion_proyectos', success=success_message, error=error_mensaje))

        # Cargar todos los proyectos y usuarios para la visualización (GET Request)
        proyectos_obtenidos = servicio_proyectos.obtener_todos_los_proyectos()
        usuarios_obtenidos = servicio_usuarios.obtener_todos_los_usuarios()

        usuarios_map = {u.id: f"{u.nombre} {u.apellido}" for u in usuarios_obtenidos}

        for p in proyectos_obtenidos:
            proyectos_para_html.append({
                "id": p.id,
                "nombre": p.nombre,
                "descripcion": p.nombre,
                "fecha_inicio": p.fecha_inicio,
                "fecha_fin": p.fecha_fin,
                "estado": p.estado,
                "responsable_nombre": usuarios_map.get(p.id_usuario_responsable, "Desconocido"),
                "id_usuario_responsable": p.id_usuario_responsable
            })
        
        for u in usuarios_obtenidos:
            usuarios_data.append({
                "id": u.id,
                "nombre": u.nombre,
                "apellido": u.apellido,
                "rol": u.rol
            })

    except Exception as e:
        error_mensaje = f"Error al cargar datos o interactuar con la DB: {e}"
        print(f"ERROR general en gestión de proyectos: {e}")
    finally:
        if db_session:
            db_session.close()

    # Manejar mensajes flash (si se redirigió después de un POST)
    if 'success' in request.args:
        success_message = request.args.get('success')
    if 'error' in request.args:
        error_mensaje = request.args.get('error')

    return render_template('web/templates/proyectos_crud.html',
                           proyectos=proyectos_para_html,
                           usuarios=usuarios_data,
                           error=error_mensaje,
                           success=success_message)



@bp_web.route('/encuestas')
async def encuestas():
    encuestas_para_html = []
    error_mensaje = None
    db_session = None

    try:
        db_session = DBSession()

        repo_encuesta = RepositorioEncuesta(db_session)
        repo_usuario = RepositorioUsuario(db_session)
        servicio_encuesta = ServicioEncuesta(repo_encuesta)

        encuestas_obtenidas = servicio_encuesta.obtener_todas()

        for encuesta in encuestas_obtenidas:
            creador_nombre = "Desconocido"
            if encuesta.creador:
                creador_nombre = f"{encuesta.creador.nombre} {encuesta.creador.apellido}"

            try:
                preguntas_lista = json.loads(encuesta.questions)
                preguntas_texto = "\n".join(f"- {p['question']}" for p in preguntas_lista)
            except Exception as e:
                preguntas_texto = "Error al leer preguntas"

            encuestas_para_html.append({
                "id": encuesta.id,
                "nombre":encuesta.nombre,
                "preguntas": preguntas_texto,
                "fecha_limite": encuesta.deadline_date,
                "fecha_creacion": encuesta.created_at,
                "creador": creador_nombre
            })

    except Exception as e:
        error_mensaje = f"No se pudieron cargar las encuestas: {e}"
        print(f"Error al cargar encuestas en Flask: {e}")

    finally:
        if db_session:
            db_session.close()

    return render_template('web/templates/encuestas.html', encuestas=encuestas_para_html, error=error_mensaje)

@bp_web.route('/encuestas/<int:id>')
def ver_encuesta(id):
    db_session = DBSession()
    encuesta = None
    error_mensaje = None
    preguntas = []

    try:
        repo_encuesta = RepositorioEncuesta(db_session)
        encuesta = repo_encuesta.obtener_por_id(id)

        if not encuesta:
            error_mensaje = "Encuesta no encontrada"
        else:
            # Si preguntas están en formato JSON serializado, las convertimos a lista/diccionario
            preguntas = json.loads(encuesta.questions)

    except Exception as e:
        error_mensaje = f"No se pudo cargar la encuesta: {e}"

    finally:
        db_session.close()

    return render_template('web/templates/ver_encuesta.html',encuesta=encuesta,preguntas=preguntas,error=error_mensaje)

from app.modelos.respuestas import Respuesta 
@bp_web.route('/guardar_respuestas', methods=['POST'])
def guardar_respuestas():
    data = request.form
    survey_id = data.get('survey_id')
    user_id = session.get('usuario_id')  # 

    # Recolectar dinámicamente las respuestas
    respuestas = {}
    for key in data:
        if key.startswith('respuesta_'):
            respuestas[key] = data.get(key)

    if not survey_id or not user_id or not respuestas:
        flash("Faltan datos para guardar la respuesta", "error")
        return redirect(url_for('web.encuestas'))

    try:
        respuestas_json = json.dumps(respuestas)

        nueva_respuesta = Respuesta(
            survey_id=survey_id,
            user_id=user_id,
            response_data=respuestas_json
        )

        db.session.add(nueva_respuesta)
        db.session.commit()

        flash("Respuestas guardadas correctamente", "success")
        return redirect(url_for('web.encuestas'))

    except Exception as e:
        db.session.rollback()
        flash(f"Error al guardar respuestas: {e}", "error")
        return redirect(url_for('web.encuestas'))

@bp_web.route('/bienvenido')
def pagina_bienvenida():
    mensaje = "¡Bienvenido de nuevo al Sistema de Gestión del Comité de Padres de Familia!"
    return render_template('web/templates/index.html', mensaje=mensaje)

@bp_web.route('/dashboard/admin')
def dashboard_admin():
    return render_template('login/templates/sesion_admin.html', message="Bienvenido, Administrador!")

@bp_web.route('/dashboard/padre')
def dashboard_padre():
    return render_template('login/templates/sesion_padre.html', message="Bienvenido, Padre de Familia!")

@bp_web.route('/dashboard/secre')
def dashboard_secretario():
    return render_template('login/templates/sesion_secretario.html', message="Bienvenido, Secretario!")

@bp_web.route('/dashboard/tesorero')
def dashboard_tesorero():
    return render_template('login/templates/sesion_tesorero.html', message="Bienvenido, Tesorero!")

@bp_web.route('/dashboard/director')
def dashboard_director():
    return render_template('login/templates/sesion_director.html', message="Bienvenido, Director!")

@bp_web.route('/debug-rutas')
def debug_rutas():
    """
    Ruta de debug para verificar que las rutas se están registrando correctamente.
    """
    return {"mensaje": "Las rutas web están funcionando correctamente", "rutas_disponibles": ["/", "/proyectos", "/reuniones", "/bienvenido"]}

@bp_web.route('/reuniones')
def pagina_reuniones():
    """
    Ruta para la página de gestión de reuniones.
    """
    return render_template('web/templates/reuniones.html')