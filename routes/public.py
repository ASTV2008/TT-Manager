from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from models import db, Jugador, Grupo, JugadorGrupo, Partido
import re

public_bp = Blueprint('public', __name__)

# Página principal
@public_bp.get('/')
def index():
    grupos = Grupo.query.all()
    return render_template('index.html', grupos=grupos)

# Formulario de registro
@public_bp.get('/registrar')
def registrar_form():
    return render_template('register.html')

# Procesar registro
@public_bp.post('/registrar')
def registrar_post():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    edad = request.form.get('edad')

    # Validaciones básicas
    if not nombre or not correo:
        flash('Nombre y correo son obligatorios', 'error')
        return redirect(url_for('public.registrar_form'))

    # Validar formato de correo
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
        flash('Correo inválido', 'error')
        return redirect(url_for('public.registrar_form'))

    # Validar edad
    try:
        edad = int(edad) if edad else None
        if edad is not None and (edad < 8 or edad > 100):
            flash('Edad fuera de rango permitido (8-100)', 'error')
            return redirect(url_for('public.registrar_form'))
    except ValueError:
        flash('Edad inválida', 'error')
        return redirect(url_for('public.registrar_form'))

    # Intentar guardar en la base de datos
    try:
        jugador = Jugador(nombre=nombre, correo=correo, edad=edad)
        db.session.add(jugador)
        db.session.commit()
        flash('Solicitud enviada. Espera la aprobación del administrador.', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Este correo ya está registrado. Intenta con otro.', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al registrar: {str(e)}', 'error')

    return redirect(url_for('public.index'))

# Ver grupo específico
@public_bp.get('/grupos/<int:grupo_id>')
def ver_grupo(grupo_id):
    grupo = Grupo.query.get_or_404(grupo_id)
    tabla = (
        JugadorGrupo.query
        .filter_by(grupo_id=grupo_id)
        .order_by(JugadorGrupo.puntos.desc(), JugadorGrupo.victorias.desc())
        .all()
    )
    partidos = Partido.query.filter_by(grupo_id=grupo_id).all()
    return render_template('groups.html', grupo=grupo, tabla=tabla, partidos=partidos)

# Vista de eliminación
@public_bp.get('/eliminacion')
def ver_eliminacion():
    rondas = {}
    partidos = (
        Partido.query
        .filter_by(fase='eliminacion')
        .order_by(Partido.ronda.asc())
        .all()
    )
    for p in partidos:
        rondas.setdefault(p.ronda, []).append(p)

    return render_template('elimination.html', rondas=rondas)
