import os
from pathlib import Path
from dotenv import load_dotenv

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Cargar variables del .env si existe
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-dev")

    # Forzar SQLite para desarrollo (ignorar DATABASE_URL si no estamos en producción)
    ENV = os.getenv("FLASK_ENV", "development")

    if ENV == "production":
        # En producción, usa DATABASE_URL si existe
        DATABASE_URL = os.getenv("DATABASE_URL")

        # Ajustar si Heroku o similar usa postgres://
        if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
    else:
        # Para desarrollo, siempre SQLite local
        DATABASE_URL = f"sqlite:///{BASE_DIR / 'ttournament_dev.db'}"

    # URI para SQLAlchemy
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
