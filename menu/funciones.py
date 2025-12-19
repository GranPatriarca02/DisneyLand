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
    #CRUD de visitantes
def crear_visitante_menu():
    """Menú para crear un visitante y retorna el objeto creado"""
    print(" CREAR VISITANTE")
    nombre = input("Nombre: ")
    valido = False
    while not valido:
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
        print("\n¿Tienes alguna preferencia?")
        print("1. Sí")
        print("2. No")
        opcion = validar_entero()

        if opcion == 1:
            preferencias = {}

            print("\nTipo preferencia:")
            print("1. extrema")
            print("2. familiar")
            print("3. infantil")
            print("4. acuatica")

            tipo_valido = False
            while not tipo_valido:
                tipo_opcion = validar_entero()
                if tipo_opcion == 1:
                    preferencias['tipo_favorito'] = "extrema"
                    tipo_valido = True
                elif tipo_opcion == 2:
                    preferencias['tipo_favorito'] = "familiar"
                    tipo_valido = True
                elif tipo_opcion == 3:
                    preferencias['tipo_favorito'] = "infantil"
                    tipo_valido = True
                elif tipo_opcion == 4:
                    preferencias['tipo_favorito'] = "acuatica"
                    tipo_valido = True
                else:
                    print("Opción no válida")

            restricciones = input("Restricciones (separadas por comas): ").split(',')
            lista_restricciones_limpia = []

            for restriccion in restricciones:
                restriccion_limpia = restriccion.strip()
                if restriccion_limpia:
                    lista_restricciones_limpia.append(restriccion_limpia)

            preferencias['restricciones'] = lista_restricciones_limpia
            preferencias['historial_visitas'] = []

            visitante = VisitanteRepositorie.crear_visitante(nombre, email, altura, preferencias)
            valido = True

        elif opcion == 2:
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
    
    print("Tipos disponibles:")
    print("1. extrema")
    print("2. familiar")
    print("3. infantil")
    print("4. acuatica")

    tipo = ""
    valido = False
    while not valido:
        opcion_tipo = validar_entero()
        if opcion_tipo == 1:
            tipo = "extrema"
            valido = True
        elif opcion_tipo == 2:
            tipo = "familiar"
            valido = True
        elif opcion_tipo == 3:
            tipo = "infantil"
            valido = True
        elif opcion_tipo == 4:
            tipo = "acuatica"
            valido = True
        else:
            print("Opción no válida")
    
    print("Altura minima (cm):")
    altura_minima = validar_entero()
    
    detalles = None
    atraccion = None
    valido = False
    
    while not valido:
        print("\n¿Quieres agregar detalles?")
        print("1. Sí")
        print("2. No")
        opcion = validar_entero()

        if opcion == 1:
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
            
        elif opcion == 2:
            atraccion = AtraccionRepositorie.crear_atraccion(nombre, tipo, altura_minima)
            valido = True
        else:
            print("Error: Opcion no valida")
    
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
    #CRUD de Tickets

def crear_ticket_menu():
    """Menú para crear un ticket y retorna el objeto creado"""
    print("CREAR TICKET")
    
    print("ID del visitante:")
    visitante_id = validar_entero()
    
    # Validación de ticket general/específico
    general = False
    atraccion_id = None
    valido_tipo = False
    while not valido_tipo:
        print("\n¿Es un ticket general?")
        print("1. Sí (Ticket general)")
        print("2. No (Ticket específico)")
        opcion = validar_entero()

        if opcion == 1:
            general = True
            valido_tipo = True
        elif opcion == 2:
            print("ID de la atraccion:")
            atraccion_id = validar_entero()
            valido_tipo = True
        else:
            print("Error: Opcion no valida")
    
    # Validación de fecha
    fecha_visita = validar_fecha()
    
    print("\nTipos de ticket:")
    print("1. general")
    print("2. colegio")
    print("3. empleado")

    valido = False
    tipo_ticket = ""
    while not valido:
        opcion = validar_entero()
        if opcion == 1:
            tipo_ticket = "general"
            valido = True
        elif opcion == 2:
            tipo_ticket = "colegio"
            valido = True
        elif opcion == 3:
            tipo_ticket = "empleado"
            valido = True
        else:
            print("Opción no válida")
    
    detalles_compra = {}
    print("Precio:")
    detalles_compra['precio'] = validar_float()
    
    # Bucle para Descuentos
    entrada_descuentos = input("Descuentos aplicados (separados por comas): ").split(',')
    lista_descuentos = []
    for descuento in entrada_descuentos:
        descuento_limpio = descuento.strip()
        if descuento_limpio:
            lista_descuentos.append(descuento_limpio)
    detalles_compra['descuentos_aplicados'] = lista_descuentos
    
    # Bucle para Servicios
    entrada_servicios = input("Servicios extra (separados por comas): ").split(',')
    lista_servicios = []
    for servicio in entrada_servicios:
        servicio_limpio = servicio.strip()
        if servicio_limpio:
            lista_servicios.append(servicio_limpio)
    detalles_compra['servicios_extra'] = lista_servicios
    
    detalles_compra['metodo_pago'] = input("Metodo de pago: ")
    
    ticket = TicketRepositorie.crear_ticket(
        visitante_id, fecha_visita, tipo_ticket, detalles_compra, atraccion_id
    )
    
    if ticket:
        print(f"Ticket creado con ID: {ticket.id}")
    else:
        print("Error: No se pudo crear el ticket")
        
    return ticket

def listar_tickets():
    """Listar todos los tickets y retorna la lista"""
    print("LISTA DE TICKETS")
    tickets = TicketRepositorie.obtener_todos_tickets()
    
    if not tickets:
        print("No hay tickets registrados")
        return []
    
    for t in tickets:
        print(f"\nID: {t.id}")
        id_visitante = t.visitante.id
        nombre_visitante = t.visitante.nombre
        print(f"Visitante: ID {id_visitante} - {nombre_visitante}")
        
        # Para la atracción, como puede ser None (si es ticket general)
        # usamos una estructura simple de if/else
        if t.atraccion is None:
            nombre_atraccion = "General"
        else:
            nombre_atraccion = t.atraccion.nombre
            
        print(f"Atraccion: {nombre_atraccion}")
        print(f"Tipo: {t.tipo_ticket}")
        print(f"Fecha visita: {t.fecha_visita}")
        if t.usado:
            print("Ticket usado: Si")
        else:
            print("Ticket usado: No")
        if t.detalles_compra:
            print(f"Detalles: {json.dumps(t.detalles_compra, indent=2)}")
            
    return tickets
def marcar_ticket_usado_menu():
    """Marcar un ticket como usado y retorna el resultado"""
    print("MARCAR TICKET USADO")
    print("ID del ticket:")
    ticket_id = validar_entero()
    
    exito = TicketRepositorie.marcar_ticket_usado(ticket_id)
    
    if exito:
        print("Confirmacion: Ticket marcado como usado")
    else:
        print("Error: No se pudo marcar el ticket")
        
    return exito

    #Metodos listar

def listar_tickets_visitante():
    """Listar tickets de un visitante específico"""
    print("elige el id del visitante")
    visitante_id = validar_entero()
    tickets = TicketRepositorie.obtener_tickets_visitante(visitante_id)
    print(f"\nTickets del visitante (Total: {len(tickets)}):")
    for t in tickets:
        if t.atraccion is None:
            atraccion = "General"
        else:
            atraccion = t.atraccion.nombre
        
        print(f"- Ticket {t.id}: {atraccion} - {t.fecha_visita}")

def listar_tickets_atraccion():
    """Listar tickets de una atracción específica"""
    print("elige el id de la atraccion")
    atraccion_id = validar_entero()
    tickets = TicketRepositorie.obtener_tickets_atraccion(atraccion_id)
    print(f"\nTickets de la atracción (Total: {len(tickets)}):")
    for t in tickets:
        if t.visitante is None:
            visitante = "Desconocido"
        else:
            visitante = t.visitante.nombre
        
        print(f"- Ticket {t.id}: Visitante {visitante} - {t.fecha_visita}")

def listar_visitantes_atraccion():
    """Listar visitantes con ticket para una atracción"""
    print("elige el id de la atraccion")
    atraccion_id = validar_entero()
    visitantes = TicketRepositorie.obtener_visitantes_con_ticket_atraccion(atraccion_id)
    print(f"\nVisitantes con ticket (Total: {len(visitantes)}):")
    for v in visitantes:
        if v is None:
            nombre = "Desconocido"
            email = "Sin email"
        else:
            nombre = v.nombre
            email = v.email
            print(f"- {nombre} ({email})")

        # CONSULTAS 

def consultas_menu():
    """Menú de consultas"""
    salir = False
    while not salir:
        print("\n=== MENÚ DE CONSULTAS ===")
        print("1. Visitantes con preferencia extrema")
        print("2. Atracciones con intensidad > 7")
        print("3. Tickets colegio < 30€")
        print("4. Atracciones duración > 120 seg")
        print("5. Visitantes con problemas cardíacos")
        print("6. Atracciones con looping y caída libre")
        print("7. Tickets con descuento estudiante")
        print("8. Atracciones con mantenimiento")
        print("9. Visitantes por cantidad de tickets")
        print("10. Top 5 atracciones más vendidas")
        print("11. Visitantes que gastaron > 100€")
        print("12. Atracciones compatibles visitante")
        print("0. Volver")
        print("Seleccione una opción: ")
        opcion = validar_entero()
        
        if opcion == 0:
            salir = True
        elif opcion == 1:
            visitantes = VisitanteRepositorie.visitantes_con_preferencia_extrema()
            print(f"\nEncontrados {len(visitantes)} visitantes")
            for v in visitantes:
                print(f"- {v.nombre} ({v.email})")
        
        elif opcion == 2:
            atracciones = AtraccionRepositorie.atracciones_intensidad_mayor(7)
            print(f"\nEncontradas {len(atracciones)} atracciones")
            for a in atracciones:
                intensidad = a.detalles.get('intensidad', 'N/A')
                print(f"- {a.nombre} (Intensidad: {intensidad})")
        
        elif opcion == 3:
            tickets = TicketRepositorie.tickets_tipo_colegio_precio_menor(30)
            print(f"\nEncontrados {len(tickets)} tickets")
            for t in tickets:
                precio = t.detalles_compra.get('precio', 'N/A')
                print(f"- Ticket {t.id} - Precio: {precio}€")
        
        elif opcion == 4:
            atracciones = AtraccionRepositorie.atracciones_duracion_mayor(120)
            print(f"\nEncontradas {len(atracciones)} atracciones")
            for a in atracciones:
                duracion = a.detalles.get('duracion_segundos', 'N/A')
                print(f"- {a.nombre} (Duración: {duracion}s)")
        
        elif opcion == 5:
            visitantes = VisitanteRepositorie.visitantes_con_problemas_cardiacos()
            print(f"\nEncontrados {len(visitantes)} visitantes")
            for v in visitantes:
                print(f"- {v.nombre} ({v.email})")
        
        elif opcion == 6:
            atracciones = AtraccionRepositorie.atracciones_con_caracteristicas(['looping', 'caida_libre'])
            print(f"\nEncontradas {len(atracciones)} atracciones")
            for a in atracciones:
                print(f"- {a.nombre}")
        
        elif opcion == 7:
            tickets = TicketRepositorie.tickets_con_descuento('estudiante')
            print(f"\nEncontrados {len(tickets)} tickets")
            for t in tickets:
                print(f"- Ticket {t.id} - Visitante: {t.visitante.nombre}")
        
        elif opcion == 8:
            atracciones = AtraccionRepositorie.atracciones_con_mantenimiento()
            print(f"\nEncontradas {len(atracciones)} atracciones")
            for a in atracciones:
                print(f"- {a.nombre}")
        
        elif opcion == 9:
            visitantes = VisitanteRepositorie.visitantes_ordenados_por_tickets()
            print("\nVisitantes ordenados por tickets:")
            for v in visitantes:
                total = getattr(v, 'total_tickets', 0)
                print(f"- {v.nombre}: {total} tickets")
        
        elif opcion == 10:
            atracciones = AtraccionRepositorie.atracciones_mas_vendidas(5)
            print("\nTop 5 atracciones más vendidas:")
            for a in atracciones:
                total = getattr(a, 'total_tickets', 0)
                print(f"- {a.nombre}: {total} tickets")
        
        elif opcion == 11:
            visitantes = VisitanteRepositorie.visitantes_gastado_mas_de(100)
            print("\nVisitantes que gastaron más de 100€:")
            for v in visitantes:
                total = getattr(v, 'total_gastado', 0)
                print(f"- {v.nombre}: {total}€")
        
        elif opcion == 12:
            print("ID del visitante: ")
            visitante_id = validar_entero()
            atracciones = AtraccionRepositorie.atracciones_compatibles_visitante(visitante_id)
            print(f"\nAtracciones compatibles:")
            for a in atracciones:
                print(f"- {a.nombre} ({a.tipo})")
        else:
            print("Opcion no valida")
        
        
