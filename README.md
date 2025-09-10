# 🏓 TT-Manager: Gestor de Torneos de Tenis de Mesa
Aplicación web desarrollada en Flask para gestionar torneos de tenis de mesa con fase de grupos y eliminación directa, incluyendo registro de jugadores y control de resultados.

## 📖 ¿Qué hace este proyecto?
Este sistema permite:
- Registrar jugadores para un torneo.
- Crear grupos y asignar jugadores aleatoriamente.
- Gestionar partidos en fase de grupos.
- Generar eliminación directa con clasificación automática.
- Mostrar resultados y tablas actualizadas.

## 📦 Requisitos previos
Antes de comenzar, necesitas tener instalado:
- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Virtualenv (opcional, pero recomendado)
- SQLite (ya viene incluido con Python)

## 🛠️ Tecnologías usadas
- Backend: Flask (framework web para Python)
- Base de datos: SQLite con SQLAlchemy (ORM)
- Migraciones: Flask-Migrate (Alembic)
- Frontend: HTML5 + CSS + Bootstrap + Jinja2 (motor de plantillas)

## 📂 Estructura del proyecto
TT-Manager/
│
├── app.py                  # Punto de entrada principal
├── config.py               # Configuración de la app y la base de datos
├── models.py               # Modelos de datos (SQLAlchemy)
├── reset_db.py             # Script para reiniciar la base de datos
├── requirements.txt        # Lista de dependencias
│
├── routes/                 # Carpeta con las rutas del proyecto
│   ├── public.py           # Rutas públicas (registro, inicio)
│   └── admin.py            # Rutas administrativas (gestión)
│
├── templates/              # Plantillas HTML
│   ├── base.html           # Layout base (header, footer)
│   ├── index.html          # Página principal
│   ├── register.html       # Registro de jugadores
│   ├── groups.html         # Fase de grupos
│   └── elimination.html    # Eliminación directa
│
├── static/                 # Archivos estáticos (CSS, JS, imágenes)
│   ├── css/
│   └── js/main.js
│
└── migrations/             # Carpeta para migraciones de la base de datos

## 🚀 Instalación y ejecución paso a paso
1. Clonar el repositorio:
   git clone https://github.com/tuusuario/TT-Manager.git
   cd TT-Manager

2. Crear un entorno virtual:
   Windows (PowerShell):
       python -m venv venv
       venv\Scripts\activate
   Linux/Mac:
       python3 -m venv venv
       source venv/bin/activate

3. Instalar dependencias:
   pip install -r requirements.txt

4. Configurar variables de entorno:
   Windows:
       $env:FLASK_APP = "app.py"
       $env:FLASK_ENV = "development"
   Linux/Mac:
       export FLASK_APP=app.py
       export FLASK_ENV=development

5. Inicializar la base de datos:
   flask db init
   flask db migrate -m "Inicial"
   flask db upgrade

6. Ejecutar la aplicación:
   flask run
   Acceder en: http://127.0.0.1:5000/

## 🔄 Reiniciar la base de datos
   python reset_db.py
   flask db init
   flask db migrate -m "Reinicio"
   flask db upgrade

## ✅ Comandos rápidos
- Ejecutar app: flask run
- Crear migración: flask db migrate -m "mensaje"
- Aplicar migración: flask db upgrade
- Reiniciar DB: python reset_db.py + comandos arriba

## 🔮 Próximas mejoras
- Autenticación de usuarios (login y roles)
- Dashboard con estadísticas
- Soporte para múltiples torneos
- API REST para app móvil

## 📜 Flujo del sistema
1. Ingresar a la página principal
2. Registrar jugadores
3. Generar fase de grupos
4. Jugar partidos y registrar resultados
5. Iniciar eliminación directa
6. Finalizar torneo y mostrar ganador

## 👨‍💻 Autor
Andres Santiago Torres Viuche  
Proyecto educativo para aprender POO

## 📜 Licencia
No License
/ Copyrigth 
/ No copiar
/ No clonar 
/ No robar
/ Autoria Propia
