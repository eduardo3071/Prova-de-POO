"""Divide o projeto quadras-campos-api em 4 partes (uma por integrante).

Gerar as partes:   python dividir_partes.py
Aplicar uma parte: python dividir_partes.py aplicar partes/parte1_eduardo_oliveira.txt

Cada parte vira um .txt em ./partes, com todos os arquivos separados por um cabecalho
"### caminho/do/arquivo". Quem recebe a parte cola o texto num arquivo e roda o modo
"aplicar" dentro da pasta do projeto, ou cria os arquivos na mao.
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).parent / "quadras-campos-api"
SAIDA = pathlib.Path(__file__).parent / "partes"
MARCA = "### "

PARTES = {
    "parte1_eduardo_oliveira": [
        "requirements.txt",
        ".gitignore",
        "app/__init__.py",
        "app/data/__init__.py",
        "app/data/espaco_mock.py",
        "app/data/cliente_mock.py",
        "app/data/reserva_mock.py",
        "app/models/__init__.py",
        "app/models/erros.py",
        "app/models/espaco.py",
    ],
    "parte2_eduardo_franca": [
        "app/models/cliente.py",
        "app/models/reserva.py",
    ],
    "parte3_gabriel_jesus": [
        "app/controllers/__init__.py",
        "app/controllers/espaco_controller.py",
        "app/controllers/cliente_controller.py",
        "app/controllers/reserva_controller.py",
    ],
    "parte4_gabriel_pilar": [
        "app/routes/__init__.py",
        "app/routes/espaco_routes.py",
        "app/routes/reserva_routes.py",
        "main.py",
        "verificar.py",
        "README.md",
        "DIVISAO-DE-TAREFAS.md",
    ],
}


def gerar():
    SAIDA.mkdir(exist_ok=True)
    cobertos = {c for lista in PARTES.values() for c in lista}
    todos = {
        p.relative_to(RAIZ).as_posix()
        for p in RAIZ.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    }
    esquecidos = sorted(todos - cobertos)
    if esquecidos:
        print("Aviso: arquivos fora de qualquer parte:", esquecidos)
    for nome, arquivos in PARTES.items():
        blocos = []
        for caminho in arquivos:
            conteudo = (RAIZ / caminho).read_text(encoding="utf-8")
            blocos.append(f"{MARCA}{caminho}\n{conteudo}")
        (SAIDA / f"{nome}.txt").write_text("\n".join(blocos), encoding="utf-8")
        print(f"{nome}.txt  ({len(arquivos)} arquivos)")


def aplicar(caminho_txt):
    atual, linhas = None, []

    def salvar():
        if atual is None:
            return
        destino = pathlib.Path(atual)
        destino.parent.mkdir(parents=True, exist_ok=True)
        texto = "\n".join(linhas).rstrip("\n") + "\n"
        destino.write_text(texto, encoding="utf-8")
        print("criado:", atual)

    for linha in pathlib.Path(caminho_txt).read_text(encoding="utf-8").splitlines():
        if linha.startswith(MARCA):
            salvar()
            atual, linhas = linha[len(MARCA):].strip(), []
        else:
            linhas.append(linha)
    salvar()


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "aplicar":
        aplicar(sys.argv[2])
    else:
        gerar()
