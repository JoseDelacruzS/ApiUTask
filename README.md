# 🔥 API REST con Flask y SQLite

Esta API REST está desarrollada con **Flask** y utiliza **SQLite** como base de datos ligera. Ofrece funcionalidades CRUD para manejar **usuarios**, **tareas** y **grupos**, ideal para aplicaciones de gestión o proyectos backend simples.

---

## 🚀 Funcionalidades principales

- **Usuarios:** Crear, leer, actualizar y eliminar usuarios.
- **Tareas:** CRUD completo para tareas asignadas a usuarios o grupos.
- **Grupos:** Gestión de grupos para organizar usuarios y tareas.
- Manejo básico de relaciones entre usuarios, tareas y grupos.

---

## 🛠️ Tecnologías usadas

- Python 3.x  
- Flask  
- SQLite  
- Flask-RESTful (opcional para estructurar recursos)  
- SQLAlchemy ORM (para manejo sencillo de la base de datos)

---

## 📦 Instalación y ejecución

1. Clona el repositorio:

   ```bash
   git clone https://github.com/TU_USUARIO/tu-api-flask.git
   cd tu-api-flask

2. Crea y activa un entorno virtual (recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate       # Windows
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación:

   ```bash
   flask run
   ```

---

## 🗂️ Endpoints disponibles

### Usuarios

| Método | Ruta        | Descripción              |
| ------ | ----------- | ------------------------ |
| GET    | /users      | Lista todos los usuarios |
| POST   | /users      | Crea un nuevo usuario    |
| GET    | /users/<id> | Obtiene usuario por ID   |
| PUT    | /users/<id> | Actualiza usuario por ID |
| DELETE | /users/<id> | Elimina usuario por ID   |

### Tareas

| Método | Ruta        | Descripción            |
| ------ | ----------- | ---------------------- |
| GET    | /tasks      | Lista todas las tareas |
| POST   | /tasks      | Crea una nueva tarea   |
| GET    | /tasks/<id> | Obtiene tarea por ID   |
| PUT    | /tasks/<id> | Actualiza tarea por ID |
| DELETE | /tasks/<id> | Elimina tarea por ID   |

### Grupos

| Método | Ruta         | Descripción            |
| ------ | ------------ | ---------------------- |
| GET    | /groups      | Lista todos los grupos |
| POST   | /groups      | Crea un nuevo grupo    |
| GET    | /groups/<id> | Obtiene grupo por ID   |
| PUT    | /groups/<id> | Actualiza grupo por ID |
| DELETE | /groups/<id> | Elimina grupo por ID   |

---

## 🧰 Estructura del proyecto

```
tu-api-flask/
│
├── app.py               # Archivo principal con la app Flask
├── models.py            # Definición de modelos SQLAlchemy
├── routes/              # Módulo con rutas y lógica CRUD
├── database.db          # Archivo SQLite generado
├── requirements.txt     # Dependencias de Python
└── README.md            # Documentación
```

---

## 🔧 Configuración adicional

* Puedes modificar la configuración de la base de datos en `app.py`.
* Para producción, se recomienda usar una base de datos más robusta y manejar autenticación.

---

## 🧑‍💻 Autor

**José de la Cruz (Chucho)**
Backend Developer

---

## ⚖️ Licencia

Este proyecto es de código abierto y libre para uso educativo y comercial.

