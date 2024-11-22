from fastapi import Response, APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from app.models import Session as DBSession
from app.models import Usuario
from app.database import get_db
from app.schemas import UsuarioCreate, UsuarioResponse, UserRequest
from app.crud import create_usuario, get_usuario_by_email
from passlib.context import CryptContext
import uuid
from pydantic import BaseModel
import shutil
from pathlib import Path
from typing import List

class LoginRequest(BaseModel):
    email: str
    password: str

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Crear la carpeta de imágenes si no existe
UPLOAD_DIR = Path("uploaded_images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@router.post("/register", response_model=UsuarioResponse)
async def register_user(
    nombre: str = Form(...),
    apellido: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    telefono: str = Form(None),
    direccion: str = Form(None),
    nickname: str = Form(...),
    avatar: UploadFile = File(None),  # Este campo es para el archivo
    db: Session = Depends(get_db)
):
    # Verificar si el email ya existe
    from app.crud import get_usuario_by_email
    if get_usuario_by_email(db, email=email):
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # Procesar el archivo de avatar
    avatar_url = None
    if avatar:
        if avatar.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="El archivo debe ser una imagen JPEG o PNG.")
        
        # Guardar el archivo en el servidor
        avatar_filename = f"{uuid.uuid4()}_{avatar.filename}"
        avatar_path = UPLOAD_DIR / avatar_filename

        with avatar_path.open("wb") as f:
            content = await avatar.read()
            f.write(content)
        
        # Crear la URL para la imagen (puedes ajustarla según tus necesidades)
        avatar_url = f"/static/{avatar_filename}"

    # Hashear la contraseña
    hashed_password = pwd_context.hash(password)

    # Crear el usuario
    usuario_data = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "password": hashed_password,
        "telefono": telefono,
        "direccion": direccion,
        "nickname": nickname,
        "avatar": avatar_url,
    }
    from app.schemas import UsuarioCreate
    usuario = UsuarioCreate(**usuario_data)
    return create_usuario(db, usuario)

@router.post("/login")
def login_user(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    # Buscar usuario por email
    user = get_usuario_by_email(db, email=request.email)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario no existe")
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    # Generar un identificador de sesión único
    session_id = str(uuid.uuid4())

    # Crear una nueva sesión en la base de datos
    db_session = DBSession(session_id=session_id, user_id=user.id)

    # Agregar la sesión a la base de datos
    db.add(db_session)
    db.commit()

    # Establecer una cookie de sesión
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    return {"message": "Inicio de sesión exitoso", "user_id": user.id}
