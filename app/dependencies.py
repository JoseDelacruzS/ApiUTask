from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Session as DBSession  # El modelo de sesiones que creamos previamente
from app.database import get_db

def get_current_user(request: Request, db: Session = Depends(get_db)):
    # Obtener el session_id del encabezado 'sesion'
    session_id = request.headers.get("sesion")
    
    if not session_id:
        raise HTTPException(status_code=401, detail="No session header found")
    
    # Verificar si el session_id es válido
    db_session = db.query(DBSession).filter(DBSession.session_id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    # Obtener el usuario asociado con el session_id
    user = db_session.user  # Relación definida en el modelo de sesión
    return user
