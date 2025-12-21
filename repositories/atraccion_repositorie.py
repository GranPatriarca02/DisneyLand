# =============================================================================
# REPOSITORIO DE ATRACCIONES
# =============================================================================
from models.atraccion_model import AtraccionModel
from peewee import *
from playhouse.postgres_ext import *

class AtraccionRepositorie:
    """Gestiona todas las operaciones relacionadas con atracciones"""
    
    # =========================================================================
    # OPERACIONES CRUD 
    # =========================================================================
    
    @staticmethod
    def crear_atraccion(nombre, tipo, altura_minima, detalles=None):
        """Registra una nueva atracción en el parque"""
        try:
            return AtraccionModel.create(
                nombre=nombre,
                tipo=tipo,
                altura_minima=altura_minima,
                detalles=detalles or {}
            )
        except Exception as e:
            print(f"Error al crear atracción: {e}")
            return None

    @staticmethod
    def obtener_todas_atracciones():
        """Devuelve todas las atracciones (activas e inactivas)"""
        try:
            return list(AtraccionModel.select())
        except Exception as e:
            print(f"Error: {e}")
            return []

    @staticmethod
    def obtener_atracciones_activas():
        """Filtra solo las atracciones que están actualmente operativas"""
        try:
            return list(AtraccionModel.select().where(AtraccionModel.activa == True))
        except Exception as e:
            print(f"Error: {e}")
            return []

    @staticmethod
    def obtener_atraccion_por_id(atraccion_id):
        """Busca una atracción específica por su ID"""
        try:
            return AtraccionModel.get_by_id(atraccion_id)
        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def cambiar_estado_atraccion(atraccion_id, activa):
        """Activa o desactiva una atracción (mantenimiento, reparaciones, etc.)"""
        try:
            atraccion = AtraccionModel.get_by_id(atraccion_id)
            atraccion.activa = activa
            atraccion.save()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def eliminar_atraccion(atraccion_id):
        """Elimina permanentemente una atracción del sistema"""
        try:
            atraccion = AtraccionModel.get_by_id(atraccion_id)
            atraccion.delete_instance()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    # =========================================================================
    # CONSULTAS CON JSONB
    # =========================================================================

    @staticmethod
    def atracciones_intensidad_mayor(intensidad):
        """Filtra atracciones cuya intensidad supera el valor indicado el campo 'intensidad' está dentro del JSONB 'detalles'"""
        try:
            return list(AtraccionModel.select().where(
                AtraccionModel.detalles['intensidad'].cast('int') > intensidad
            ))
        except Exception as e:
            print(f"Error: {e}")
            return []

    @staticmethod
    def atracciones_duracion_mayor(segundos):
        """Busca atracciones que duran más de X segundos"""
        try:
            return list(AtraccionModel.select().where(
                AtraccionModel.detalles['duracion_segundos'].cast('int') > segundos
            ))
        except Exception as e:
            print(f"Error: {e}")
            return []

    @staticmethod
    def atracciones_con_caracteristicas(caracteristicas):
        """Busca atracciones que contengan todas las características solicitadas"""
        try:
            query = AtraccionModel.select()
            # Aplica un filtro por cada característica 
            for caracteristica in caracteristicas:
                query = query.where(
                    AtraccionModel.detalles['caracteristicas'].cast('text').contains(caracteristica)
                )
            return list(query)
        except Exception as e:
            print(f"Error: {e}")
            return []

    @staticmethod
    def atracciones_con_mantenimiento():
        """Encuentra atracciones que tienen mantenimiento programado"""
        try:
            return list(AtraccionModel.select().where(
                # Condición 1: la clave no es NULL
                (AtraccionModel.detalles['horarios']['mantenimiento'].is_null(False)) &
                # Condición 2: no es un array vacío []
                (AtraccionModel.detalles['horarios']['mantenimiento'] != json.dumps([]))
            ))
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    # =========================================================================
    # MODIFICACIONES DE JSONB
    # =========================================================================
    
    @staticmethod
    def agregar_caracteristica(atraccion_id, caracteristica):
        """Añade una nueva característica al array de características"""
        try:
            atraccion = AtraccionModel.get_by_id(atraccion_id)
            detalles = atraccion.detalles or {}
            caracs = detalles.get('caracteristicas', [])
            
            if caracteristica not in caracs:
                caracs.append(caracteristica)
                detalles['caracteristicas'] = caracs
                atraccion.detalles = detalles
                atraccion.save()
                return True
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False

    # =========================================================================
    # REPORTES Y LÓGICA DE NEGOCIO
    # =========================================================================

    @staticmethod
    def atracciones_mas_vendidas(limite=5):
        """Genera un ranking de las atracciones con más tickets vendidos"""
        try:
            from models.tickets_model import TicketModel
            return list(
                AtraccionModel
                .select(AtraccionModel, fn.COUNT(TicketModel.id).alias('total_tickets'))
                .join(TicketModel, JOIN.LEFT_OUTER)
                .where(TicketModel.atraccion.is_null(False))
                .group_by(AtraccionModel)
                .order_by(fn.COUNT(TicketModel.id).desc())
                .limit(limite)
            )
        except Exception as e:
            print(f"Error: {e}")
            return []

    @staticmethod
    def atracciones_compatibles_visitante(visitante_id):
        """Encuentra atracciones adecuadas para un visitante específico"""
        try:
            from models.visitante_model import VisitanteModel
            visitante = VisitanteModel.get_by_id(visitante_id)
            fav = visitante.preferencias.get('tipo_favorito', '')
            
            query = AtraccionModel.select().where(
                (AtraccionModel.activa == True) &
                (AtraccionModel.altura_minima <= visitante.altura)
            )
            
            # Filtro adicional si tiene preferencia de tipo
            if fav:
                query = query.where(AtraccionModel.tipo == fav)
            return list(query)
        except Exception as e:
            print(f"Error: {e}")
            return []