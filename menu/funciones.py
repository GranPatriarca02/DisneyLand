from repositories.visitante_repositorie import VisitanteRepositorie
from repositories.atraccion_repositorie import AtraccionRepositorie
from repositories.ticket_repositorie import TicketRepositorie
import json
from datetime import datetime, date

def validar_email(email):
    """Validar formato de email"""
    verificacion = '@' in email and '.' in email
    return verificacion

def validar_entero():
    """Validar que el input sea un entero"""
    while True:
        try:
            num = int(input("Ingrese un número válido:"))
            return num
        except ValueError:
            print("Error: Debe ingresar un número entero")

def validar_float():
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

def crear_visitante_menu():
    """Menú para crear un visitante y retorna el objeto creado"""
    print(" CREAR VISITANTE")
    nombre = input("Nombre: ")
    valido = False
    while not valido :
        email = input("Email: ")
        if validar_email(email):
            valido = True
        else:
            print("Error: Email inválido")
    
    print("Altura en centímetros:")
    altura = validar_entero()
    
    preferencias = None
    valido = False
    while not valido:
        respuesta = input("¿Tienes alguna preferencia?(s/n)")
        if respuesta.lower() == 's':
            preferencias = {}
            preferencias['tipo_favorito'] = input("Tipo favorito (extrema/familiar/infantil/acuatica): ")

            restricciones = input("Restricciones (separadas por comas): ").split(',')
            lista_restricciones_limpia = []

            for restriccion in restricciones:
                restriccion_limpia = restriccion.strip() # Quitamos espacios en blanco
                if restriccion_limpia:         # Verificamos que no sea una cadena vacía
                    lista_restricciones_limpia.append(restriccion_limpia)

            preferencias['restricciones'] = lista_restricciones_limpia

            preferencias['historial_visitas'] = []
            visitante = VisitanteRepositorie.crear_visitante(nombre, email, altura, preferencias)
            valido = True
        elif respuesta.lower() == 'n':
            print("Sin preferencias")
            visitante = VisitanteRepositorie.crear_visitante(nombre, email, altura)
            valido = True
        else:
            print("Opcion no valida")
    if visitante:
        print(f"Confirmacion: Visitante creado con ID: {visitante.id}")
    else:
        print("Error: No se pudo crear el visitante")
        
    return visitante

def listar_visitantes():
    """Listar todos los visitantes y retorna la lista"""
    print("LISTA DE VISITANTES")
    visitantes = VisitanteRepositorie.obtener_todos_visitantes()
    
    if not visitantes:
        print("No hay visitantes registrados")
        return []
    
    for v in visitantes:
        print(f"\nID: {v.id}")
        print(f"Nombre: {v.nombre}")
        print(f"Email: {v.email}")
        print(f"Altura: {v.altura} cm")
        print(f"Fecha registro: {v.fecha_registro}")
        if v.preferencias:
            print(f"Preferencias: {json.dumps(v.preferencias, indent=2)}")
            
    return visitantes

def eliminar_visitante_menu():
    """Menú para eliminar un visitante y retorna True si fue exitoso"""
    print("ELIMINAR VISITANTE")
    print("ID del visitante:")
    visitante_id = validar_entero()
    
    exito = VisitanteRepositorie.eliminar_visitante(visitante_id)
    
    if exito:
        print("Confirmacion: Visitante eliminado exitosamente")
    else:
        print("Error: No se pudo eliminar al visitante")
        
    return exito