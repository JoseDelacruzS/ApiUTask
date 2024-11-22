from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from app.dependencies import get_current_user
from app.models import Usuario
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import TareaCreate, TareaResponse, TareaUpdate
from app.crud import (
    create_tarea,
    get_tarea,
    get_tareas_by_user,
    update_tarea,
    delete_tarea,
)
import uuid
from pathlib import Path

router = APIRouter(prefix="/tasks", tags=["tasks"])

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Crear la carpeta de imágenes si no existe
UPLOAD_DIR = Path("task_images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@router.post("/", response_model=TareaResponse)
async def create_task(
    titulo: str = Form(...),
    descripcion: str = Form(None),
    due_date: str = Form(...),  # Se recibirá como string y se convertirá a datetime
    grupo_id: int = Form(None),
    imagen: UploadFile = File(None),  # Archivo opcional para la imagen
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    """
    Crear una nueva tarea para el usuario autenticado.
    """
    # Validar y procesar la imagen
    imagen_url = None
    if imagen:
        if imagen.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="La imagen debe ser de tipo JPEG o PNG.")
        
        # Guardar el archivo con un nombre único
        imagen_filename = f"{uuid.uuid4()}_{imagen.filename}"
        imagen_path = UPLOAD_DIR / imagen_filename
        
        with imagen_path.open("wb") as f:
            content = await imagen.read()
            f.write(content)
        
        # URL pública para acceder a la imagen (ajustar según tu configuración de servidor)
        imagen_url = f"/static/{imagen_filename}"

    # Convertir due_date a datetime
    from datetime import datetime
    try:
        due_date_dt = datetime.fromisoformat(due_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="El formato de la fecha de vencimiento es inválido.")

    # Crear el objeto de la tarea
    tarea_data = {
        "titulo": titulo,
        "descripcion": descripcion,
        "due_date": due_date_dt,
        "imagen": imagen_url,
        "grupo_id": grupo_id,
        "user_id": user.id,
    }

    # Llamar al CRUD para crear la tarea
    tarea = TareaCreate(**tarea_data)
    return create_tarea(db, tarea, user_id=user.id)


@router.get("/{task_id}", response_model=TareaResponse)
def get_task(
    task_id: int, 
    db: Session = Depends(get_db), 
    user: Usuario = Depends(get_current_user)
):
    """
    Obtener una tarea específica por su ID, solo si pertenece al usuario autenticado.
    """
    task = get_tarea(db, tarea_id=task_id)
    if not task or task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Tarea no encontrada o no autorizada")
    return task


@router.get("/", response_model=list[TareaResponse])
def get_tasks_for_user(
    db: Session = Depends(get_db), 
    user: Usuario = Depends(get_current_user)
):
    """
    Obtener todas las tareas del usuario autenticado.
    """
    return get_tareas_by_user(db, user_id=user.id)


@router.put("/{task_id}", response_model=TareaResponse)
def update_task(
    task_id: int, 
    task_update: TareaUpdate, 
    db: Session = Depends(get_db), 
    user: Usuario = Depends(get_current_user)
):
    """
    Actualizar una tarea específica del usuario autenticado.
    """
    task = get_tarea(db, tarea_id=task_id)
    if not task or task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Tarea no encontrada o no autorizada")
    return update_tarea(db, tarea_id=task_id, tarea_update=task_update)


@router.delete("/{task_id}")
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db), 
    user: Usuario = Depends(get_current_user)
):
    """
    Eliminar una tarea específica del usuario autenticado.
    """
    task = get_tarea(db, tarea_id=task_id)
    if not task or task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Tarea no encontrada o no autorizada")
    delete_tarea(db, tarea_id=task_id)
    return {"message": "Tarea eliminada correctamente"}
