# -*- coding: utf-8 -*-
# app/__init__.py
# Este archivo sirve para que Python reconozca la carpeta 'app' como un paquete.
# Las inicializaciones de DB ahora están en app/db.py para evitar importaciones circulares.

# Importa los modelos aquí para que Base.metadata.create_all() los detecte.
# No se inicializa la DB aquí, solo se asegura que los modelos sean conocidos.
from app.modelos import proyecto, usuario, reunion
from app.modelos import proyecto, usuario, encuesta
