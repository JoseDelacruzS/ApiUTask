from fastapi import APIRouter, Depends, HTTPException,Form,  UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UsuarioResponse, UsuarioUpdate
from app.crud import get_usuario, update_usuario, delete_usuario
from app.dependencies import get_current_user  # Importar get_current_user
from app.models import Usuario
import uuid
from pathlib import Path
from typing import Optional
from pydantic import EmailStr

# Crear la carpeta de imágenes si no existe
UPLOAD_DIR = Path("uploaded_images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=UsuarioResponse)
def get_user(db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    """
    Obtener los datos del usuario autenticado.
    """
    return user

@router.put("/", response_model=UsuarioResponse)
async def update_user(
    nombre: Optional[str] = Form(None),
    apellido: Optional[str] = Form(None),
    email: Optional[EmailStr] = Form(None),
    telefono: Optional[str] = Form(None),
    direccion: Optional[str] = Form(None),
    avatar: UploadFile = File(None),  # Archivo opcional para el avatar
    nickname: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user)
):
    """
    Actualizar los datos del usuario autenticado.
    """
    # Mantener los datos actuales del usuario si no se envían en la solicitud
    usuario_data = {
        "nombre": nombre or user.nombre,
        "apellido": apellido or user.apellido,
        "email": email or user.email,
        "telefono": telefono or user.telefono,
        "direccion": direccion or user.direccion,
        "nickname": nickname or user.nickname,
    }

    # Procesar el nuevo avatar si se envió uno
    avatar_url = user.avatar  # Mantener el avatar actual si no se envía uno nuevo
    if avatar:
        if avatar.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="El avatar debe ser de tipo JPEG o PNG.")
        
        # Eliminar el avatar antiguo si es necesario
        # Aquí puedes eliminar el archivo antiguo si lo deseas

        # Guardar el nuevo avatar
        avatar_filename = f"{uuid.uuid4()}_{avatar.filename}"
        avatar_path = UPLOAD_DIR / avatar_filename
        
        with avatar_path.open("wb") as f:
            content = await avatar.read()
            f.write(content)
        
        # Actualizar la URL del avatar
        avatar_url = f"/static/{avatar_filename}"

    # Añadir la URL del avatar al diccionario de datos del usuario
    usuario_data["avatar"] = avatar_url

    # Llamar al CRUD para actualizar el usuario
    return update_usuario(db, user_id=user.id, user_update=usuario_data)

@router.delete("/")
def delete_user(db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    """
    Eliminar la cuenta del usuario autenticado.
    """
    delete_usuario(db, user_id=user.id)
    return {"message": "Usuario eliminado correctamente"}
