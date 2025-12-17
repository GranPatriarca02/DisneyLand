from models.tickets_model import TicketModel
from models.visitante_model import VisitanteModel
from models.atraccion_model import AtraccionModel
from peewee import *
from playhouse.postgres_ext import *
from datetime import datetime

class TicketRepositorie:
      # MÉTODOS DE CREACIÓN Y BÚSQUEDA 
    @staticmethod
    def crear_ticket(visitante_id, fecha_visita, tipo_ticket, detalles_compra, atraccion_id=None):
        """Crear un nuevo ticket"""
        try:
            ticket = TicketModel.create(
                visitante=visitante_id,
                atraccion=atraccion_id,
                fecha_visita=fecha_visita,
                tipo_ticket=tipo_ticket,
                detalles_compra=detalles_compra or {}
            )
            return ticket
        except Exception as e:
            print(f"Error al crear ticket: {e}")
            return None
    
    @staticmethod
    def obtener_todos_tickets():
        """Obtener todos los tickets"""
        try:
            return list(TicketModel.select())
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @staticmethod
    def obtener_tickets_visitante(visitante_id):
        """Obtener tickets de un visitante específico"""
        try:
            return list(TicketModel.select().where(
                TicketModel.visitante == visitante_id
            ))
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @staticmethod
    def obtener_tickets_atraccion(atraccion_id):
        """Obtener tickets vendidos para una atracción específica"""
        try:
            return list(TicketModel.select().where(
                TicketModel.atraccion == atraccion_id
            ))
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @staticmethod
    def obtener_visitantes_con_ticket_atraccion(atraccion_id):
        """Obtener visitantes que tienen ticket para una atracción (directa o general)"""
        try:
            return list(
                VisitanteModel
                .select()
                .join(TicketModel)
                .where(
                    (TicketModel.atraccion == atraccion_id) | 
                    (TicketModel.atraccion.is_null(True))
                )
                .distinct()
            )
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @staticmethod
    def marcar_ticket_usado(ticket_id):
        """Marcar un ticket como usado"""
        try:
            ticket = TicketModel.get_by_id(ticket_id)
            ticket.usado = True
            ticket.fecha_uso = datetime.now()
            ticket.save()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    @staticmethod
    def tickets_tipo_colegio_precio_menor(precio):
        """Tickets tipo colegio con precio menor a X"""
        try:
            return list(TicketModel.select().where(
                (TicketModel.tipo_ticket == 'colegio') &
                (TicketModel.detalles_compra['precio'].cast('float') < precio)
            ))
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @staticmethod
    def tickets_con_descuento(descuento):
        """Tickets que tengan un descuento específico"""
        try:
            return list(TicketModel.select().where(
                TicketModel.detalles_compra['descuentos_aplicados'].cast('text').contains(descuento)
            ))
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @staticmethod
    def cambiar_precio_ticket(ticket_id, nuevo_precio):
        """Cambiar el precio de un ticket"""
        try:
            ticket = TicketModel.get_by_id(ticket_id)
            detalles = ticket.detalles_compra or {}
            detalles['precio'] = nuevo_precio
            ticket.detalles_compra = detalles
            ticket.save()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False