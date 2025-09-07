from flask import Flask
from config import Config
from models import db
from routes.public import public_bp
from routes.admin import admin_bp
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    # Inicializar base de datos y migraciones
    db.init_app(app)
    Migrate(app, db)

    # Registrar blueprints
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    # Filtro personalizado para templates (muestra nombre de jugador por id)
    @app.template_filter('jugador_nombre')
    def jugador_nombre(jid):
        from models import Jugador
        jugador = Jugador.query.get(jid)
        return jugador.nombre if jugador else 'BYE'

    return app


if __name__ == '__main__':
    app = create_app()
    # Crear tablas si no existen (solo para desarrollo rápido)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
