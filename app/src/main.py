import requests
from datetime import datetime, timedelta
from activitywatch import buscar_eventos

from pipeline import executar_pipeline

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import settings

if __name__ == "__main__":
    agora = datetime.now(settings.FUSO_ATUAL)
    inicio = (agora - timedelta(minutes=settings.ULTIMOS_MINUTOS))
    
    try:
        evento_afk = buscar_eventos(settings.AFK_BUCKET)
        eventos_window = buscar_eventos(settings.WINDOW_BUCKET)

        resumo = executar_pipeline(evento_afk, eventos_window)
        print(resumo)
    except requests.exceptions.ConnectionError:
        print("ERRO: não foi possível conectar ao ActivityWatch.")
        print("Verifique se o ActivityWatch está executando.")

    except requests.exceptions.HTTPError as erro:
        print("ERRO HTTP:")
        print(erro)

    except Exception as erro:
        print(f"ERRO: {type(erro).__name__}, {erro}")
        