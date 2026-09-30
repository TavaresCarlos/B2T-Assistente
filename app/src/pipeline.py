import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from filters.cruzar_eventos import cruzar_eventos
from filters.filtrar_intervalo import filtrar_ultimos_minutos as filtrar_intervalo
from filters.agregar_intervalos import agregar_intervalos
from filters.gerar_resumo import gerar_resumo

import settings

def executar_pipeline(evento_afk, eventos_window):
    eventos_cruzados = cruzar_eventos(evento_afk, eventos_window)
    eventos_filtrados = filtrar_intervalo(eventos_cruzados)
    agregar = agregar_intervalos(eventos_filtrados)
    resumo = gerar_resumo(agregar)

    return resumo
