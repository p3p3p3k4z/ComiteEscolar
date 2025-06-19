# -*- coding: utf-8 -*-
# app/rutas.py

import json
from os import abort
from sqlalchemy.sql import text
from urllib import response
from flask import Blueprint, render_template, request, redirect, session, url_for, flash, jsonify
from datetime import date , datetime
from functools import wraps

from app import db
from app.modelos import usuario
from app.servicios.proyecto_servicio import ServicioProyecto
from app.repositorios.proyecto_repo import RepositorioProyecto
from app.servicios.usuario_servicio import ServicioUsuario
from app.repositorios.usuario_repo import RepositorioUsuario

from app.servicios.encuesta_servicio import ServicioEncuesta
from app.repositorios.encuesta_repo import RepositorioEncuesta
from app.repositorios.comite_repo import RepositorioComite
from app.servicios.comite_servicio import ServicioComite
from app.servicios.finanzas_servicios import ServicioFinanciero
from app.repositorios.finanzas_repo import RepositorioFinanzas

from app.db import Session as DBSession
from app.web import crear_app_web


bp_web = Blueprint('web', __name__, url_prefix='/')

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
                session['usuario_id'] = usuario_autenticado.id
                session['usuario_rol']= usuario_autenticado.rol
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
@bp_web.route('/admin/comites', methods=['GET', 'POST'])
def gestion_comites():
    db_session = DBSession()
    try:
        repo_comite = RepositorioComite(db_session)
        servicio_comite = ServicioComite(repo_comite)

        if request.method == 'POST':
            operacion = request.form.get('operacion')
            
            if operacion == 'crear':
                nombre = request.form['nombre']
                periodo = request.form['periodo']
                servicio_comite.crear_comite(nombre, periodo)
                flash('Comité creado exitosamente', 'success')

            elif operacion == 'editar':
                id_comite = int(request.form['id_comite'])
                nombre = request.form.get('nombre')
                status = request.form.get('status')
                servicio_comite.actualizar_comite(id_comite, nombre, status)
                flash('Comité actualizado', 'success')

        comites = repo_comite.obtener_todos()
        return render_template('templates/admin/comites.html', comites=comites)

    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('web.gestion_comites'))
    finally:
        db_session.close()


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

@bp_web.route('/guardar_respuestas', methods=['POST'])
def guardar_respuestas():
    data = request.form
    survey_id = data.get('survey_id')
    user_id = session.get('usuario_id')

    if not survey_id or not user_id:
        flash("Faltan datos para guardar la respuesta", "error")
        return redirect(url_for('web.encuestas'))

    try:
        # Recuperar preguntas de la encuesta para obtener texto completo
        db = DBSession()
        enc = db.execute(text("SELECT questions FROM surveys WHERE id = :id"), {"id": survey_id}).fetchone()
        if not enc:
            flash("Encuesta no encontrada", "error")
            return redirect(url_for('web.encuestas'))

        preguntas = json.loads(enc[0])  # el campo questions

        # Armar diccionario de respuestas legibles
        respuestas = {}
        for i, pregunta in enumerate(preguntas, start=1):
            key = f'respuesta_{i}'
            valor = data.get(key)
            if valor:
                respuestas[pregunta['question']] = valor

        if not respuestas:
            flash("No se respondieron preguntas", "error")
            return redirect(url_for('web.encuestas'))

        respuestas_json = json.dumps(respuestas, ensure_ascii=False)

        # Insertar en base
        insert_query = text("""
            INSERT INTO survey_responses (survey_id, user_id, response_data, responded_at)
            VALUES (:survey_id, :user_id, :response_data, :responded_at)
        """)

        db.execute(insert_query, {
            'survey_id': survey_id,
            'user_id': user_id,
            'response_data': respuestas_json,
            'responded_at': datetime.now()
        })
        db.commit()

        flash("Respuestas guardadas correctamente", "success")
        return redirect(url_for('web.encuestas'))

    except Exception as e:
        db.rollback()
        print("Error al guardar respuestas:", e)
        flash("Error al guardar respuestas", "error")
        return redirect(url_for('web.encuestas'))

    finally:
        db.close()


@bp_web.route('/crear_encuesta', methods=['GET', 'POST'])
def crear_encuesta():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        fecha_limite = request.form.get('fecha_limite')
        usuario_id = session.get('usuario_id')

        if not nombre or not fecha_limite:
            flash("Todos los campos son obligatorios", "error")
            return redirect('/crear_encuesta')

        # Construir preguntas dinámicamente
        preguntas = []
        i = 0
        while True:
            texto = request.form.get(f'pregunta_texto_{i}')
            tipo = request.form.get(f'pregunta_tipo_{i}')
            if not texto or not tipo:
                break  # Ya no hay más preguntas

            pregunta = {
                "question": texto,
                "type": tipo
            }

            if tipo == "radio":
                opciones_raw = request.form.get(f'pregunta_opciones_{i}', '')
                opciones = [o.strip() for o in opciones_raw.split(',') if o.strip()]
                pregunta["options"] = opciones

            preguntas.append(pregunta)
            i += 1

        if not preguntas:
            flash("Debes agregar al menos una pregunta.", "error")
            return redirect('/crear_encuesta')

        preguntas_json = json.dumps(preguntas, ensure_ascii=False)

        try:
            db = DBSession()
            query = text("""
                INSERT INTO surveys (nombre, creator_id, questions, deadline_date, created_at)
                VALUES (:nombre, :creator_id, :questions, :deadline_date, :created_at)
            """)
            db.execute(query, {
                'nombre': nombre,
                'creator_id': usuario_id,
                'questions': preguntas_json,
                'deadline_date': fecha_limite,
                'created_at': datetime.now()
            })
            db.commit()
            flash("Encuesta creada exitosamente", "success")
            return redirect('/crear_encuesta')
        except Exception as e:
            db.rollback()
            print("Error al guardar encuesta:", e)
            flash("Hubo un error al guardar la encuesta.", "error")
        finally:
            db.close()

    return render_template('web/templates/crear_encuestas.html')

@bp_web.route('/validar_usuario')
def validar_usuario():
    usuario_rol = session.get('usuario_rol')
    if usuario_rol == 'PadreDeFamilia':
        return redirect(url_for('web.dashboard_padre'))
    elif usuario_rol == 'Director':
        return redirect(url_for('web.dashboard_director'))
    elif usuario_rol== 'Secretario':
        return redirect(url_for('web.dashboard_secretario'))
    elif usuario_rol == 'Administrador':
        return redirect(url_for('web.dashboard_admin'))
    elif usuario_rol == 'Tesorero':
        return redirect(url_for('web.dashboard_tesorero'))
    else:
        flash("Rol de usuario no reconocido. Redirigiendo a la página principal.", "info")
        return redirect(url_for('web.pagina_principal'))


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


@bp_web.route('/dashboard/director')
def dashboard_director():
    return render_template('login/templates/sesion_director.html', message="Bienvenido, Director!")

@bp_web.route('/debug-rutas')
def debug_rutas():
    """
    Ruta de debug para verificar que las rutas se están registrando correctamente.
    """
    return {"mensaje": "Las rutas web están funcionando correctamente", "rutas_disponibles": ["/", "/proyectos", "/reuniones", "/bienvenido" , "/finanzas"]}

@bp_web.route('/reuniones')
def pagina_reuniones():
    """
    Ruta para la página de gestión de reuniones.
    """
    return render_template('web/templates/reuniones.html')


@bp_web.route('/finanzas/gestion', methods=['GET', 'POST'])
async def gestion_movimientos_financieros():
    """
    Ruta para gestionar (CRUD) los movimientos financieros.
    """
    movimientos_para_html = []
    usuarios_data = []
    error_mensaje = None
    success_message = None
    db_session = None

    try:
        db_session = DBSession()
        repo_finanzas = RepositorioFinanzas(db_session)
        repo_usuarios = RepositorioUsuario(db_session)
        servicio_finanzas = ServicioFinanciero(repo_finanzas, repo_usuarios)
        servicio_usuarios = ServicioUsuario(repo_usuarios)

        if request.method == 'POST':
            operacion = request.form.get('operacion')
            movimiento_id = request.form.get('id_movimiento')

            if operacion == 'crear':
                tipo = request.form.get('tipo')
                monto = float(request.form.get('monto'))
                concepto = request.form.get('concepto')
                fecha_str = request.form.get('fecha')
                id_usuario = int(request.form.get('id_usuario'))

                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

                try:
                    servicio_finanzas.crear_movimiento(
                        tipo=tipo,
                        monto=monto,
                        concepto=concepto,
                        fecha=fecha,
                        id_usuario=id_usuario
                    )
                    success_message = "Movimiento financiero creado correctamente."
                except ValueError as e:
                    error_mensaje = str(e)
                except Exception as e:
                    error_mensaje = f"Error interno al crear movimiento: {e}"

            elif operacion == 'editar':
                if not movimiento_id:
                    error_mensaje = "ID del movimiento no proporcionado."
                else:
                    tipo = request.form.get('tipo')
                    monto = float(request.form.get('monto'))
                    concepto = request.form.get('concepto')
                    fecha_str = request.form.get('fecha')
                    id_usuario = int(request.form.get('id_usuario'))

                    fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

                    try:
                        servicio_finanzas.actualizar_movimiento(
                            id_movimiento=int(movimiento_id),
                            tipo=tipo,
                            monto=monto,
                            concepto=concepto,
                            fecha=fecha,
                            id_usuario=id_usuario
                        )
                        success_message = f"Movimiento con ID {movimiento_id} actualizado exitosamente."
                    except ValueError as e:
                        error_mensaje = str(e)
                    except Exception as e:
                        error_mensaje = f"Error al actualizar movimiento: {e}"

            elif operacion == 'eliminar':
                if not movimiento_id:
                    error_mensaje = "ID del movimiento no proporcionado para eliminar."
                else:
                    try:
                        servicio_finanzas.eliminar_movimiento(int(movimiento_id))
                        success_message = f"Movimiento con ID {movimiento_id} eliminado correctamente."
                    except Exception as e:
                        error_mensaje = f"Error al eliminar movimiento: {e}"

            return redirect(url_for('web.gestion_movimientos_financieros', success=success_message, error=error_mensaje))

        # Cargar datos para la vista GET
        movimientos = servicio_finanzas.obtener_todos_los_movimientos()
        usuarios = servicio_usuarios.obtener_todos_los_usuarios()
        usuarios_map = {u.id: f"{u.nombre} {u.apellido}" for u in usuarios}

        for m in movimientos:
            movimientos_para_html.append({
                "id": m.id,
                "tipo": m.type,
                "monto": m.amount,
                "concepto": m.concept,
                "fecha": m.fecha_transaccion.strftime('%Y-%m-%d'),
                "registrado_por": usuarios_map.get(m.id_usuario, "Desconocido"),
                "id_usuario": m.id_usuario
            })

        for u in usuarios:
            usuarios_data.append({
                "id": u.id,
                "nombre": u.nombre,
                "apellido": u.apellido
            })

    except Exception as e:
        error_mensaje = f"Error general en gestión de finanzas: {e}"
        print(f"ERROR en gestión_movimientos_financieros: {e}")
    finally:
        if db_session:
            db_session.close()

    if 'success' in request.args:
        success_message = request.args.get('success')
    if 'error' in request.args:
        error_mensaje = request.args.get('error')

    return render_template(
        'web/templates/finanzas_crud.html',
        movimientos=movimientos_para_html,
        usuarios=usuarios_data,
        error=error_mensaje,
        success=success_message
    )
