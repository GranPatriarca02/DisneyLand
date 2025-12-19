from models.atraccion_model import AtraccionModel
from peewee import *
from playhouse.postgres_ext import *

class AtraccionRepositorie:
    
    # MÉTODOS DE CREACIÓN Y BÚSQUEDA 

    @staticmethod
    def crear_atraccion(nombre, tipo, altura_minima, detalles=None):
        """ Registra una nueva atracción en la base de datos """
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
        """ Retorna el listado completo de atracciones """
        try:
            return list(AtraccionModel.select())
        except Exception as e:
            print(f"Error: {e}"); 
            return []

    @staticmethod
    def obtener_atracciones_activas():
        """ Retorna solo las atracciones con estado activo """
        try:
            return list(AtraccionModel.select().where(AtraccionModel.activa == True))
        except Exception as e:
            print(f"Error: {e}"); 
            return []

    @staticmethod
    def obtener_atraccion_por_id(atraccion_id):
        """ Busca una atracción específica por su clave primaria """
        try:
            return AtraccionModel.get_by_id(atraccion_id)
        except Exception as e:
            print(f"Error: {e}"); 
            return None

    #  MÉTODOS DE ACTUALIZACIÓN Y ELIMINACIÓN

    @staticmethod
    def cambiar_estado_atraccion(atraccion_id, activa):
        """ Alterna la disponibilidad de la atracción """
        try:
            atraccion = AtraccionModel.get_by_id(atraccion_id)
            atraccion.activa = activa
            atraccion.save()
            return True
        except Exception as e:
            print(f"Error: {e}"); 
            return False

    @staticmethod
    def eliminar_atraccion(atraccion_id):
        """ Remueve físicamente el registro de la atracción """
        try:
            atraccion = AtraccionModel.get_by_id(atraccion_id)
            atraccion.delete_instance()
            return True
        except Exception as e:
            print(f"Error: {e}"); 
            return False

    #  CONSULTAS ESPECIALIZADAS

    @staticmethod
    def atracciones_intensidad_mayor(intensidad):
        """ Filtra atracciones por el campo 'intensidad' dentro del JSONB """
        try:
            return list(AtraccionModel.select().where(
                AtraccionModel.detalles['intensidad'].cast('int') > intensidad
            ))
        except Exception as e:
            print(f"Error: {e}"); 
            return []

    @staticmethod
    def atracciones_duracion_mayor(segundos):
        """ Filtra atracciones por duración mínima definida en detalles """
        try:
            return list(AtraccionModel.select().where(
                AtraccionModel.detalles['duracion_segundos'].cast('int') > segundos
            ))
        except Exception as e:
            print(f"Error: {e}"); 
            return []

    @staticmethod
    def atracciones_con_caracteristicas(caracteristicas):
        """ Busca atracciones que contengan todas las características solicitadas """
        try:
            query = AtraccionModel.select()
            for caracteristica in caracteristicas:
                query = query.where(
                    AtraccionModel.detalles['caracteristicas'].cast('text').contains(caracteristica)
                )
            return list(query)
        except Exception as e:
            print(f"Error: {e}"); 
            return []

    @staticmethod
    def atracciones_con_mantenimiento():
        """ Lista atracciones que poseen claves de mantenimiento en su horario """
        try:
            return list(AtraccionModel.select().where(
                AtraccionModel.detalles['horarios']['mantenimiento'].exists()
            ))
        except Exception as e:
            print(f"Error: {e}"); 
            return []

    @staticmethod
    def agregar_caracteristica(atraccion_id, caracteristica):
        """ Inyecta una nueva etiqueta en el array de características del JSONB """
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
            print(f"Error: {e}"); 
            return False

    #  REPORTES Y LÓGICA DE NEGOCIO 

    @staticmethod
    def atracciones_mas_vendidas(limite=5):
        """ Calcula el ranking de atracciones basado en tickets emitidos """
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
            print(f"Error: {e}"); 
            return []

    @staticmethod
    def atracciones_compatibles_visitante(visitante_id):
        """ Filtra atracciones según altura y gustos del visitante """
        try:
            from models.visitante_model import VisitanteModel
            visitante = VisitanteModel.get_by_id(visitante_id)
            fav = visitante.preferencias.get('tipo_favorito', '')
            
            query = AtraccionModel.select().where(
                (AtraccionModel.activa == True) &
                (AtraccionModel.altura_minima <= visitante.altura)
            )
            
            if fav: query = query.where(AtraccionModel.tipo == fav)
            return list(query)
        except Exception as e:
            print(f"Error: {e}"); 
            return []