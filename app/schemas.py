from pydantic import BaseModel, EmailStr
from datetime import datetime
from fastapi import UploadFile
from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional

# Base para los datos comunes de usuario
class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    avatar: Optional[str] = None
    nickname: str

# Para crear un usuario (entrada de datos)
class UsuarioCreate(UsuarioBase):
    password: str

# Para actualizar un usuario (entrada de datos)
class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    avatar: Optional[str] = None
    nickname: Optional[str] = None

    class Config:
        from_attributes  = True

# Para responder con información del usuario (salida de datos)
class UsuarioResponse(UsuarioBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserRequest(BaseModel):
    user: UsuarioCreate
    avatar: Optional[UploadFile] = None


# Base para los datos comunes de grupo
class GrupoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

# Esquema para crear un grupo (entrada)
class GrupoCreate(GrupoBase):
    pass  # No incluye user_id porque se obtiene automáticamente del usuario autenticado

# Esquema para responder datos de un grupo (salida)
class GrupoResponse(GrupoBase):
    id: int
    user_id: int
    created_at: datetime
    descripcion: str = "Sin descripción" 

    class Config:
        from_attributes  = True

# Esquema para actualizar un grupo (entrada)
class GrupoUpdate(GrupoBase):
    pass 


# Esquema base para Tarea
class TareaBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    due_date: datetime
    imagen: Optional[str] = None

# Esquema para crear una tarea (entrada)
class TareaCreate(TareaBase):
    grupo_id: Optional[int] = None  # Asociar la tarea opcionalmente a un grupo

# Esquema para actualizar una tarea (entrada)
class TareaUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    due_date: Optional[datetime] = None
    imagen: Optional[str] = None
    grupo_id: Optional[int] = None

# Esquema para responder datos de una tarea (salida)
class TareaResponse(TareaBase):
    id: int
    grupo_id: Optional[int] = None
    user_id: int  # Se incluye en la respuesta para identificar al usuario propietario

    class Config:
        from_attributes = True
    id: int
    user_id: int
    grupo_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

