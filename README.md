# B2T-Assistente

Assistente para monitorar e resumir atividades do usuário a partir dos eventos do ActivityWatch.

O projeto busca os buckets de AFK e de janela ativa, cruza os dados temporais, filtra o intervalo desejado, agrega eventos consecutivos e gera um resumo textual com aplicativo, categoria, título da janela e tempo total gasto.

## Visão geral

O fluxo principal está em:

- [app/src/main.py](app/src/main.py): ponto de entrada do programa
- [app/src/pipeline.py](app/src/pipeline.py): orquestra a execução do processamento
- [app/settings.py](app/settings.py): configurações globais do projeto
- [app/filters](app/filters): módulos de processamento e classificação dos eventos

## Como funciona

1. Consulta os eventos do bucket de AFK do ActivityWatch.
2. Consulta os eventos do bucket da janela ativa do navegador/desktop.
3. Cruza os intervalos temporais entre os dois tipos de evento.
4. Filtra apenas os últimos minutos configurados.
5. Junta intervalos consecutivos do mesmo app, categoria e status.
6. Gera um resumo final em texto.

## Funcionalidades

- Leitura de eventos via API REST do ActivityWatch
- Interseção temporal entre eventos de AFK e de janela ativa
- Filtro por janela de tempo recente
- Agrupamento de atividades por app/título/categoria
- Classificação automática de atividade, como:
  - desenvolvimento
  - comunicação
  - escrita
  - apresentação
  - navegação
  - entretenimento
  - inatividade
  - outra
- Saída formatada em texto para leitura rápida

## Requisitos

- Python 3.10+
- ActivityWatch em execução local
- Biblioteca Python: `requests`

## Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/B2T-Assistente.git
cd B2T-Assistente
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install requests
```

## Configuração

A configuração principal fica em [app/settings.py](app/settings.py):

- `BASE_URL`: URL da API do ActivityWatch
- `AFK_BUCKET`: bucket do status de inatividade
- `WINDOW_BUCKET`: bucket da janela ativa
- `FUSO_ATUAL`: timezone utilizado
- `ULTIMOS_MINUTOS`: janela de tempo considerada
- `MIN_DURACAO_SEGUNDOS`: duração mínima para ignorar eventos muito curtos

Exemplo de configuração padrão:

```python
BASE_URL = "http://localhost:5600/api/0"
AFK_BUCKET = "aw-watcher-afk_Carlos"
WINDOW_BUCKET = "aw-watcher-window_Carlos"
FUSO_ATUAL = ZoneInfo("America/Sao_Paulo")
ULTIMOS_MINUTOS = 15
```

> Ajuste os nomes dos buckets para os nomes reais configurados no seu ActivityWatch.

## Execução

Certifique-se de que o ActivityWatch está rodando antes de iniciar o programa:

```bash
python app/src/main.py
```

A saída será algo como:

```text
====================================================================
RESUMO
====================================================================
- nome_aplicativo: code.exe
- categoria: desenvolvimento
- titulo_janela: README.md
- timestamp_inicio: 2026-09-30T09:10:00-03:00
- timestamp_fim: 2026-09-30T09:12:15-03:00
- tempo_total: 2 min 15 s
```

## Estrutura do projeto

```text
B2T-Assistente/
├── app/
│   ├── filters/
│   │   ├── agregar_intervalos.py
│   │   ├── classificar_atividade.py
│   │   ├── converter_timestamp.py
│   │   ├── cruzar_eventos.py
│   │   ├── filtrar_intervalo.py
│   │   ├── formatar_duracao.py
│   │   ├── formatar_timestamp.py
│   │   ├── gerar_resumo.py
│   │   └── __init__.py
│   ├── src/
│   │   ├── activitywatch.py
│   │   ├── main.py
│   │   ├── pipeline.py
│   │   └── backup_get_activitywatch.py
│   ├── __init__.py
│   └── settings.py
├── README.md
├── tabela.txt
└── .git/
```

## Observações

- Este projeto foi pensado para uso local e pessoal, com foco em produtividade e acompanhamento de tempo de atividade.
- O resumo final depende da qualidade dos dados capturados pelo ActivityWatch e da classificação de apps/janelas.
- Se os nomes dos buckets ou do timezone não coincidirem com o seu ambiente, ajuste as configurações antes de rodar.

## Licença

Este projeto não possui licença definida no repositório até o momento.

## Autor

Projeto em desenvolvimento para auxiliar na organização e no acompanhamento de tempo de atividade por aplicativo e categoria.
