from filters.classificar_atividade import classificar_atividade
from filters.converter_timestamp import converter_timestamp

import requests
from datetime import datetime, timedelta

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import settings

def cruzar_eventos(afk_events, window_events):

    resultado = []

    for afk_event in afk_events:

        afk_inicio = converter_timestamp(
            afk_event["timestamp"]
        )

        afk_duracao = float(
            afk_event.get("duration", 0)
        )

        afk_fim = (
            afk_inicio +
            timedelta(seconds=afk_duracao)
        )

        afk_status = afk_event.get(
            "data", {}
        ).get(
            "status",
            "unknown"
        )

        for window_event in window_events:

            window_inicio = converter_timestamp(
                window_event["timestamp"]
            )

            window_duracao = float(
                window_event.get("duration", 0)
            )

            window_fim = (
                window_inicio +
                timedelta(seconds=window_duracao)
            )

            # ------------------------------------------------
            # INTERSEÇÃO TEMPORAL
            # ------------------------------------------------

            inicio = max(
                afk_inicio,
                window_inicio
            )

            fim = min(
                afk_fim,
                window_fim
            )

            # Não existe interseção
            if inicio >= fim:
                continue

            duracao = (
                fim - inicio
            ).total_seconds()

            if duracao < settings.MIN_DURACAO_SEGUNDOS:
                continue

            dados_window = window_event.get(
                "data",
                {}
            )

            app = dados_window.get(
                "app",
                ""
            )

            titulo = dados_window.get(
                "title",
                ""
            )

            atividade = classificar_atividade(
                afk_status,
                app,
                titulo
            )

            resultado.append({
                "inicio": inicio.isoformat(),
                "fim": fim.isoformat(),
                "duracao_segundos": duracao,
                "afk": afk_status,
                "status": afk_status,
                "app": app,
                "titulo": titulo,
                "atividade": atividade
            })

    resultado.sort(
        key=lambda x: x["inicio"]
    )

    return resultado
