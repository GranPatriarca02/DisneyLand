"""
ingesta.py - Script para cargar datos de prueba en el sistema
Genera automáticamente:
- 100 visitantes con preferencias variadas
- 20 atracciones de diferentes tipos
- 150 tickets con diferentes características
"""

from database import conectar_db, cerrar_db
from repositories.visitante_repositorie import VisitanteRepositorie
from repositories.atraccion_repositorie import AtraccionRepositorie
from repositories.ticket_repositorie import TicketRepositorie
from datetime import datetime, timedelta
import random

class Ingesta:
    """Clase para generar datos de prueba en el sistema"""
    
    def __init__(self):
        """Inicializa listas para almacenar los IDs creados"""
        self.visitantes_ids = []
        self.atracciones_ids = []
        self.tickets_ids = []
    
    def generar_visitantes(self, cantidad=100):
        """Genera visitantes con datos variados"""
        print(f"\n{'='*60}")
        print(f"GENERANDO {cantidad} VISITANTES")
        print(f"{'='*60}")
        
        # Nombres de ejemplo
        nombres = [
            "Ana García", "Carlos Martínez", "Laura López", "Miguel Torres",
            "Sofía Rodríguez", "David Hernández", "Elena Pérez", "Pablo Sánchez",
            "María González", "Javier Ramírez", "Carmen Flores", "Antonio Ruiz",
            "Isabel Moreno", "Francisco Jiménez", "Lucía Álvarez", "Sergio Romero",
            "Patricia Navarro", "Roberto Molina", "Marta Castro", "Diego Ortiz",
            "Julia Rubio", "Manuel Delgado", "Rosa Marín", "Alberto Suárez",
            "Beatriz Vega", "Fernando Gil", "Cristina Cortés", "Raúl Méndez",
            "Natalia Guerrero", "Andrés Prieto", "Teresa Iglesias", "Luis Garrido",
            "Sandra Santos", "José Lozano", "Mónica Núñez", "Daniel Muñoz",
            "Silvia Ramos", "Ángel Vargas", "Alicia Herrera", "Víctor Medina",
            "Pilar Aguilar", "Marcos Reyes", "Nuria Cabrera", "Rubén León",
            "Eva Santana", "Adrián Pascual", "Clara Domínguez", "Jorge Vázquez",
            "Irene Giménez", "Óscar Fernández", "Lorena Díaz", "Héctor Benítez"
        ]
        
        # Dominios de email
        dominios = ["gmail.com", "hotmail.com", "yahoo.es", "outlook.com", "icloud.com"]
        
        # Tipos de preferencia
        tipos_favoritos = ["extrema", "familiar", "infantil", "acuatica"]
        
        # Restricciones posibles
        restricciones_disponibles = [
            "problemas_cardiacos", "embarazo", "problemas_espalda",
            "miedo_alturas", "mareos", "claustrofobia"
        ]
        
        contador_exitosos = 0
        
        for i in range(cantidad):
            try:
                # Selecciona un nombre aleatorio (con posibilidad de repetir)
                nombre = random.choice(nombres)
                if i >= len(nombres):
                    nombre = f"{nombre} {i}"  # Añade número para hacerlo único
                
                # Genera email único
                email = f"{nombre.lower().replace(' ', '.')}.{i}@{random.choice(dominios)}"
                
                # Altura aleatoria entre 100 y 200 cm
                altura = random.randint(100, 200)
                
                # 70% de probabilidad de tener preferencias
                preferencias = None
                if random.random() < 0.7:
                    preferencias = {}
                    
                    # Tipo favorito
                    preferencias['tipo_favorito'] = random.choice(tipos_favoritos)
                    
                    # Restricciones (0-3 restricciones aleatorias)
                    num_restricciones = random.randint(0, 3)
                    preferencias['restricciones'] = random.sample(
                        restricciones_disponibles, 
                        num_restricciones
                    )
                    
                    # Historial vacío (se llenará con visitas futuras)
                    preferencias['historial_visitas'] = []
                
                # Crear visitante
                visitante = VisitanteRepositorie.crear_visitante(
                    nombre=nombre,
                    email=email,
                    altura=altura,
                    preferencias=preferencias
                )
                
                if visitante:
                    self.visitantes_ids.append(visitante.id)
                    contador_exitosos += 1
                    if (contador_exitosos) % 10 == 0:
                        print(f"✓ Creados {contador_exitosos} visitantes...")
                
            except Exception as e:
                print(f"✗ Error al crear visitante {i+1}: {e}")
        
        print(f"\n✅ Total visitantes creados: {contador_exitosos}/{cantidad}")
        return contador_exitosos
    
    def generar_atracciones(self, cantidad=20):
        """Genera atracciones variadas"""
        print(f"\n{'='*60}")
        print(f"GENERANDO {cantidad} ATRACCIONES")
        print(f"{'='*60}")
        
        # Definición de atracciones con sus características
        atracciones_data = [
            # EXTREMAS
            {
                "nombre": "Montaña Rusa Infernal",
                "tipo": "extrema",
                "altura_minima": 140,
                "detalles": {
                    "duracion_segundos": 180,
                    "capacidad_por_turno": 24,
                    "intensidad": 10,
                    "caracteristicas": ["looping", "caida_libre", "inversion", "alta_velocidad"],
                    "horarios": {
                        "apertura": "10:00",
                        "cierre": "22:00",
                        "mantenimiento": []
                    }
                }
            },
            {
                "nombre": "Caída Libre Extrema",
                "tipo": "extrema",
                "altura_minima": 135,
                "detalles": {
                    "duracion_segundos": 45,
                    "capacidad_por_turno": 16,
                    "intensidad": 9,
                    "caracteristicas": ["caida_libre", "alta_velocidad"],
                    "horarios": {
                        "apertura": "10:30",
                        "cierre": "21:30",
                        "mantenimiento": []
                    }
                }
            },
            {
                "nombre": "Tornado Giratorio",
                "tipo": "extrema",
                "altura_minima": 140,
                "detalles": {
                    "duracion_segundos": 120,
                    "capacidad_por_turno": 20,
                    "intensidad": 8,
                    "caracteristicas": ["giros", "inversion", "alta_velocidad"],
                    "horarios": {
                        "apertura": "11:00",
                        "cierre": "22:00",
                        "mantenimiento": [
                            {
                                "fecha_inicio": "2025-12-23",
                                "fecha_fin": "2025-12-25",
                                "motivo": "Revisión anual de seguridad"
                            }
                        ]
                    }
                }
            },
            {
                "nombre": "Péndulo del Terror",
                "tipo": "extrema",
                "altura_minima": 130,
                "detalles": {
                    "duracion_segundos": 90,
                    "capacidad_por_turno": 32,
                    "intensidad": 8,
                    "caracteristicas": ["pendulo", "giros", "alta_altura"],
                    "horarios": {
                        "apertura": "10:00",
                        "cierre": "21:00",
                        "mantenimiento": []
                    }
                }
            },
            
            # FAMILIARES
            {
                "nombre": "Tren Fantasma",
                "tipo": "familiar",
                "altura_minima": 110,
                "detalles": {
                    "duracion_segundos": 300,
                    "capacidad_por_turno": 30,
                    "intensidad": 4,
                    "caracteristicas": ["sustos", "oscuridad", "efectos_especiales"],
                    "horarios": {
                        "apertura": "10:00",
                        "cierre": "23:00",
                        "mantenimiento": []
                    }
                }
            },
            {
                "nombre": "Montaña Rusa Familiar",
                "tipo": "familiar",
                "altura_minima": 120,
                "detalles": {
                    "duracion_segundos": 150,
                    "capacidad_por_turno": 28,
                    "intensidad": 5,
                    "caracteristicas": ["curvas", "bajadas_suaves"],
                    "horarios": {
                        "apertura": "09:30",
                        "cierre": "22:30",
                        "mantenimiento": []
                    }
                }
            },
            {
                "nombre": "Casa del Árbol Gigante",
                "tipo": "familiar",
                "altura_minima": 100,
                "detalles": {
                    "duracion_segundos": 240,
                    "capacidad_por_turno": 40,
                    "intensidad": 3,
                    "caracteristicas": ["paseo_aereo", "vistas_panoramicas"],
                    "horarios": {
                        "apertura": "09:00",
                        "cierre": "23:00",
                        "mantenimiento": []
                    }
                }
            },
            {
                "nombre": "Río Rápido Aventura",
                "tipo": "familiar",
                "altura_minima": 115,
                "detalles": {
                    "duracion_segundos": 360,
                    "capacidad_por_turno": 24,
                    "intensidad": 5,
                    "caracteristicas": ["agua", "bajadas_moderadas", "giros"],
                    "horarios": {
                        "apertura": "10:30",
                        "cierre": "20:00",
                        "mantenimiento": []
                    }
                }
            },
            
            # INFANTILES
            {
                "nombre": "Carrusel Mágico",
                "tipo": "infantil",
                "altura_minima": 80,
                "detalles": {
                    "duracion_segundos": 180,
                    "capacidad_por_turno": 40,
                    "intensidad": 1,
                    "caracteristicas": ["musica", "luces", "caballos"],
                    "horarios": {
                        "apertura": "09:00",
                        "cierre": "22:00",
                        "mantenimiento": []
                    }
                }
            },
            {
                "nombre": "Tazas Giratorias",
                "tipo": "infantil",
                "altura_minima": 90,
                "detalles": {
                    "duracion_segundos": 120,
                    "capacidad_por_turno": 32,
                    "intensidad": 2,
                    "caracteristicas": ["giros_suaves", "colores"],
                    "horarios": {
                        "apertura": "09:00",
                        "cierre": "22:00",
                        "mantenimiento": []
                    }
                }
            },
            {
                "nombre": "Globos Voladores",
                "tipo": "infantil",
                "altura_minima": 85,
                "detalles": {
                    "duracion_segundos": 150,
                    "capacidad_por_turno": 24,
                    "intensidad": 2,
                    "caracteristicas": ["elevacion_suave", "giros_lentos"],
                    "horarios": {
                        "apertura": "09:30",
                        "cierre": "21:30",
                        "mantenimiento": []
                    }
                }
            },
            {
                "nombre": "Mini Montaña Rusa",
                "tipo": "infantil",
                "altura_minima": 95,
                "detalles": {
                    "duracion_segundos": 90,
                    "capacidad_por_turno": 20,
                    "intensidad": 3,
                    "caracteristicas": ["curvas_suaves", "velocidad_baja"],
                    "horarios": {
                        "apertura": "09:30",
                        "cierre": "22:00",
                        "mantenimiento": []
                    }
                }
            },
            {
                "nombre": "Trenecito del Parque",
                "tipo": "infantil",
                "altura_minima": 75,
                "detalles": {
                    "duracion_segundos": 420,
                    "capacidad_por_turno": 50,
                    "intensidad": 1,
                    "caracteristicas": ["paseo_tranquilo", "vistas"],
                    "horarios": {
                        "apertura": "09:00",
                        "cierre": "23:00",
                        "mantenimiento": []
                    }
                }
            },
            
            # ACUÁTICAS
            {
                "nombre": "Splash Mountain",
                "tipo": "acuatica",
                "altura_minima": 110,
                "detalles": {
                    "duracion_segundos": 240,
                    "capacidad_por_turno": 30,
                    "intensidad": 6,
                    "caracteristicas": ["agua", "caida_grande", "mojado_garantizado"],
                    "horarios": {
                        "apertura": "11:00",
                        "cierre": "20:00",
                        "mantenimiento": []
                    }
                }
            },
            {
                "nombre": "Rápidos del Cañón",
                "tipo": "acuatica",
                "altura_minima": 115,
                "detalles": {
                    "duracion_segundos": 300,
                    "capacidad_por_turno": 24,
                    "intensidad": 5,
                    "caracteristicas": ["agua", "giros", "corrientes"],
                    "horarios": {
                        "apertura": "11:00",
                        "cierre": "19:30",
                        "mantenimiento": []
                    }
                }
            },
            {
                "nombre": "Tobogán Acuático Gigante",
                "tipo": "acuatica",
                "altura_minima": 125,
                "detalles": {
                    "duracion_segundos": 60,
                    "capacidad_por_turno": 12,
                    "intensidad": 7,
                    "caracteristicas": ["agua", "alta_velocidad", "caida_libre"],
                    "horarios": {
                        "apertura": "11:30",
                        "cierre": "19:00",
                        "mantenimiento": [
                            {
                                "fecha_inicio": "2025-12-22",
                                "fecha_fin": "2025-12-22",
                                "motivo": "Limpieza de circuito"
                            }
                        ]
                    }
                }
            },
            {
                "nombre": "Piscina de Olas",
                "tipo": "acuatica",
                "altura_minima": 100,
                "detalles": {
                    "duracion_segundos": 600,
                    "capacidad_por_turno": 200,
                    "intensidad": 3,
                    "caracteristicas": ["agua", "olas", "natacion"],
                    "horarios": {
                        "apertura": "10:00",
                        "cierre": "20:00",
                        "mantenimiento": []
                    }
                }
            },
            {
                "nombre": "Lazy River",
                "tipo": "acuatica",
                "altura_minima": 90,
                "detalles": {
                    "duracion_segundos": 900,
                    "capacidad_por_turno": 100,
                    "intensidad": 2,
                    "caracteristicas": ["agua", "paseo_tranquilo", "flotadores"],
                    "horarios": {
                        "apertura": "10:00",
                        "cierre": "20:30",
                        "mantenimiento": []
                    }
                }
            },
            
            # ADICIONALES MIXTAS
            {
                "nombre": "Rueda de la Fortuna",
                "tipo": "familiar",
                "altura_minima": 105,
                "detalles": {
                    "duracion_segundos": 480,
                    "capacidad_por_turno": 48,
                    "intensidad": 2,
                    "caracteristicas": ["altura", "vistas_panoramicas", "lento"],
                    "horarios": {
                        "apertura": "09:00",
                        "cierre": "23:30",
                        "mantenimiento": []
                    }
                }
            },
            {
                "nombre": "Sillas Voladoras",
                "tipo": "familiar",
                "altura_minima": 120,
                "detalles": {
                    "duracion_segundos": 180,
                    "capacidad_por_turno": 36,
                    "intensidad": 4,
                    "caracteristicas": ["giros", "elevacion", "viento"],
                    "horarios": {
                        "apertura": "10:00",
                        "cierre": "22:00",
                        "mantenimiento": []
                    }
                }
            }
        ]
        
        contador_exitosos = 0
        
        for i, atraccion_data in enumerate(atracciones_data[:cantidad]):
            try:
                atraccion = AtraccionRepositorie.crear_atraccion(
                    nombre=atraccion_data["nombre"],
                    tipo=atraccion_data["tipo"],
                    altura_minima=atraccion_data["altura_minima"],
                    detalles=atraccion_data.get("detalles")
                )
                
                if atraccion:
                    self.atracciones_ids.append(atraccion.id)
                    contador_exitosos += 1
                    print(f"✓ Creada: {atraccion_data['nombre']} ({atraccion_data['tipo']})")
                
            except Exception as e:
                print(f"✗ Error al crear {atraccion_data['nombre']}: {e}")
        
        print(f"\n✅ Total atracciones creadas: {contador_exitosos}/{cantidad}")
        return contador_exitosos
    
    def generar_tickets(self, cantidad=150):
        """Genera tickets aleatorios para visitantes y atracciones"""
        print(f"\n{'='*60}")
        print(f"GENERANDO {cantidad} TICKETS")
        print(f"{'='*60}")
        
        if not self.visitantes_ids or not self.atracciones_ids:
            print("✗ Error: Debe generar visitantes y atracciones primero")
            return 0
        
        # Tipos de ticket
        tipos_ticket = ["general", "colegio", "empleado"]
        
        # Descuentos disponibles
        descuentos_disponibles = [
            "estudiante", "jubilado", "familia_numerosa", 
            "descuento_grupo", "promocion_especial"
        ]
        
        # Servicios extra
        servicios_disponibles = [
            "fast_pass", "comida_incluida", "parking_vip",
            "foto_digital", "taquilla_gratis"
        ]
        
        # Métodos de pago
        metodos_pago = ["tarjeta", "efectivo", "paypal", "bizum", "transferencia"]
        
        contador_exitosos = 0
        fecha_actual = datetime.now().date()
        
        for i in range(cantidad):
            try:
                # Selecciona visitante aleatorio
                visitante_id = random.choice(self.visitantes_ids)
                
                # 30% de probabilidad de ticket general, 70% específico
                atraccion_id = None
                if random.random() > 0.3:
                    atraccion_id = random.choice(self.atracciones_ids)
                
                # Fecha de visita (entre hoy y 30 días después)
                dias_adelante = random.randint(0, 30)
                fecha_visita = fecha_actual + timedelta(days=dias_adelante)
                
                # Tipo de ticket con probabilidades
                rand = random.random()
                if rand < 0.6:
                    tipo_ticket = "general"
                elif rand < 0.85:
                    tipo_ticket = "colegio"
                else:
                    tipo_ticket = "empleado"
                
                # Precio según tipo
                if tipo_ticket == "general":
                    precio_base = random.uniform(35, 50)
                elif tipo_ticket == "colegio":
                    precio_base = random.uniform(15, 28)
                else:  # empleado
                    precio_base = random.uniform(10, 20)
                
                # Descuentos (0-2 descuentos aleatorios)
                num_descuentos = random.randint(0, 2)
                descuentos = random.sample(descuentos_disponibles, num_descuentos)
                
                # Servicios extra (0-3 servicios)
                num_servicios = random.randint(0, 3)
                servicios = random.sample(servicios_disponibles, num_servicios)
                
                # Ajuste de precio por servicios
                precio_final = precio_base + (len(servicios) * random.uniform(5, 15))
                
                # Detalles de compra
                detalles_compra = {
                    "precio": round(precio_final, 2),
                    "descuentos_aplicados": descuentos,
                    "servicios_extra": servicios,
                    "metodo_pago": random.choice(metodos_pago)
                }
                
                # Crear ticket
                ticket = TicketRepositorie.crear_ticket(
                    visitante_id=visitante_id,
                    fecha_visita=fecha_visita,
                    tipo_ticket=tipo_ticket,
                    detalles_compra=detalles_compra,
                    atraccion_id=atraccion_id
                )
                
                if ticket:
                    self.tickets_ids.append(ticket.id)
                    contador_exitosos += 1
                    
                    # Marcar algunos tickets como usados (20% de probabilidad)
                    if random.random() < 0.2 and fecha_visita <= fecha_actual:
                        TicketRepositorie.marcar_ticket_usado(ticket.id)
                    
                    if (contador_exitosos) % 20 == 0:
                        print(f"✓ Creados {contador_exitosos} tickets...")
                
            except Exception as e:
                print(f"✗ Error al crear ticket {i+1}: {e}")
        
        print(f"\n✅ Total tickets creados: {contador_exitosos}/{cantidad}")
        return contador_exitosos
    
    def ejecutar_ingesta_completa(self):
        """Ejecuta la ingesta completa de datos"""
        print("\n" + "="*60)
        print("INICIANDO INGESTA DE DATOS")
        print("="*60)
        
        inicio = datetime.now()
        
        # Generar datos
        visitantes = self.generar_visitantes(100)
        atracciones = self.generar_atracciones(20)
        tickets = self.generar_tickets(150)
        
        fin = datetime.now()
        duracion = (fin - inicio).total_seconds()
        
        # Resumen final
        print(f"\n{'='*60}")
        print("RESUMEN DE INGESTA")
        print(f"{'='*60}")
        print(f"✓ Visitantes creados: {visitantes}")
        print(f"✓ Atracciones creadas: {atracciones}")
        print(f"✓ Tickets creados: {tickets}")
        print(f"⏱ Tiempo total: {duracion:.2f} segundos")
        print(f"{'='*60}\n")
        
        return {
            "visitantes": visitantes,
            "atracciones": atracciones,
            "tickets": tickets,
            "duracion": duracion
        }


def main():
    """Función principal para ejecutar la ingesta"""
    print("\n🎢 SISTEMA DE INGESTA DE DATOS - PARQUE DE ATRACCIONES 🎢\n")
    
    # Conectar a la base de datos
    if not conectar_db():
        print("❌ No se pudo conectar a la base de datos")
        return
    
    try:
        # Crear instancia de ingesta
        ingesta = Ingesta()
        
        # Ejecutar ingesta completa
        resultado = ingesta.ejecutar_ingesta_completa()
        
        print("✅ Ingesta completada exitosamente")
        print("\nPuedes comenzar a usar el sistema con los datos cargados.")
        
    except Exception as e:
        print(f"\n❌ Error durante la ingesta: {e}")
    
    finally:
        # Cerrar conexión
        cerrar_db()


if __name__ == "__main__":
    main()