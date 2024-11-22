from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el motor de base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crear la sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Función para obtener una sesión de base de datos (Dependency)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
