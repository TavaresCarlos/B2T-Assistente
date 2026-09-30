from datetime import datetime, timedelta
import requests
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import settings

def formatar_timestamp(timestamp):

    dt = datetime.fromisoformat(
        timestamp
    )

    dt = dt.astimezone(
        settings.FUSO_ATUAL
    )

    return dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

