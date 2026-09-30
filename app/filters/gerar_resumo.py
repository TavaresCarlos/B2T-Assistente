from filters.formatar_duracao import formatar_duracao

def gerar_resumo(eventos):

    resumo = {}

    for evento in eventos:

        atividade = evento.get("atividade") or "sem categoria"
        app = evento.get("app") or "aplicativo desconhecido"
        titulo = evento.get("titulo") or "sem título"
        chave = (app, atividade, titulo)
        detalhes = resumo.setdefault(
            chave,
            {
                "inicio": evento.get("inicio", ""),
                "fim": evento.get("fim", ""),
                "duracao_segundos": 0,
            },
        )
        detalhes["duracao_segundos"] += evento.get(
            "duracao_segundos", 0
        )

        inicio = evento.get("inicio", "")
        fim = evento.get("fim", "")
        if inicio and (not detalhes["inicio"] or inicio < detalhes["inicio"]):
            detalhes["inicio"] = inicio
        if fim and fim > detalhes["fim"]:
            detalhes["fim"] = fim

    linhas = ["", "=" * 70, "RESUMO", "=" * 70]

    if not resumo:

        linhas.append("Nenhuma atividade encontrada.")
        return "\n".join(linhas)

    for (app, atividade, titulo), detalhes in sorted(
        resumo.items(),
        key=lambda item: item[1]["duracao_segundos"],
        reverse=True
    ):

        linhas.append(
            f"- nome_aplicativo: {app}"
        )
        linhas.append(f"- categoria: {atividade}")
        linhas.append(f"- titulo_janela: {titulo}")
        linhas.append(f"- timestamp_inicio: {detalhes['inicio']}")
        linhas.append(f"- timestamp_fim: {detalhes['fim']}")
        linhas.append(
            f"- tempo_total: {formatar_duracao(detalhes['duracao_segundos'])}"
        )
        linhas.append("")

    return "\n".join(linhas)
