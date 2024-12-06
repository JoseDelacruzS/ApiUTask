from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UsuarioResponse, UsuarioUpdate
from app.crud import get_usuario, update_usuario, delete_usuario
from app.dependencies import get_current_user  # Importar get_current_user
from app.models import Usuario
import uuid
from pathlib import Path

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
    user_update: UsuarioUpdate,
    avatar: UploadFile = File(None),  # Archivo opcional para el nuevo avatar
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user)
):
    """
    Actualizar los datos del usuario autenticado.
    """
    # Si se recibe un nuevo avatar, procesarlo
    avatar_url = user.avatar  # Mantener el avatar actual si no se envía uno nuevo
    if avatar:
        if avatar.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="El avatar debe ser de tipo JPEG o PNG.")
        
        # Eliminar el avatar antiguo si existe, si es necesario (esto depende de cómo manejes el almacenamiento)
        # Aquí puedes eliminar el archivo antiguo en el sistema de archivos si lo deseas

        # Guardar el nuevo avatar
        avatar_filename = f"{uuid.uuid4()}_{avatar.filename}"
        avatar_path = UPLOAD_DIR / avatar_filename
        
        with avatar_path.open("wb") as f:
            content = await avatar.read()
            f.write(content)
        
        # Actualizar la URL del avatar
        avatar_url = f"/static/{avatar_filename}"

    # Actualizar los datos del usuario
    usuario_data = user_update.dict(exclude_unset=True)
    usuario_data["avatar"] = avatar_url  # Actualizar el avatar si se recibió uno nuevo

    # Llamar al CRUD para actualizar el usuario
    return update_usuario(db, user_id=user.id, user_update=usuario_data)

@router.delete("/")
def delete_user(db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    """
    Eliminar la cuenta del usuario autenticado.
    """
    delete_usuario(db, user_id=user.id)
    return {"message": "Usuario eliminado correctamente"}
