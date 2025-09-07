import os
import shutil
from app import create_app
from models import db

# Ruta de la base de datos SQLite
DB_PATH = os.path.join(os.getcwd(), "app.db")

# Eliminar base de datos
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("[OK] Base de datos eliminada")
else:
    print("[INFO] No se encontró base de datos para eliminar")

# Eliminar carpeta de migraciones
if os.path.exists("migrations"):
    shutil.rmtree("migrations")
    print("[OK] Carpeta de migraciones eliminada")

# Crear la app para inicializar la base
app = create_app()
with app.app_context():
    # Re-crear migraciones
    os.system("flask db init")
    os.system('flask db migrate -m "Initial migration"')
    os.system("flask db upgrade")
    print("[OK] Base de datos reiniciada correctamente")
