from fastapi import FastAPI
from .database import engine, Base
from .routers import users, tasks, groups, auth
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Registrar los routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(groups.router)
app.mount("/static", StaticFiles(directory="uploaded_images"), name="static")