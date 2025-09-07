from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Jugador, Grupo, JugadorGrupo, Partido
from services.tournament_service import TournamentManager

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
manager = TournamentManager()

@admin_bp.get('/')
def dashboard():
    jugadores = Jugador.query.order_by(Jugador.estado.asc(), Jugador.nombre.asc()).all()
    grupos = Grupo.query.all()
    return render_template('admin_dashboard.html', jugadores=jugadores, grupos=grupos)

@admin_bp.post('/aceptar/<int:jugador_id>')
def aceptar(jugador_id):
    manager.aceptar_jugador(jugador_id)
    flash('Jugador aceptado', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.post('/rechazar/<int:jugador_id>')
def rechazar(jugador_id):
    manager.rechazar_jugador(jugador_id)
    flash('Jugador rechazado', 'info')
    return redirect(url_for('admin.dashboard'))

@admin_bp.post('/sortear')
def sortear():
    try:
        manager.sortear_grupos()
        flash('Sorteo realizado y calendario generado', 'success')
    except Exception as e:
        flash(str(e), 'error')
    return redirect(url_for('admin.dashboard'))

@admin_bp.post('/partido/<int:partido_id>/resultado')
def resultado_grupo(partido_id):
    marcador = request.form.get('marcador')
    ganador_id = request.form.get('ganador_id', type=int)
    p = Partido.query.get_or_404(partido_id)
    if p.fase == 'grupos':
        manager.registrar_resultado_grupo(partido_id, marcador, ganador_id)
    else:
        manager.registrar_resultado_eliminacion(partido_id, marcador, ganador_id)
    flash('Resultado registrado', 'success')
    return redirect(request.referrer or url_for('admin.dashboard'))

@admin_bp.post('/generar_eliminacion')
def generar_eliminacion():
    try:
        manager.generar_eliminacion()
        flash('Fase de eliminación generada', 'success')
    except Exception as e:
        flash(str(e), 'error')
    return redirect(url_for('admin.dashboard'))
