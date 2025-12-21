# =============================================================================
#  MODELO DE ATRACCIONES
# =============================================================================
from models.base_model import BaseModel
from peewee import *
from playhouse.postgres_ext import BinaryJSONField
from datetime import datetime

class AtraccionModel(BaseModel):
    # Modelo que representa una atracción del parque
    id = AutoField(primary_key=True)
    nombre = CharField(unique=True, null=False)
    tipo = CharField()  # "extrema", "familiar", "infantil", "acuatica"
    altura_minima = IntegerField()
    detalles = BinaryJSONField(null=True, default={})
    activa = BooleanField(default=True)
    fecha_inauguracion = DateField(default=datetime.now)
    
    class Meta:
        table_name = 'atracciones'