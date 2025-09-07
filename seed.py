from app import create_app
from models import db, Jugador
app = create_app()
nombres = [
 ("Ana", "ana@example.com"),
 ("Bruno", "bruno@example.com"),
 ("Carla", "carla@example.com"),
 ("Diego", "diego@example.com"),
 ("Elena", "elena@example.com"),
 ("Fabio", "fabio@example.com"),
 ("Gina", "gina@example.com"),
 ("Hugo", "hugo@example.com"),
 ]
with app.app_context():
    for nombre, correo in nombres:
        j = Jugador(nombre=nombre, correo=correo, edad=20,
        estado_inscripcion='aceptado')
        db.session.add(j)
        db.session.commit()
print("Seed listo")