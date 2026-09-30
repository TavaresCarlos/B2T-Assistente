import requests
import json

from datetime import datetime, timedelta

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import settings


# ============================================================
# BUSCAR EVENTOS DO ACTIVITYWATCH
# ============================================================

def buscar_eventos(bucket_id):
    url = f"{settings.BASE_URL}/buckets/{bucket_id}/events"

    resposta = requests.get(url, timeout=10)
    resposta.raise_for_status()

    return resposta.json()


# ============================================================
# CONVERTER TIMESTAMP PARA BRASÍLIA
# ============================================================

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


# ============================================================
# CLASSIFICAR ATIVIDADE
# ============================================================

def classificar_atividade(afk, app, titulo):

    app = str(app or "").lower()
    titulo = str(titulo or "").lower()

    texto = f"{app} {titulo}"

    # --------------------------------------------------------
    # INATIVIDADE
    # --------------------------------------------------------

    if afk == "afk":
        return "inatividade"

    # --------------------------------------------------------
    # DESENVOLVIMENTO
    # --------------------------------------------------------

    palavras_desenvolvimento = [
        "visual studio code",
        "vs code",
        "code.exe",
        "pycharm",
        "intellij",
        "eclipse",
        "android studio",
        "sublime",
        "notepad++",
        "terminal",
        "powershell",
        "cmd.exe",
        "git bash",
        "windows terminal",
        "postman",
        "docker",
        "github",
        "git",
    ]

    if any(palavra in texto for palavra in palavras_desenvolvimento):
        return "desenvolvimento"

    # --------------------------------------------------------
    # COMUNICAÇÃO
    # --------------------------------------------------------

    palavras_comunicacao = [
        "whatsapp",
        "whatsapp.root.exe",
        "teams",
        "discord",
        "slack",
        "telegram",
        "zoom",
        "skype",
    ]

    if any(palavra in texto for palavra in palavras_comunicacao):
        return "comunicação"

    # --------------------------------------------------------
    # ESCRITA
    # --------------------------------------------------------

    palavras_escrita = [
        "word",
        "winword",
        "libreoffice writer",
        "writer",
        ".docx",
        "latex",
        "overleaf",
        "notepad",
    ]

    if any(palavra in texto for palavra in palavras_escrita):
        return "escrita"

    # --------------------------------------------------------
    # APRESENTAÇÃO
    # --------------------------------------------------------

    palavras_apresentacao = [
        "powerpoint",
        "powerpnt",
        "libreoffice impress",
        "impress",
    ]

    if any(palavra in texto for palavra in palavras_apresentacao):
        return "apresentação"

    # --------------------------------------------------------
    # NAVEGAÇÃO
    # --------------------------------------------------------

    palavras_navegacao = [
        "chrome",
        "firefox",
        "firefox.exe",
        "edge",
        "ms edge",
        "brave",
        "opera",
    ]

    if any(palavra in texto for palavra in palavras_navegacao):
        return "navegação"

    # --------------------------------------------------------
    # ENTRETENIMENTO
    # --------------------------------------------------------

    palavras_entretenimento = [
        "youtube",
        "netflix",
        "spotify",
        "twitch",
    ]

    if any(palavra in texto for palavra in palavras_entretenimento):
        return "entretenimento"

    # --------------------------------------------------------
    # PADRÃO
    # --------------------------------------------------------

    return "outra"


# ============================================================
# CRUZAR EVENTOS AFK + JANELA
# ============================================================

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


# ============================================================
# FILTRAR ÚLTIMOS 15 MINUTOS
# ============================================================

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


# ============================================================
# AGREGAR INTERVALOS
# ============================================================

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


# ============================================================
# FORMATAR DURAÇÃO
# ============================================================

def formatar_duracao(segundos):

    segundos = int(round(segundos))

    horas = segundos // 3600

    minutos = (
        segundos % 3600
    ) // 60

    segundos_restantes = (
        segundos % 60
    )

    if horas > 0:

        if minutos > 0:
            return f"{horas} h {minutos} min"

        return f"{horas} h"

    if minutos > 0:

        if segundos_restantes > 0:
            return (
                f"{minutos} min "
                f"{segundos_restantes} s"
            )

        return f"{minutos} min"

    return f"{segundos_restantes} s"


# ============================================================
# FORMATAR TIMESTAMP
# ============================================================

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


# ============================================================
# IMPRIMIR EVENTO
# ============================================================

def imprimir_evento(evento):

    inicio = formatar_timestamp(
        evento["inicio"]
    )

    fim = formatar_timestamp(
        evento["fim"]
    )

    duracao = formatar_duracao(
        evento["duracao_segundos"]
    )

    print()
    print(
        f"{inicio} ─ {fim}"
    )

    print(
        f"├── AFK:       {evento['afk']}"
    )

    print(
        f"├── Janela:    {evento['app']}"
    )

    if evento["titulo"]:

        print(
            f"├── Título:    "
            f"{evento['titulo']}"
        )

    print(
        f"├── Duração:   {duracao}"
    )

    print(
        f"└── Atividade: "
        f"{evento['atividade']}"
    )


# ============================================================
# IMPRIMIR TODOS OS EVENTOS
# ============================================================

def imprimir_eventos(eventos):

    print()
    print("=" * 70)
    print(
        f"ATIVIDADES DOS ÚLTIMOS "
        f"{settings.ULTIMOS_MINUTOS} MINUTOS"
    )
    print("=" * 70)

    if not eventos:

        print(
            "Nenhuma atividade encontrada."
        )

        return

    for evento in eventos:

        imprimir_evento(evento)


# ============================================================
# RESUMO
# ============================================================

def gerar_resumo(eventos):

    resumo = {}

    for evento in eventos:

        atividade = evento[
            "atividade"
        ]

        duracao = evento[
            "duracao_segundos"
        ]

        resumo[atividade] = (
            resumo.get(
                atividade,
                0
            )
            + duracao
        )

    print()
    print("=" * 70)
    print("RESUMO")
    print("=" * 70)

    if not resumo:

        print(
            "Nenhuma atividade encontrada."
        )

        return

    for atividade, segundos in sorted(
        resumo.items(),
        key=lambda x: x[1],
        reverse=True
    ):

        print(
            f"{atividade:20} "
            f"{formatar_duracao(segundos)}"
        )


# ============================================================
# SALVAR JSON
# ============================================================

def salvar_json(eventos):

    dados = {
        "gerado_em": datetime.now(
            settings.FUSO_ATUAL
        ).isoformat(),

        "fuso_horario": (
            "America/Sao_Paulo"
        ),

        "periodo_minutos": (
            settings.ULTIMOS_MINUTOS
        ),

        "quantidade_eventos": (
            len(eventos)
        ),

        "eventos": eventos
    }

    with open(
        settings.ARQUIVO_JSON,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    print()
    print(
        f"Dados salvos em: "
        f"{settings.ARQUIVO_JSON}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("ACTIVITYWATCH - MONITORAMENTO")
    print("=" * 70)

    agora = datetime.now(
        settings.FUSO_ATUAL
    )

    inicio = (
        agora -
        timedelta(
            minutes=settings.ULTIMOS_MINUTOS
        )
    )

    print(
        f"Agora:       "
        f"{agora.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    print(
        f"Início:      "
        f"{inicio.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    print(
        f"Fuso:        "
        f"{settings.FUSO_ATUAL}"
    )

    print(
        f"Período:     "
        f"últimos {settings.ULTIMOS_MINUTOS} minutos"
    )

    try:

        # ----------------------------------------------------
        # Buscar AFK
        # ----------------------------------------------------

        print()
        print("Buscando eventos AFK...")

        afk_events = buscar_eventos(
            settings.AFK_BUCKET
        )

        print(
            f"Eventos AFK encontrados: "
            f"{len(afk_events)}"
        )

        # ----------------------------------------------------
        # Buscar janelas
        # ----------------------------------------------------

        print()
        print("Buscando eventos de janela...")

        window_events = buscar_eventos(
            settings.WINDOW_BUCKET
        )

        print(
            f"Eventos de janela encontrados: "
            f"{len(window_events)}"
        )

        # ----------------------------------------------------
        # Cruzar eventos
        # ----------------------------------------------------

        print()
        print("Cruzando eventos...")

        eventos = cruzar_eventos(
            afk_events,
            window_events
        )

        print(
            f"Eventos após cruzamento: "
            f"{len(eventos)}"
        )

        # ----------------------------------------------------
        # Filtrar últimos 15 minutos
        # ----------------------------------------------------

        eventos = filtrar_ultimos_minutos(
            eventos
        )

        print(
            f"Eventos nos últimos "
            f"{settings.ULTIMOS_MINUTOS} minutos: "
            f"{len(eventos)}"
        )

        # ----------------------------------------------------
        # Agregar intervalos
        # ----------------------------------------------------

        eventos = agregar_intervalos(
            eventos
        )

        print(
            f"Eventos após agregação: "
            f"{len(eventos)}"
        )

        # ----------------------------------------------------
        # Mostrar
        # ----------------------------------------------------

        imprimir_eventos(
            eventos
        )

        # ----------------------------------------------------
        # Resumo
        # ----------------------------------------------------

        gerar_resumo(
            eventos
        )

        # ----------------------------------------------------
        # Salvar
        # ----------------------------------------------------

        salvar_json(
            eventos
        )

    except requests.exceptions.ConnectionError:

        print()
        print(
            "ERRO: não foi possível conectar "
            "ao ActivityWatch."
        )

        print(
            "Verifique se o ActivityWatch "
            "está executando."
        )

    except requests.exceptions.HTTPError as erro:

        print()
        print(
            "ERRO HTTP:"
        )

        print(erro)

    except Exception as erro:

        print()
        print(
            "ERRO:"
        )

        print(
            type(erro).__name__,
            erro
        )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    main()