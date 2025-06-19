from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, func
from app.db import Base

class Respuesta(Base):
    __tablename__ = 'survey_responses'

    survey_id = Column(Integer, ForeignKey('surveys.id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    response_data = Column(Text, nullable=False)  # JSON guardado como texto
    responded_at = Column(DateTime(timezone=True), server_default=func.now())
