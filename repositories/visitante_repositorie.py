from models.visitante_model import VisitanteModel
from peewee import *
from playhouse.postgres_ext import *

class VisitanteRepositorie:
    
    @staticmethod
    def crear_visitante(nombre, email, altura=None, preferencias=None):
        """Crear un nuevo visitante"""
        try:
            visitante = VisitanteModel.create(
                nombre=nombre,
                email=email,
                altura=altura,
                preferencias=preferencias or {}
            )
            return visitante
        except Exception as e:
            print(f"Error al crear visitante: {e}")
            return None
    
    @staticmethod
    def obtener_todos_visitantes():
        """Obtener todos los visitantes"""
        try:
            return list(VisitanteModel.select())
        except Exception as e:
            print(f"Error al obtener visitantes: {e}")
            return []
    
    @staticmethod
    def obtener_visitante_por_id(visitante_id):
        """Obtener un visitante por ID"""
        try:
            return VisitanteModel.get_by_id(visitante_id)
        except Exception as e:
            print(f"Error al obtener visitante: {e}")
            return None
    
    @staticmethod
    def obtener_visitante_por_email(email):
        """Obtener un visitante por email"""
        try:
            return VisitanteModel.get(VisitanteModel.email == email)
        except Exception as e:
            print(f"Error al obtener visitante: {e}")
            return None
    
    @staticmethod
    def eliminar_visitante(visitante_id):
        """Eliminar un visitante (y sus tickets en cascada)"""
        try:
            visitante = VisitanteModel.get_by_id(visitante_id)
            visitante.delete_instance()
            return True
        except Exception as e:
            print(f"Error al eliminar visitante: {e}")
            return False
    
    @staticmethod
    def visitantes_con_preferencia_extrema():
        """Visitantes con preferencia por atracciones extremas"""
        try:
            return list(VisitanteModel.select().where(
                VisitanteModel.preferencias['tipo_favorito'].cast('text') == '"extrema"'
            ))
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @staticmethod
    def visitantes_con_problemas_cardiacos():
        """Visitantes con problemas cardíacos en restricciones"""
        try:
            return list(VisitanteModel.select().where(
                VisitanteModel.preferencias['restricciones'].cast('text').contains('problemas_cardiacos')
            ))
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @staticmethod
    def eliminar_restriccion(visitante_id, restriccion):
        """Eliminar una restricción del array de restricciones"""
        try:
            visitante = VisitanteModel.get_by_id(visitante_id)
            preferencias = visitante.preferencias or {}
            restricciones = preferencias.get('restricciones', [])
            
            if restriccion in restricciones:
                restricciones.remove(restriccion)
                preferencias['restricciones'] = restricciones
                visitante.preferencias = preferencias
                visitante.save()
                return True
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    @staticmethod
    def agregar_visita_historial(visitante_id, fecha, atracciones_visitadas):
        """Añadir una nueva visita al historial"""
        try:
            visitante = VisitanteModel.get_by_id(visitante_id)
            preferencias = visitante.preferencias or {}
            historial = preferencias.get('historial_visitas', [])
            
            historial.append({
                "fecha": fecha,
                "atracciones_visitadas": atracciones_visitadas
            })
            
            preferencias['historial_visitas'] = historial
            visitante.preferencias = preferencias
            visitante.save()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    @staticmethod
    def visitantes_ordenados_por_tickets():
        """Listar visitantes ordenados por cantidad de tickets (descendente)"""
        try:
            from models.tickets_model import TicketModel
            return list(
                VisitanteModel
                .select(VisitanteModel, fn.COUNT(TicketModel.id).alias('total_tickets'))
                .join(TicketModel, JOIN.LEFT_OUTER)
                .group_by(VisitanteModel)
                .order_by(fn.COUNT(TicketModel.id).desc())
            )
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @staticmethod
    def visitantes_gastado_mas_de(cantidad):
        """Visitantes que han gastado más de X euros"""
        try:
            from models.tickets_model import TicketModel
            
            return list(
                VisitanteModel
                .select(
                    VisitanteModel,
                    fn.SUM(TicketModel.detalles_compra['precio'].cast('float')).alias('total_gastado')
                )
                .join(TicketModel, JOIN.LEFT_OUTER)
                .group_by(VisitanteModel)
                .having(fn.SUM(TicketModel.detalles_compra['precio'].cast('float')) > cantidad)
            )
        except Exception as e:
            print(f"Error: {e}")
            return []