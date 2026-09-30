from zoneinfo import ZoneInfo

BASE_URL = "http://localhost:5600/api/0"

#Bucket para registro de ativo/ inativo
AFK_BUCKET = "aw-watcher-afk_Carlos"
#Bucket para registro de qual janela está ativa
WINDOW_BUCKET = "aw-watcher-window_Carlos"

# Fuso horário de Brasília
FUSO_ATUAL = ZoneInfo("America/Sao_Paulo")

# Ignorar eventos muito pequenos, inferiores a 1s
MIN_DURACAO_SEGUNDOS = 1

# Mostrar somente os últimos X minutos
ULTIMOS_MINUTOS = 15

# Arquivo de saída
ARQUIVO_JSON = "activities.json"
