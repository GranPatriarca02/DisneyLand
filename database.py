# =============================================================================
# CONFIGURACIÓN DE BASE DE DATOS
# =============================================================================
from peewee import *
import envyte

# Configuración de la conexión a PostgreSQL en Supabase
# Lee las credenciales desde el archivo .env
db = PostgresqlDatabase(
    envyte.get("SUPABASE_DB_NAME"),      
    host=envyte.get("SUPABASE_DB_HOST"), 
    port=int(envyte.get("SUPABASE_DB_PORT")), 
    user=envyte.get("SUPABASE_DB_USER"),     
    password=envyte.get("SUPABASE_DB_PASSWORD") 
)

def conectar_db():
    """Establece conexión con la base de datos"""
    try:
        db.connect()
        print("Conectado a la base de datos")
        return True
    except Exception as e:
        print(f"Error al conectar: {e}")
        return False

def cerrar_db():
    """Cierra la conexión a la base de datos de forma segura"""
    if not db.is_closed():
        db.close()
        print("Desconectado de la base de datos")
