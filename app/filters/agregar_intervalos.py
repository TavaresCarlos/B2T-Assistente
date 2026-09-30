from datetime import datetime, timedelta

import requests
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import settings

def agregar_intervalos(eventos):

    if not eventos:
        return []

    resultado = []

    evento_atual = eventos[0].copy()

    for proximo in eventos[1:]:

        inicio_atual = datetime.fromisoformat(
            evento_atual["inicio"]
        )

        fim_atual = datetime.fromisoformat(
            evento_atual["fim"]
        )

        inicio_proximo = datetime.fromisoformat(
            proximo["inicio"]
        )

        # ----------------------------------------------------
        # Verificar se podem ser unidos
        # ----------------------------------------------------

        mesmo_app = (
            evento_atual["app"]
            == proximo["app"]
        )

        mesma_atividade = (
            evento_atual["atividade"]
            == proximo["atividade"]
        )

        mesmo_afk = (
            evento_atual["afk"]
            == proximo["afk"]
        )

        intervalo = (
            inicio_proximo - fim_atual
        ).total_seconds()

        # Permite pequena diferença de até 1 segundo
        if (
            mesmo_app
            and mesma_atividade
            and mesmo_afk
            and intervalo <= 1
        ):

            evento_atual["fim"] = proximo["fim"]

            evento_atual["duracao_segundos"] = (
                datetime.fromisoformat(
                    evento_atual["fim"]
                )
                - inicio_atual
            ).total_seconds()

        else:

            resultado.append(
                evento_atual
            )

            evento_atual = proximo.copy()

    resultado.append(
        evento_atual
    )

    return resultado
