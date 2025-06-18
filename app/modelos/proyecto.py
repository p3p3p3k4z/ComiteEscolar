# app/modelos/proyecto.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.__init__ import Base # Asume que Base está definida en app/__init__.py

class Proyecto(Base):
    """
    Clase de modelo para representar un Proyecto Escolar.
    Mapea a la tabla 'projects' en la base de datos.
    """
    __tablename__ = 'projects' # El nombre de la tabla en la DB generalmente se mantiene en inglés

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), unique=True, nullable=False)
    # id_usuario_responsable del encargado del proyecto, haciendo referencia a la tabla 'users'
    id_usuario_responsable = Column(Integer, ForeignKey('users.id'), nullable=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    # Aunque el documento es un archivo, aquí guardamos una ruta o ID de documento
    # En un sistema más complejo, habría una tabla de documentos con un ID
    ruta_documento = Column(String(255), nullable=True)
    estado = Column(String(50), default='activo', nullable=False) # Ej: 'activo', 'finalizado', 'pendiente', 'aprobado', 'rechazado'

    # Relación con la tabla de usuarios si necesitas acceder al objeto Usuario del encargado
    # from app.modelos.usuario import Usuario # Importación local para evitar circular
    # usuario_responsable = relationship("Usuario", back_populates="proyectos") # Si Usuario también tiene una relación a Proyecto

    def __repr__(self):
        return f"<Proyecto(id={self.id}, nombre='{self.nombre}', estado='{self.estado}')>"

    def establecer_activo(self):
        """Marca el proyecto como activo."""
        self.estado = 'activo'

    def establecer_aprobado(self):
        """Marca el proyecto como aprobado."""
        self.estado = 'aprobado'

    def establecer_rechazado(self):
        """Marca el proyecto como rechazado."""
        self.estado = 'rechazado'
