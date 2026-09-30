from datetime import datetime, timedelta

import requests
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import settings

def filtrar_ultimos_minutos(eventos):

    agora = datetime.now(settings.FUSO_ATUAL)

    inicio_janela = (
        agora -
        timedelta(minutes=settings.ULTIMOS_MINUTOS)
    )

    eventos_filtrados = []

    for evento in eventos:

        inicio = datetime.fromisoformat(
            evento["inicio"]
        )

        fim = datetime.fromisoformat(
            evento["fim"]
        )

        # ----------------------------------------------------
        # Verificar se o evento possui alguma interseção
        # com a janela dos últimos 15 minutos
        # ----------------------------------------------------

        if fim <= inicio_janela:
            continue

        if inicio >= agora:
            continue

        # ----------------------------------------------------
        # Cortar o início
        # ----------------------------------------------------

        if inicio < inicio_janela:
            inicio = inicio_janela

        # ----------------------------------------------------
        # Cortar o fim
        # ----------------------------------------------------

        if fim > agora:
            fim = agora

        duracao = (
            fim - inicio
        ).total_seconds()

        if duracao < settings.MIN_DURACAO_SEGUNDOS:
            continue

        novo_evento = evento.copy()

        novo_evento["inicio"] = inicio.isoformat()
        novo_evento["fim"] = fim.isoformat()
        novo_evento["duracao_segundos"] = duracao

        eventos_filtrados.append(
            novo_evento
        )

    eventos_filtrados.sort(
        key=lambda x: x["inicio"]
    )

    return eventos_filtrados
