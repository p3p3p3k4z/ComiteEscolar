# -*- coding: utf-8 -*-
# app/web/rutas.py

from flask import Blueprint, render_template
from datetime import date

# Crea un Blueprint para organizar las rutas web
bp_web = Blueprint('web', __name__)

@bp_web.route('/')
def pagina_inicio():
    """
    Ruta para la página de inicio de la aplicación web.
    Ahora mostrará un listado de proyectos escolares.
    """
    # Aquí simulamos una lista de proyectos.
    # En una aplicación real, esto provendría de tu ServicioProyecto (ServicioProyecto.obtener_todos_los_proyectos())
    proyectos_ejemplo = [
        {
            "id": 1,
            "nombre": "Campaña de Reciclaje 'Verde Escuela'",
            "descripcion": "Iniciativa para fomentar el reciclaje de papel y plásticos en toda la escuela.",
            "fecha_inicio": date(2025, 9, 1),
            "fecha_fin": date(2025, 12, 15),
            "estado": "Activo",
            "responsable": "Juan Pérez (Maestro)"
        },
        {
            "id": 2,
            "nombre": "Construcción de Jardín Botánico Escolar",
            "descripcion": "Creación de un espacio verde para el estudio de plantas y recreación.",
            "fecha_inicio": date(2026, 3, 1),
            "fecha_fin": date(2026, 6, 30),
            "estado": "Pendiente",
            "responsable": "María García (Directora)"
        },
        {
            "id": 3,
            "nombre": "Feria de Ciencias Interescolar 2025",
            "descripcion": "Organización de un evento para que los estudiantes presenten sus proyectos científicos.",
            "fecha_inicio": date(2025, 10, 1),
            "fecha_fin": date(2025, 11, 20),
            "estado": "Activo",
            "responsable": "Carlos López (Secretario)"
        }
    ]
    return render_template('inicio.html', proyectos=proyectos_ejemplo)

@bp_web.route('/bienvenido')
def pagina_bienvenida():
    """
    Ruta de ejemplo para una página de bienvenida.
    """
    mensaje = "¡Bienvenido al Sistema de Gestión del Comité de Padres de Familia!"
    return render_template('inicio.html', mensaje_personalizado=mensaje)

