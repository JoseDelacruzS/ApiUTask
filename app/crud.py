from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from datetime import datetime
from app.schemas import UsuarioUpdate
from pydantic import List

# Crear un objeto CryptContext para el manejo de contraseñas con hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Funciones CRUD para Usuarios

def get_usuario(db: Session, user_id: int):  # Cambié `usuario_id` a `user_id`
    return db.query(models.Usuario).filter(models.Usuario.id == user_id).first()

def get_usuario_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = models.Usuario(
        nombre=usuario.nombre, 
        apellido=usuario.apellido, 
        email=usuario.email, 
        password=usuario.password,  # Se deja la contraseña tal cual, ya está hasheada antes
        telefono=usuario.telefono,
        direccion=usuario.direccion, 
        avatar=usuario.avatar, 
        nickname=usuario.nickname)
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, user_id: int, user_update: dict):
    # Buscar al usuario en la base de datos
    db_user = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
    if not db_user:
        return None  # O lanzar una excepción si el usuario no existe

    # Actualiza solo los campos que están presentes en user_update (como un diccionario)
    if user_update.get('nombre'):
        db_user.nombre = user_update['nombre']
    if user_update.get('apellido'):
        db_user.apellido = user_update['apellido']
    if user_update.get('email'):
        db_user.email = user_update['email']
    if user_update.get('telefono'):
        db_user.telefono = user_update['telefono']
    if user_update.get('direccion'):
        db_user.direccion = user_update['direccion']
    if user_update.get('avatar'):
        db_user.avatar = user_update['avatar']
    if user_update.get('nickname'):
        db_user.nickname = user_update['nickname']

    # Guardar los cambios en la base de datos
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_usuario(db: Session, user_id: int):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        return db_usuario
    return None


# Funciones CRUD para Grupos

def get_grupo(db: Session, grupo_id: int):
    """
    Obtener un grupo por su ID.
    """
    return db.query(models.Grupo).filter(models.Grupo.id == grupo_id).first()

def get_grupos_by_user(db: Session, user_id: int):
    """
    Obtener todos los grupos de un usuario específico.
    """
    return db.query(models.Grupo).filter(models.Grupo.user_id == user_id).all()

def create_grupo(db: Session, grupo: schemas.GrupoCreate, user_id: int):
    """
    Crear un nuevo grupo asociado a un usuario.
    """
    db_grupo = models.Grupo(
        nombre=grupo.nombre,
        descripcion=grupo.descripcion,  # Asignamos la descripción al crear
        user_id=user_id
    )
    db.add(db_grupo)
    db.commit()
    db.refresh(db_grupo)
    return db_grupo

def delete_grupo(db: Session, grupo_id: int):
    """
    Eliminar un grupo por su ID.
    """
    db_grupo = db.query(models.Grupo).filter(models.Grupo.id == grupo_id).first()
    if db_grupo:
        db.delete(db_grupo)
        db.commit()
        return db_grupo
    return None

def update_grupo(db: Session, grupo_id: int, grupo_update: schemas.GrupoCreate):
    """
    Actualiza un grupo específico.
    """
    db_grupo = db.query(models.Grupo).filter(models.Grupo.id == grupo_id).first()
    if db_grupo:
        db_grupo.nombre = grupo_update.nombre
        db_grupo.descripcion = grupo_update.descripcion  # Actualizamos la descripción
        db.commit()
        db.refresh(db_grupo)
        return db_grupo
    return None


# Funciones CRUD para Tareas

def get_tarea(db: Session, tarea_id: int):
    """
    Obtener una tarea específica por su ID.
    """
    return db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()

def get_tareas_by_user(db: Session, user_id: int):
    """
    Obtener todas las tareas asociadas a un usuario.
    """
    return db.query(models.Tarea).filter(models.Tarea.user_id == user_id).all()

def get_tareas(db: Session, user_id: int, limit: int = 10):
    """
    Obtener un número limitado de tareas asociadas a un usuario.
    """
    return db.query(models.Tarea).filter(models.Tarea.user_id == user_id).limit(limit).all()

def create_tarea(db: Session, tarea: schemas.TareaCreate, user_id: int):
    """
    Crear una nueva tarea asociada a un usuario.
    """
    db_tarea = models.Tarea(
        titulo=tarea.titulo, 
        descripcion=tarea.descripcion, 
        due_date=tarea.due_date, 
        imagen=tarea.imagen, 
        grupo_id=tarea.grupo_id, 
        user_id=user_id
    )
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

def update_tarea(db: Session, tarea_id: int, tarea_update: dict):
    """
    Actualizar una tarea específica.
    """
    db_tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if not db_tarea:
        return None  # Si no se encuentra la tarea, retornar None

    # Actualiza solo los campos que están presentes en tarea_update (como un diccionario)
    if tarea_update.get('titulo'):
        db_tarea.titulo = tarea_update['titulo']
    if tarea_update.get('descripcion'):
        db_tarea.descripcion = tarea_update['descripcion']
    if tarea_update.get('due_date'):
        db_tarea.due_date = tarea_update['due_date']
    if tarea_update.get('imagen'):
        db_tarea.imagen = tarea_update['imagen']
    if tarea_update.get('grupo_id'):
        db_tarea.grupo_id = tarea_update['grupo_id']

    # Guardar los cambios en la base de datos
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

def delete_tarea(db: Session, tarea_id: int):
    """
    Eliminar una tarea específica.
    """
    db_tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if db_tarea:
        db.delete(db_tarea)
        db.commit()
        return db_tarea
    return None

def get_tareas_by_user_and_group(db: Session, user_id: int, group_id: int) -> List[models.Tarea]:
    """
    Obtener todas las tareas asociadas a un usuario y a un grupo específico.
    """
    return db.query(models.Tarea).filter(models.Tarea.user_id == user_id, models.Tarea.grupo_id == group_id).all()
# Sesiones de usuario

def create_session(db: Session, session_id: str, user_id: int):
    db_session = Session(session_id=session_id, user_id=user_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session