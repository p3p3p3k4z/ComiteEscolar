# -*- coding: utf-8 -*-
# app/servicios/reunion_servicio.py

from app.modelos.reunion import Reunion, MiembroReunion, Notificacion, Acta
from app.repositorios.reunion_repo import (
    RepositorioReunion, RepositorioMiembroReunion, 
    RepositorioNotificacion, RepositorioActa
)
from app.repositorios.usuario_repo import RepositorioUsuario
from datetime import date, time, datetime
from typing import Optional, List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

class ServicioReunion:
    """
    Servicio para la lógica de negocio de Reuniones.
    """
    def __init__(
        self, 
        repo_reunion: RepositorioReunion,
        repo_miembro_reunion: RepositorioMiembroReunion,
        repo_notificacion: RepositorioNotificacion,
        repo_acta: RepositorioActa,
        repo_usuario: RepositorioUsuario
    ):
        self.repo_reunion = repo_reunion
        self.repo_miembro_reunion = repo_miembro_reunion
        self.repo_notificacion = repo_notificacion
        self.repo_acta = repo_acta
        self.repo_usuario = repo_usuario

    def programar_reunion(
        self,
        fecha: date,
        hora: time,
        lugar: str,
        agenda: Optional[str],
        miembros_solicitados: List[int]
    ) -> Reunion:
        """
        Programa una nueva reunión del Comité Escolar.
        """
        # Validaciones
        if fecha < date.today():
            raise ValueError("La fecha de la reunión no puede ser anterior a hoy.")
        
        if not lugar.strip():
            raise ValueError("El lugar de la reunión es obligatorio.")
        
        if not miembros_solicitados:
            raise ValueError("Debe invitar al menos un miembro a la reunión.")

        # Verificar que los miembros existen
        for id_miembro in miembros_solicitados:
            usuario = self.repo_usuario.obtener_por_id(id_miembro)
            if not usuario:
                raise ValueError(f"El usuario con ID {id_miembro} no existe.")

        # Crear la reunión
        nueva_reunion = Reunion(
            fecha=fecha,
            hora=hora,
            lugar=lugar,
            agenda=agenda,
            estado='Programada'
        )

        # Guardar la reunión
        reunion_guardada = self.repo_reunion.guardar(nueva_reunion)

        # Agregar miembros a la reunión
        for id_miembro in miembros_solicitados:
            miembro_reunion = MiembroReunion(
                id_reunion=reunion_guardada.id,
                id_miembro=id_miembro
            )
            self.repo_miembro_reunion.agregar_miembro(miembro_reunion)

        # Enviar notificación de confirmación
        self.enviar_notificacion(
            reunion_guardada.id,
            'confirmacion',
            f"Se ha programado una reunión para el {fecha} a las {hora} en {lugar}."
        )

        return reunion_guardada

    def enviar_notificacion(
        self,
        id_reunion: int,
        tipo: str,
        mensaje_personalizado: Optional[str] = None
    ) -> bool:
        """
        Envía notificaciones por correo electrónico sobre la reunión.
        """
        reunion = self.repo_reunion.obtener_por_id(id_reunion)
        if not reunion:
            raise ValueError(f"Reunión con ID {id_reunion} no encontrada.")

        # Obtener miembros de la reunión
        miembros = self.repo_miembro_reunion.obtener_miembros_por_reunion(id_reunion)
        
        # Generar mensaje según el tipo
        if mensaje_personalizado:
            mensaje = mensaje_personalizado
        else:
            mensaje = self._generar_mensaje_notificacion(reunion, tipo)

        # Crear notificación en la base de datos
        notificacion = Notificacion(
            id_reunion=id_reunion,
            tipo=tipo,
            mensaje=mensaje
        )
        self.repo_notificacion.guardar(notificacion)

        # Enviar correos (simulado - en producción usarías un servicio real)
        try:
            for miembro in miembros:
                usuario = self.repo_usuario.obtener_por_id(miembro.id_miembro)
                if usuario and usuario.email:
                    self._enviar_correo_simulado(usuario.email, tipo, mensaje)
            return True
        except Exception as e:
            print(f"Error al enviar notificaciones: {e}")
            return False

    def registrar_acta(
        self,
        id_reunion: int,
        contenido: str,
        generar_pdf: bool = True
    ) -> Acta:
        """
        Registra el acta de una reunión y opcionalmente genera el PDF.
        """
        reunion = self.repo_reunion.obtener_por_id(id_reunion)
        if not reunion:
            raise ValueError(f"Reunión con ID {id_reunion} no encontrada.")

        if not contenido.strip():
            raise ValueError("El contenido del acta es obligatorio.")

        # Verificar si ya existe un acta
        acta_existente = self.repo_acta.obtener_por_reunion(id_reunion)
        
        archivo_pdf = None
        if generar_pdf:
            archivo_pdf = self._generar_pdf_acta(reunion, contenido)

        if acta_existente:
            # Actualizar acta existente
            acta_existente.contenido = contenido
            acta_existente.archivo_pdf = archivo_pdf
            return self.repo_acta.actualizar(acta_existente)
        else:
            # Crear nueva acta
            nueva_acta = Acta(
                id_reunion=id_reunion,
                contenido=contenido,
                archivo_pdf=archivo_pdf
            )
            return self.repo_acta.guardar(nueva_acta)

    def exportar_pdf(self, id_reunion: int) -> Optional[str]:
        """
        Exporta el acta de una reunión en formato PDF.
        """
        acta = self.repo_acta.obtener_por_reunion(id_reunion)
        if not acta:
            raise ValueError(f"No se encontró acta para la reunión con ID {id_reunion}.")

        if acta.archivo_pdf and os.path.exists(acta.archivo_pdf):
            return acta.archivo_pdf
        else:
            # Regenerar PDF si no existe
            reunion = self.repo_reunion.obtener_por_id(id_reunion)
            archivo_pdf = self._generar_pdf_acta(reunion, acta.contenido)
            acta.archivo_pdf = archivo_pdf
            self.repo_acta.actualizar(acta)
            return archivo_pdf

    def obtener_reunion(self, id_reunion: int) -> Optional[Reunion]:
        """Obtiene una reunión por su ID."""
        return self.repo_reunion.obtener_por_id(id_reunion)

    def obtener_todas_reuniones(self) -> List[Reunion]:
        """Obtiene todas las reuniones."""
        return self.repo_reunion.obtener_todas()

    def actualizar_reunion(
        self,
        id_reunion: int,
        fecha: Optional[date] = None,
        hora: Optional[time] = None,
        lugar: Optional[str] = None,
        agenda: Optional[str] = None,
        estado: Optional[str] = None,
        miembros_solicitados: Optional[List[int]] = None
    ) -> Reunion:
        """Actualiza una reunión existente."""
        reunion = self.repo_reunion.obtener_por_id(id_reunion)
        if not reunion:
            raise ValueError(f"Reunión con ID {id_reunion} no encontrada.")

        # Actualizar campos
        if fecha:
            if fecha < date.today() and reunion.estado == 'Programada':
                raise ValueError("La fecha de la reunión no puede ser anterior a hoy.")
            reunion.fecha = fecha
        if hora:
            reunion.hora = hora
        if lugar:
            reunion.lugar = lugar
        if agenda is not None:
            reunion.agenda = agenda
        if estado:
            reunion.estado = estado

        # Actualizar miembros si se proporcionan
        if miembros_solicitados is not None:
            # Eliminar miembros actuales
            self.repo_miembro_reunion.eliminar_miembros_reunion(id_reunion)
            # Agregar nuevos miembros
            for id_miembro in miembros_solicitados:
                usuario = self.repo_usuario.obtener_por_id(id_miembro)
                if not usuario:
                    raise ValueError(f"El usuario con ID {id_miembro} no existe.")
                miembro_reunion = MiembroReunion(
                    id_reunion=id_reunion,
                    id_miembro=id_miembro
                )
                self.repo_miembro_reunion.agregar_miembro(miembro_reunion)

        reunion_actualizada = self.repo_reunion.actualizar(reunion)

        # Enviar notificación de modificación
        self.enviar_notificacion(
            id_reunion,
            'modificacion',
            f"La reunión del {reunion.fecha} ha sido modificada."
        )

        return reunion_actualizada

    def cancelar_reunion(self, id_reunion: int) -> Reunion:
        """Cancela una reunión."""
        reunion = self.repo_reunion.obtener_por_id(id_reunion)
        if not reunion:
            raise ValueError(f"Reunión con ID {id_reunion} no encontrada.")

        reunion.estado = 'Cancelada'
        reunion_actualizada = self.repo_reunion.actualizar(reunion)

        # Enviar notificación de cancelación
        self.enviar_notificacion(
            id_reunion,
            'cancelacion',
            f"La reunión del {reunion.fecha} ha sido cancelada."
        )

        return reunion_actualizada

    def _generar_mensaje_notificacion(self, reunion: Reunion, tipo: str) -> str:
        """Genera el mensaje de notificación según el tipo."""
        mensajes = {
            'confirmacion': f"Reunión confirmada para el {reunion.fecha} a las {reunion.hora} en {reunion.lugar}.",
            'recordatorio': f"Recordatorio: Reunión el {reunion.fecha} a las {reunion.hora} en {reunion.lugar}.",
            'modificacion': f"La reunión del {reunion.fecha} ha sido modificada.",
            'cancelacion': f"La reunión del {reunion.fecha} ha sido cancelada."
        }
        return mensajes.get(tipo, "Notificación de reunión.")

    def _enviar_correo_simulado(self, email: str, tipo: str, mensaje: str):
        """Simula el envío de correo electrónico."""
        print(f"[CORREO SIMULADO] Para: {email}")
        print(f"[CORREO SIMULADO] Tipo: {tipo}")
        print(f"[CORREO SIMULADO] Mensaje: {mensaje}")
        print("=" * 50)

    def _generar_pdf_acta(self, reunion: Reunion, contenido: str) -> str:
        """Genera un archivo PDF con el acta de la reunión."""
        # Crear directorio si no existe
        pdf_dir = "actas_pdf"
        os.makedirs(pdf_dir, exist_ok=True)
        
        # Nombre del archivo
        nombre_archivo = f"acta_reunion_{reunion.id}_{reunion.fecha}.pdf"
        ruta_archivo = os.path.join(pdf_dir, nombre_archivo)
        
        # Crear PDF
        c = canvas.Canvas(ruta_archivo, pagesize=letter)
        width, height = letter
        
        # Título
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "ACTA DE REUNIÓN")
        
        # Información de la reunión
        c.setFont("Helvetica", 12)
        y_position = height - 100
        c.drawString(50, y_position, f"Fecha: {reunion.fecha}")
        y_position -= 20
        c.drawString(50, y_position, f"Hora: {reunion.hora}")
        y_position -= 20
        c.drawString(50, y_position, f"Lugar: {reunion.lugar}")
        y_position -= 40
        
        # Contenido del acta
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_position, "CONTENIDO:")
        y_position -= 30
        
        c.setFont("Helvetica", 10)
        # Dividir el contenido en líneas para que quepa en la página
        lines = contenido.split('\n')
        for line in lines:
            if y_position < 50:  # Nueva página si es necesario
                c.showPage()
                y_position = height - 50
            c.drawString(50, y_position, line[:80])  # Limitar caracteres por línea
            y_position -= 15
        
        c.save()
        return ruta_archivo
