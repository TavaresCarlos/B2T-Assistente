import requests
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import settings

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
