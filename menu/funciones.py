from repositories.visitante_repositorie import VisitanteRepositorie
from repositories.atraccion_repositorie import AtraccionRepositorie
from repositories.ticket_repositorie import TicketRepositorie
import json
from datetime import datetime, date

def validar_email(email):
    """Validar formato de email"""
    verificacion = '@' in email and '.' in email
    return verificacion

def validar_entero(valor):
    """Validar que el input sea un entero"""
    while True:
        try:
            num = int(input("Ingrese un número válido:"))
            return num
        except ValueError:
            print("Error: Debe ingresar un número entero")

def validar_float(valor):
    """Validar que el input sea un float"""
    while True:
        try:
            num = float(input("Ingrese un número válido:"))
            return num
        except ValueError:
            print("Error: Debe ingresar un número válido")

def validar_fecha():
    """Validar formato de fecha"""
    while True:
        try:
            fecha = input("Ingrese fecha (YYYY-MM-DD:")
            return datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            print("Error: Formato de fecha inválido. Use YYYY-MM-DD")
