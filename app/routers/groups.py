from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import GrupoCreate, GrupoResponse
from app.models import Usuario
from app.dependencies import get_current_user
from app.crud import create_grupo, get_grupo, get_grupos_by_user, delete_grupo, update_grupo

router = APIRouter(prefix="/groups", tags=["groups"])


@router.post("/", response_model=GrupoResponse)
def create_group(
    group: GrupoCreate, 
    db: Session = Depends(get_db), 
    user: Usuario = Depends(get_current_user)
):
    """
    Crear un nuevo grupo asociado al usuario autenticado.
    """
    return create_grupo(db, group, user_id=user.id)

@router.get("/{group_id}", response_model=GrupoResponse)
def get_group(
    group_id: int, 
    db: Session = Depends(get_db), 
    user: Usuario = Depends(get_current_user)
):
    """
    Obtener un grupo específico solo si pertenece al usuario autenticado.
    """
    group = get_grupo(db, grupo_id=group_id)
    if not group or group.user_id != user.id:
        raise HTTPException(status_code=404, detail="Grupo no encontrado o no autorizado")
    return group

@router.get("/", response_model=list[GrupoResponse])
def get_groups_for_user(
    db: Session = Depends(get_db), 
    user: Usuario = Depends(get_current_user)
):
    """
    Obtener todos los grupos del usuario autenticado.
    """
    return get_grupos_by_user(db, user_id=user.id)

@router.delete("/{group_id}")
def delete_group(
    group_id: int, 
    db: Session = Depends(get_db), 
    user: Usuario = Depends(get_current_user)
):
    """
    Eliminar un grupo solo si pertenece al usuario autenticado.
    """
    group = get_grupo(db, grupo_id=group_id)
    if not group or group.user_id != user.id:
        raise HTTPException(status_code=404, detail="Grupo no encontrado o no autorizado")
    
    # Pasa grupo_id y no group_id aquí
    delete_grupo(db, grupo_id=group_id)  # Aquí se pasa el argumento correctamente como `grupo_id`
    
    return {"message": "Grupo eliminado correctamente"}

@router.put("/{group_id}", response_model=GrupoResponse)
def update_group(
    group_id: int, 
    group_update: GrupoCreate,  # El modelo que usas para actualizar un grupo
    db: Session = Depends(get_db), 
    user: Usuario = Depends(get_current_user)
):
    """
    Actualizar un grupo solo si pertenece al usuario autenticado.
    """
    group = get_grupo(db, grupo_id=group_id)
    if not group or group.user_id != user.id:
        raise HTTPException(status_code=404, detail="Grupo no encontrado o no autorizado")
    
    # Se pasa el user_id del usuario autenticado al actualizar el grupo
    return update_grupo(db, grupo_id=group_id, grupo_update=group_update)
