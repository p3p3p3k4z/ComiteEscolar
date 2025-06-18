# app/servicios/proyecto_servicio.py

from app.modelos.proyecto import Proyecto
from app.repositorios.proyecto_repo import RepositorioProyecto
from datetime import date
from typing import Optional, List

class ServicioProyecto:
    """
    Clase de Servicio para la lógica de negocio relacionada con los Proyectos.
    Implementa el caso de uso "Agregar Proyecto".
    """
    def __init__(self, repositorio_proyecto: RepositorioProyecto):
        self.repositorio_proyecto = repositorio_proyecto

    def agregar_proyecto(
        self,
        nombre: str,
        id_usuario_responsable: Optional[int],
        fecha_inicio: date,
        fecha_fin: Optional[date],
        ruta_documento: Optional[str]
    ) -> Proyecto:
        """
        Agrega un nuevo proyecto escolar al sistema.
        Implementa la lógica del flujo principal y validaciones.
        """
        # 1. Validaciones de negocio (basado en el alcance y excepciones del caso de uso)
        if not nombre or not fecha_inicio:
            raise ValueError("El nombre del proyecto y la fecha de inicio son obligatorios.")

        if self.repositorio_proyecto.obtener_por_nombre(nombre):
            raise ValueError(f"Ya existe un proyecto con el nombre '{nombre}'.")

        if fecha_fin and fecha_fin < fecha_inicio:
            raise ValueError("La fecha de finalización no puede ser anterior a la fecha de inicio.")

        # Aquí iría la validación de autenticación/permisos del Director,
        # pero eso se manejaría en la capa de la API (middleware o dependencia)
        # o en un servicio de autenticación si fuera más complejo.
        # Por simplicidad, asumimos que la llamada a este servicio ya está autenticada.

        # 2. Creación del objeto Proyecto
        nuevo_proyecto = Proyecto(
            nombre=nombre,
            id_usuario_responsable=id_usuario_responsable,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            ruta_documento=ruta_documento,
            estado='activo' # Por defecto, un nuevo proyecto está activo
        )

        # 3. Persistencia a través del repositorio
        try:
            proyecto_guardado = self.repositorio_proyecto.guardar(nuevo_proyecto)
            # Aquí podrías añadir lógica para enviar notificaciones
            # print(f"Proyecto '{proyecto_guardado.nombre}' agregado y notificado al Director.")
            return proyecto_guardado
        except Exception as e:
            # Aquí manejarías errores específicos de la BD o del guardado
            raise RuntimeError(f"Error al guardar el proyecto en la base de datos: {e}")

    # Otros métodos para ServicioProyecto (ej: actualizar_proyecto, obtener_proyecto, etc.)
    def obtener_proyecto(self, id_proyecto: int) -> Optional[Proyecto]:
        """Obtiene un proyecto por su ID."""
        return self.repositorio_proyecto.obtener_por_id(id_proyecto)

    def obtener_todos_los_proyectos(self) -> List[Proyecto]:
        """Obtiene todos los proyectos."""
        return self.repositorio_proyecto.obtener_todos()

    def actualizar_proyecto(
        self,
        id_proyecto: int,
        nombre: Optional[str] = None,
        id_usuario_responsable: Optional[int] = None,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
        ruta_documento: Optional[str] = None,
        estado: Optional[str] = None
    ) -> Proyecto:
        """Actualiza los datos de un proyecto existente."""
        proyecto_a_actualizar = self.repositorio_proyecto.obtener_por_id(id_proyecto)
        if not proyecto_a_actualizar:
            raise ValueError(f"Proyecto con ID {id_proyecto} no encontrado.")

        if nombre:
            proyecto_existente = self.repositorio_proyecto.obtener_por_nombre(nombre)
            if proyecto_existente and proyecto_existente.id != id_proyecto:
                raise ValueError(f"Ya existe un proyecto con el nombre '{nombre}'.")
            proyecto_a_actualizar.nombre = nombre
        if id_usuario_responsable is not None:
            proyecto_a_actualizar.id_usuario_responsable = id_usuario_responsable
        if fecha_inicio:
            proyecto_a_actualizar.fecha_inicio = fecha_inicio
        if fecha_fin:
            if fecha_inicio and fecha_fin < fecha_inicio:
                raise ValueError("La fecha de finalización no puede ser anterior a la fecha de inicio.")
            proyecto_a_actualizar.fecha_fin = fecha_fin
        if ruta_documento:
            proyecto_a_actualizar.ruta_documento = ruta_documento
        if estado:
            proyecto_a_actualizar.estado = estado

        return self.repositorio_proyecto.actualizar(proyecto_a_actualizar)

    def eliminar_proyecto(self, id_proyecto: int):
        """Elimina un proyecto por su ID."""
        proyecto_a_eliminar = self.repositorio_proyecto.obtener_por_id(id_proyecto)
        if not proyecto_a_eliminar:
            raise ValueError(f"Proyecto con ID {id_proyecto} no encontrado.")
        self.repositorio_proyecto.eliminar(proyecto_a_eliminar)
