from models.base_model import BaseModel
from models.visitante_model import VisitanteModel
from models.atraccion_model import AtraccionModel
from peewee import *
from playhouse.postgres_ext import BinaryJSONField
from datetime import datetime

class TicketModel(BaseModel):
    id = AutoField(primary_key=True)
    visitante = ForeignKeyField(VisitanteModel, backref='tickets', on_delete='CASCADE')
    atraccion = ForeignKeyField(AtraccionModel, backref='tickets', null=True, on_delete='SET NULL')
    fecha_compra = DateTimeField(default=datetime.now)
    fecha_visita = DateField()
    tipo_ticket = CharField()  # "general", "colegio", "empleado"
    detalles_compra = BinaryJSONField(null=True, default={})
    usado = BooleanField(default=False)
    fecha_uso = DateTimeField(null=True)
    
    class Meta:
        table_name = 'tickets'