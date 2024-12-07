from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    telefono = Column(String, nullable=True)
    direccion = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    nickname = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

       # Relación con Grupo (agregada)
    grupos = relationship("Grupo", back_populates="usuario")

    # Relación con Tarea (agregada)
    tareas = relationship("Tarea", back_populates="usuario")

class Grupo(Base):
    __tablename__ = "grupos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
        # Relación con Usuario
    usuario = relationship("Usuario", back_populates="grupos")

    # Relación con Tarea (agregada)
    tareas = relationship("Tarea", back_populates="grupo")

class Tarea(Base):
    __tablename__ = "tareas"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    due_date = Column(String, nullable=False)  # Cambié el tipo de `DateTime` a `String` para mantenerlo como texto
    created_at = Column(DateTime, default=datetime.utcnow)
    imagen = Column(String, nullable=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    grupo = relationship("Grupo", back_populates="tareas")
    usuario = relationship("Usuario", back_populates="tareas")

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)  # El identificador único de la sesión
    user_id = Column(Integer, ForeignKey("usuarios.id"))  # Relación con el usuario
    user = relationship("Usuario")  # Relación con la tabla de usuarios

    def __repr__(self):
        return f"<Session(session_id={self.session_id}, user_id={self.user_id})>"