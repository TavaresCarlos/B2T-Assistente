from datetime import datetime, timedelta
import requests
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import settings

def converter_timestamp(timestamp):
    """
    Converte timestamp do ActivityWatch para o fuso
    America/Sao_Paulo.
    """

    if not timestamp:
        return None

    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

    # Caso o timestamp não possua timezone
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=settings.FUSO_ATUAL)

    return dt.astimezone(settings.FUSO_ATUAL)
