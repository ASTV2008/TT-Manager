from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Constantes para estados
ESTADO_PENDIENTE = "pendiente"
ESTADO_ACEPTADO = "aceptado"
ESTADO_RECHAZADO = "rechazado"


class Administrador(db.Model):
    __tablename__ = 'administradores'

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena = db.Column(db.Text, nullable=False)  # almacenar hash, no contraseña en claro

    def __repr__(self):
        return f'<Administrador {self.usuario}>'


class Jugador(db.Model):
    __tablename__ = 'jugadores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    edad = db.Column(db.Integer)
    estado = db.Column(db.String(20), default=ESTADO_PENDIENTE, nullable=False)
    puntos = db.Column(db.Integer, default=0)
    victorias = db.Column(db.Integer, default=0)
    derrotas = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relaciones
    grupos = db.relationship(
        'JugadorGrupo',
        back_populates='jugador',
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f'<Jugador {self.nombre}>'


class Grupo(db.Model):
    __tablename__ = 'grupos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(10), nullable=False, unique=True)

    jugadores = db.relationship(
        'JugadorGrupo',
        back_populates='grupo',
        cascade="all, delete-orphan",
        lazy=True
    )

    partidos = db.relationship(
        'Partido',
        back_populates='grupo',
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f'<Grupo {self.nombre}>'


class JugadorGrupo(db.Model):
    __tablename__ = 'jugadores_grupos'

    id = db.Column(db.Integer, primary_key=True)
    jugador_id = db.Column(db.Integer, db.ForeignKey('jugadores.id', ondelete='CASCADE'), nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id', ondelete='CASCADE'), nullable=False)
    puntos = db.Column(db.Integer, default=0)
    victorias = db.Column(db.Integer, default=0)
    derrotas = db.Column(db.Integer, default=0)

    jugador = db.relationship('Jugador', back_populates='grupos')
    grupo = db.relationship('Grupo', back_populates='jugadores')

    __table_args__ = (db.UniqueConstraint('jugador_id', 'grupo_id', name='uq_jugador_grupo'),)

    def __repr__(self):
        return f'<JugadorGrupo jugador_id={self.jugador_id} grupo_id={self.grupo_id}>'


class Partido(db.Model):
    __tablename__ = 'partidos'

    id = db.Column(db.Integer, primary_key=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id', ondelete='CASCADE'), nullable=True)
    jugador1_id = db.Column(db.Integer, db.ForeignKey('jugadores.id'), nullable=False)
    jugador2_id = db.Column(db.Integer, db.ForeignKey('jugadores.id'), nullable=True)
    marcador = db.Column(db.String(20), nullable=True)  # ej: "3-1"
    ganador_id = db.Column(db.Integer, db.ForeignKey('jugadores.id'), nullable=True)
    fase = db.Column(db.String(20), default='grupos', nullable=False)  # 'grupos' o 'eliminacion'
    ronda = db.Column(db.Integer, default=0)  # para eliminación
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    grupo = db.relationship('Grupo', back_populates='partidos')
    jugador1 = db.relationship('Jugador', foreign_keys=[jugador1_id], lazy=True)
    jugador2 = db.relationship('Jugador', foreign_keys=[jugador2_id], lazy=True)
    ganador = db.relationship('Jugador', foreign_keys=[ganador_id], lazy=True)

    def __repr__(self):
        return f'<Partido {self.jugador1_id} vs {self.jugador2_id}>'
