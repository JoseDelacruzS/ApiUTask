from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UsuarioResponse, UsuarioUpdate
from app.crud import get_usuario, update_usuario, delete_usuario
from app.dependencies import get_current_user  # Importar get_current_user
from app.models import Usuario

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=UsuarioResponse)
def get_user(db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    """
    Obtener los datos del usuario autenticado.
    """
    return user

@router.put("/", response_model=UsuarioResponse)
def update_user(user_update: UsuarioUpdate, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    """
    Actualizar los datos del usuario autenticado.
    """
    return update_usuario(db, user_id=user.id, user_update=user_update)

@router.delete("/")
def delete_user(db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    """
    Eliminar la cuenta del usuario autenticado.
    """
    delete_usuario(db, user_id=user.id)
    return {"message": "Usuario eliminado correctamente"}
