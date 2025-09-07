from typing import List
from math import ceil
from random import shuffle
from models import db, Jugador, Grupo, JugadorGrupo, Partido, ESTADO_ACEPTADO, ESTADO_PENDIENTE, ESTADO_RECHAZADO


class TournamentManager:
    def __init__(self, nombre_torneo: str = "TTournament"):
        self.nombre = nombre_torneo

    # Inscripciones
    def aceptar_jugador(self, jugador_id: int):
        jugador = Jugador.query.get_or_404(jugador_id)
        jugador.estado = ESTADO_ACEPTADO
        db.session.commit()
        return jugador

    def rechazar_jugador(self, jugador_id: int):
        jugador = Jugador.query.get_or_404(jugador_id)
        jugador.estado = ESTADO_RECHAZADO
        db.session.commit()
        return jugador

    # Sorteo en grupos (3–4 por grupo)
    def sortear_grupos(self, prefijo: str = "G"):
        aceptados: List[Jugador] = Jugador.query.filter_by(estado=ESTADO_ACEPTADO).all()

        if len(aceptados) < 3:
            raise ValueError("Se requieren al menos 3 jugadores aceptados para crear grupos")

        shuffle(aceptados)

        n = len(aceptados)
        grupos_4 = n % 3
        if grupos_4 * 4 + ceil((n - grupos_4 * 4) / 3) * 3 < n:
            grupos_4 = (grupos_4 + 1) % 3

        grupos: List[Grupo] = []
        idx = 0

        # Crear grupos de 4
        for i in range(grupos_4):
            g = Grupo(nombre=f"{prefijo}{i + 1}")
            db.session.add(g)
            grupos.append(g)
            # asociar 4 jugadores
            for _ in range(4):
                j = aceptados[idx]
                idx += 1
                db.session.add(JugadorGrupo(jugador=j, grupo=g))

        # Crear grupos de 3 para el resto
        gcount = len(grupos)
        while idx < n:
            g = Grupo(nombre=f"{prefijo}{gcount + 1}")
            db.session.add(g)
            grupos.append(g)
            for _ in range(min(3, n - idx)):
                j = aceptados[idx]
                idx += 1
                db.session.add(JugadorGrupo(jugador=j, grupo=g))
            gcount += 1

        # Commit para persistir grupos y relaciones y asignar ids
        db.session.commit()

        # Generar calendario round-robin por grupo
        for g in grupos:
            self._generar_partidos_grupo(g.id)

        return grupos

    def _generar_partidos_grupo(self, grupo_id: int):
        jugadores_grupo = JugadorGrupo.query.filter_by(grupo_id=grupo_id).all()
        ids = [jg.jugador_id for jg in jugadores_grupo]

        nuevos_partidos = []
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                nuevos_partidos.append(
                    Partido(
                        grupo_id=grupo_id,
                        jugador1_id=ids[i],
                        jugador2_id=ids[j],
                        fase='grupos'
                    )
                )
        db.session.add_all(nuevos_partidos)
        db.session.commit()

    # Registro de resultados y actualizacion de tabla (usando Jugador.puntos, victorias, derrotas)
    def registrar_resultado_grupo(self, partido_id: int, marcador: str, ganador_id: int):
        p = Partido.query.get_or_404(partido_id)
        if p.fase != 'grupos':
            raise ValueError("El partido no pertenece a fase de grupos")

        p.marcador = marcador
        p.ganador_id = ganador_id

        # Actualizar estadísticas en Jugador
        jugador1 = Jugador.query.get(p.jugador1_id)
        jugador2 = Jugador.query.get(p.jugador2_id)

        # inicializar si None
        for jugador in (jugador1, jugador2):
            if jugador.puntos is None:
                jugador.puntos = 0
            if jugador.victorias is None:
                jugador.victorias = 0
            if jugador.derrotas is None:
                jugador.derrotas = 0

        if ganador_id == jugador1.id:
            jugador1.victorias += 1
            jugador1.puntos += 2
            jugador2.derrotas += 1
            jugador2.puntos += 1
        else:
            jugador2.victorias += 1
            jugador2.puntos += 2
            jugador1.derrotas += 1
            jugador1.puntos += 1

        db.session.commit()
        return p

    def clasificados_por_grupo(self, grupo_id: int):
        jgs = JugadorGrupo.query.filter_by(grupo_id=grupo_id).all()
        jugadores = [Jugador.query.get(jg.jugador_id) for jg in jgs]
        jugadores.sort(key=lambda j: (j.puntos or 0, j.victorias or 0), reverse=True)
        return jugadores[:2] if len(jugadores) >= 2 else []

    # Generar fase eliminatoria
    def generar_eliminacion(self):
        grupos = Grupo.query.all()
        clasificados: List[Jugador] = []
        for g in grupos:
            top2 = self.clasificados_por_grupo(g.id)
            clasificados.extend(top2)

        ids = [j.id for j in clasificados]
        if not ids:
            raise ValueError("No hay jugadores clasificados para eliminación")

        shuffle(ids)

        m = 1
        while m < len(ids):
            m *= 2
        byes = m - len(ids)

        nuevos_partidos = []
        # agregar byes (auto-avance)
        for _ in range(byes):
            j = ids.pop()
            nuevos_partidos.append(
                Partido(fase='eliminacion', ronda=1, jugador1_id=j, jugador2_id=None, ganador_id=j)
            )

        # emparejar resto
        for i in range(0, len(ids), 2):
            j1 = ids[i]
            j2 = ids[i + 1] if i + 1 < len(ids) else None
            nuevos_partidos.append(
                Partido(fase='eliminacion', ronda=1, jugador1_id=j1, jugador2_id=j2)
            )

        db.session.add_all(nuevos_partidos)
        db.session.commit()

    def registrar_resultado_eliminacion(self, partido_id: int, marcador: str, ganador_id: int):
        p = Partido.query.get_or_404(partido_id)
        if p.fase != 'eliminacion':
            raise ValueError("El partido no pertenece a eliminación")

        p.marcador = marcador
        p.ganador_id = ganador_id
        db.session.commit()

        # si todos los partidos de la ronda tienen ganador, generar siguiente ronda
        self._progresar_llave(p.ronda)
        return p

    def _progresar_llave(self, ronda: int):
        partidos = Partido.query.filter_by(fase='eliminacion', ronda=ronda).all()
        if not partidos:
            return

        # si alguno no tiene ganador (ganador_id), no avanzar
        if any(p.ganador_id is None for p in partidos):
            return

        ganadores = [p.ganador_id for p in partidos]
        if len(ganadores) == 1:
            return  # campeón

        nr = ronda + 1
        nuevos = []
        for i in range(0, len(ganadores), 2):
            j1 = ganadores[i]
            j2 = ganadores[i + 1] if i + 1 < len(ganadores) else None
            nuevos.append(Partido(fase='eliminacion', ronda=nr, jugador1_id=j1, jugador2_id=j2))

        db.session.add_all(nuevos)
        db.session.commit()