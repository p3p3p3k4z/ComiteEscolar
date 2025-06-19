# -*- coding: utf-8 -*-
# app/rutas.py

from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from datetime import date
from app.servicios.proyecto_servicio import ServicioProyecto
from app.repositorios.proyecto_repo import RepositorioProyecto
from app.servicios.usuario_servicio import ServicioUsuario
from app.repositorios.usuario_repo import RepositorioUsuario
from app.db import Session as DBSession
from app.web import crear_app_web

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
