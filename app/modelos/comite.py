# app/modelos/comite.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date
from app.db import Base  # Asume que tienes una clase Base para SQLAlchemy

class Comite(Base):
    __tablename__ = 'committees'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    period = Column(String(50), nullable=False)
    status = Column(String(50), default='activo')