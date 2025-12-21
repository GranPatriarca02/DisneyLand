# =============================================================================
# MODELO BASE
# =============================================================================
from peewee import Model
from database import db

class BaseModel(Model):
    """Clase base para todos los modelos configura automáticamente la conexión a la base de datos"""
    class Meta:
        database = db
