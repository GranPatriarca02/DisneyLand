# =============================================================================
# MODELO DE VISITANTES
# =============================================================================
from models.base_model import BaseModel
from peewee import *
from playhouse.postgres_ext import BinaryJSONField
from datetime import datetime

class VisitanteModel(BaseModel):
 # Modelo que representa a un visitante del parque
    id = AutoField(primary_key=True)         
    nombre = CharField(null=False)             
    email = CharField(unique=True)             
    altura = IntegerField()                   
    fecha_registro = DateTimeField(default=datetime.now) 
    preferencias = BinaryJSONField(null=True, default={}) 
    
    class Meta:
        table_name = 'visitantes'
