# =============================================================================
# REPOSITORIO DE VISITANTES
# =============================================================================
from models.visitante_model import VisitanteModel
from peewee import *
from playhouse.postgres_ext import *

class VisitanteRepositorie:
    """Encapsula toda la lógica de acceso a datos de visitantes"""
    
    # =========================================================================
    # OPERACIONES CRUD 
    # =========================================================================
    
    @staticmethod
    def crear_visitante(nombre, email, altura=None, preferencias=None):
        """Registra un nuevo visitante en el sistema"""
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
        """Recupera todos los visitantes registrados"""
        try:
            return list(VisitanteModel.select())
        except Exception as e:
            print(f"Error al obtener visitantes: {e}")
            return []
    
    @staticmethod
    def obtener_visitante_por_id(visitante_id):
        """Busca un visitante por su ID único"""
        try:
            return VisitanteModel.get_by_id(visitante_id)
        except Exception as e:
            print(f"Error al obtener visitante: {e}")
            return None
    
    @staticmethod
    def obtener_visitante_por_email(email):
        """Busca un visitante por su email"""
        try:
            return VisitanteModel.get(VisitanteModel.email == email)
        except Exception as e:
            print(f"Error al obtener visitante: {e}")
            return None
    
    @staticmethod
    def eliminar_visitante(visitante_id):
        """Elimina un visitante (sus tickets se eliminan por CASCADE)"""
        try:
            visitante = VisitanteModel.get_by_id(visitante_id)
            visitante.delete_instance()
            return True
        except Exception as e:
            print(f"Error al eliminar visitante: {e}")
            return False
    
    # =========================================================================
    # CONSULTAS CON JSONB
    # =========================================================================
    
    @staticmethod
    def visitantes_con_preferencia_extrema():
        """Filtra visitantes que prefieren atracciones extremas cast('text') convierte el JSONB a texto para comparar
        Las comillas en "extrema" son necesarias porque JSON usa comillas dobles"""
        try:
            return list(VisitanteModel.select().where(
                VisitanteModel.preferencias['tipo_favorito'].cast('text') == '"extrema"'
            ))
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @staticmethod
    def visitantes_con_problemas_cardiacos():
        """Busca visitantes con problemas cardíacos en su array de restricciones contains() busca dentro del array JSONB"""
        try:
            return list(VisitanteModel.select().where(
                VisitanteModel.preferencias['restricciones'].cast('text').contains('problemas_cardiacos')
            ))
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    # =========================================================================
    # MODIFICACIONES DE JSONB
    # =========================================================================
    
    @staticmethod
    def eliminar_restriccion(visitante_id, restriccion):
        """Elimina una restricción del array de restricciones del visitante
        1. Recupera el objeto completo
        2. Modifica el diccionario de preferencias
        3. Guarda de vuelta en la BD"""
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
        """Añade una nueva entrada al historial de visitas el historial es un array de objetos con fecha y atracciones"""
        try:
            visitante = VisitanteModel.get_by_id(visitante_id)
            preferencias = visitante.preferencias or {}
            historial = preferencias.get('historial_visitas', [])
            
            # Añade nueva visita al historial
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
    
    # =========================================================================
    # REPORTES Y CONSULTAS COMPLEJAS
    # =========================================================================
    
    @staticmethod
    def visitantes_ordenados_por_tickets():
        """Lista visitantes ordenados por cantidad de tickets comprados """
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
        """Visitantes que han gastado más de X euros en total"""
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