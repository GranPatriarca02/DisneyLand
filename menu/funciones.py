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

    #CRUD de atracciones

def crear_atraccion_menu():
    """Menú para crear una atracción y retorna el objeto creado"""
    print("CREAR ATRACCION")
    nombre = input("Nombre: ")
    
    print("Tipos disponibles: extrema, familiar, infantil, acuatica")
    tipo = input("Tipo: ")
    
    print("Altura minima (cm):")
    altura_minima = validar_entero()
    
    detalles = None
    atraccion = None
    valido = False
    
    while not valido:
        respuesta = input("quieres agregar detalles? (s/n): ").lower()
        if respuesta == 's':
            detalles = {}
            print("Duracion (segundos):")
            detalles['duracion_segundos'] = validar_entero()
            
            print("Capacidad por turno:")
            detalles['capacidad_por_turno'] = validar_entero()
            
            print("Intensidad (1-10):")
            detalles['intensidad'] = validar_entero()
            
        
            entrada_caracteristicas = input("Caracteristicas (separadas por comas): ").split(',')
            lista_caracteristicas_limpia = []
            for caracteristica in entrada_caracteristicas:
                caracteristica_limpia = caracteristica.strip()
                if caracteristica_limpia:
                    lista_caracteristicas_limpia.append(caracteristica_limpia)
            
            detalles['caracteristicas'] = lista_caracteristicas_limpia
            
            detalles['horarios'] = {
                'apertura': input("Hora apertura (HH:MM): "),
                'cierre': input("Hora cierre (HH:MM): "),
                'mantenimiento': []
            }
            
            atraccion = AtraccionRepositorie.crear_atraccion(nombre, tipo, altura_minima, detalles)
            valido = True
            
        elif respuesta == 'n':
            atraccion = AtraccionRepositorie.crear_atraccion(nombre, tipo, altura_minima)
            valido = True
        else:
            print("Error: Opcion no valida. Ingrese 's' o 'n'.")
    
    if atraccion:
        print(f"Confirmacion: Atraccion creada con ID: {atraccion.id}")
    else:
        print("Error: No se pudo crear la atraccion")
        
    return atraccion

def listar_atracciones():
    """Listar todas las atracciones y retorna la lista"""
    print("LISTA DE ATRACCIONES")
    atracciones = AtraccionRepositorie.obtener_todas_atracciones()
    
    if not atracciones:
        print("No hay atracciones registradas")
        return []
    
    for a in atracciones:
        print(f"\nID: {a.id}")
        print(f"Nombre: {a.nombre}")
        print(f"Tipo: {a.tipo}")
        print(f"Altura minima: {a.altura_minima} cm")
        print(f"Activa: {'Si' if a.activa else 'No'}")
        if a.detalles:
            print(f"Detalles: {json.dumps(a.detalles, indent=2)}")
            
    return atracciones

def cambiar_estado_atraccion_menu():
    """Cambiar estado de una atracción y retorna el nuevo estado"""
    print("CAMBIAR ESTADO ATRACCION")
    print("ID de la atraccion:")
    atraccion_id = validar_entero()
    
    print("Estado: 1=Activa, 0=Inactiva")
    valido=False
    while not valido:
        
        estado = validar_entero()
        if estado in (0,1):

            nuevo_estado = bool(estado)
            valido=True
        else:
            print("valor incorrecto")

        
    exito = AtraccionRepositorie.cambiar_estado_atraccion(atraccion_id, nuevo_estado)
        
    if exito:
        print("Estado cambiado exitosamente")
    else:
        print("No se pudo cambiar el estado")
        
    return exito

def eliminar_atraccion_menu():
    """Eliminar una atracción y retorna True si fue exitoso"""
    print("ELIMINAR ATRACCION")
    print("ID de la atraccion:")
    atraccion_id = validar_entero()
    
    exito = AtraccionRepositorie.eliminar_atraccion(atraccion_id)
    
    if exito:
        print("Confirmacion: Atraccion eliminada exitosamente")
    else:
        print("Error: No se pudo eliminar la atraccion")
        
    return exito