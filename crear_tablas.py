from database import db, conectar_db
from models.visitante_model import VisitanteModel
from models.atraccion_model import AtraccionModel
from models.tickets_model import TicketModel

def crear_tablas():
    """Crear todas las tablas en la base de datos"""
    try:
        conectar_db()
        db.create_tables([VisitanteModel, AtraccionModel, TicketModel], safe=True)
        print("Tablas creadas exitosamentee")
        return True
    except Exception as e:
        print(f"Error al crear tablas: {e}")
        return False

def eliminar_tablas():
    """Eliminar todas las tablas (usar con precaución)"""
    try:
        conectar_db()
        db.drop_tables([TicketModel, AtraccionModel, VisitanteModel], safe=True)
        print("Tablas eliminadas exitosamente")
        return True
    except Exception as e:
        print(f"Error al eliminar tablas: {e}")
        return False

def reiniciar_tablas():
    """Eliminar y crear de nuevo las tablas"""
    eliminar_tablas()
    crear_tablas()

if __name__ == "__main__":
    crear_tablas()