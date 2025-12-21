# =============================================================================
# GESTIÓN DE TABLAS
# =============================================================================
from database import db, conectar_db
from models.visitante_model import VisitanteModel
from models.atraccion_model import AtraccionModel
from models.tickets_model import TicketModel

def crear_tablas():
    """Crea todas las tablas en la base de datos si no existen
    safe=True: no falla si las tablas ya existen"""
    try:
        db.create_tables([VisitanteModel, AtraccionModel, TicketModel], safe=True)
        print("Tablas verificadas exitosamente")
        return True
    except Exception as e:
        print(f"Error al crear tablas: {e}")
        return False

def eliminar_tablas():
    """Elimina todas las tablas el orden de eliminacion es importante"""
    try:
        db.drop_tables([TicketModel, AtraccionModel, VisitanteModel], safe=True)
        print("Tablas eliminadas exitosamente")
        return True
    except Exception as e:
        print(f"Error al eliminar tablas: {e}")
        return False

def reiniciar_tablas():
    """Reinicia completamente la base de datos (elimina y recrea)"""
    eliminar_tablas()
    crear_tablas()
