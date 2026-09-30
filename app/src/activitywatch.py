import requests
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import settings

def buscar_eventos(bucket_id):
    url = f"{settings.BASE_URL}/buckets/{bucket_id}/events"

    resposta = requests.get(url, timeout=10)
    resposta.raise_for_status()

    return resposta.json()
