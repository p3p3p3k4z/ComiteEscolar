# -*- coding: utf-8 -*-
# app/web/rutas.py

from flask import Blueprint, render_template, request, redirect, session, url_for, flash # Importa request, redirect, url_for, flash
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

# --- Ruta para el inicio de sesión ---
@bp_web.route('/login', methods=['GET', 'POST'])
def login():
    """
    Ruta para el inicio de sesión de usuarios.
    Maneja la visualización del formulario (GET) y el procesamiento de credenciales (POST).
    """
    db_session = None # Inicializar a None
    try:
        # Abre una nueva sesión de base de datos para esta solicitud Flask
        db_session = DBSession()
        
        # Instancia el repositorio y el servicio de usuario con la sesión actual
        repositorio_usuarios = RepositorioUsuario(db_session)
        servicio_usuario = ServicioUsuario(repositorio_usuarios)

        if request.method == 'POST':
            # Obtener datos del formulario de login
            email = request.form['email']  
            password = request.form['password'] 
            usuario_autenticado = servicio_usuario.validar_credenciales(email, password)

            if usuario_autenticado:
                flash(f'¡Bienvenido, {usuario_autenticado.nombre}!', 'success')
                
                if usuario_autenticado.rol == 'PadreDeFamilia':
                    return redirect(url_for('web.dashboard_padre')) # Redirige al dashboard de padre
                elif usuario_autenticado.rol == 'Director':
                    return redirect(url_for('web.dashboard_director')) # Redirige al dashboard de director
                elif usuario_autenticado.rol == 'Secretario':
                    return redirect(url_for('web.dashboard_secretario')) # Redirige al dashboard de secretario
                elif usuario_autenticado.rol == 'Administrador':
                    return redirect(url_for('web.dashboard_admin')) # Redirige al dashboard de administrador
                elif usuario_autenticado.rol == 'Tesorero':
                    return redirect(url_for('web.dashboard_tesorero')) # Redirige al dashboard de tesorero
                else:
                    # rol no existe
                    flash("Rol de usuario no reconocido. Redirigiendo a la página principal.", "info")
                    return redirect(url_for('web.pagina_principal'))
            else:
                # falla de credenciales
                flash('Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.', 'danger')
                return redirect(url_for('web.login')) # Redirige de nuevo al formulario de login

    except Exception as e:
        error_message = f"Ocurrió un error al intentar iniciar sesión: {e}"
        print(f"Error en el login: {e}") # Para depuración
        flash(error_message, 'danger')
        return redirect(url_for('web.login')) # En caso de error, redirige al login
    finally:
        if db_session:
            db_session.close() # Asegúrate de cerrar la sesión de la base de datos

    return render_template('login.html') # Necesitarás crear este archivo HTML

@bp_web.route('/logout')
def logout():
    """
    Cierra la sesión del usuario eliminando todos los datos de la sesión.
    """
    session.clear() # Elimina todos los datos de la sesión
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('web.pagina_principal')) # Redirige de nuevo al formulario de login


#rutas de perfiles
@bp_web.route('/dashboard/admin')
def dashboard_admin():
    return render_template('sesion_admin.html', message="Bienvenido, Administrador!")

@bp_web.route('/dashboard/padre')
def dashboard_padre():
    return render_template('sesion_padre.html', message="Bienvenido, Padre de Familia!")

@bp_web.route('/dashboard/secre')
def dashboard_secretario():
    return render_template('sesion_secretario.html', message="Bienvenido, Secretario!")

@bp_web.route('/dashboard/tesorero')
def dashboard_tesorero():
    return render_template('sesion_tesorero.html', message="Bienvenido, Tesorero!")

@bp_web.route('/dashboard/director')
def dashboard_director():
    return render_template('sesion_director.html', message="Bienvenido, Director!")

