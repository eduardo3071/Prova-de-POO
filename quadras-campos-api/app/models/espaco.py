from app.data.espaco_mock import ESPACOS


class Espaco:
    TIPO = "espaco"
    PRECO_HORA = 0
    SUPERFICIE = "indefinida"
    JOGADORES = 0

    def __init__(self, id, nome, coberta=False):
        self._id = id
        self.alterar_nome(nome)
        self.alterar_coberta(coberta)

    def mostrar_id(self):
        return self._id

    def mostrar_nome(self):
        return self._nome

    def mostrar_tipo(self):
        return self.TIPO

    def mostrar_coberta(self):
        return self._coberta

    def alterar_nome(self, nome):
        if not nome or len(nome.strip()) < 3:
            raise ValueError("O nome do espaço precisa ter pelo menos 3 caracteres.")
        self._nome = nome.strip()

    def alterar_coberta(self, coberta):
        self._coberta = bool(coberta)

    def valor_hora(self):
        return self.PRECO_HORA

    def descricao(self):
        return f"{self._nome} - {self.SUPERFICIE}, {self.JOGADORES} jogadores"

    def __repr__(self):
        return f"{type(self).__name__}(id={self._id}, nome={self._nome!r})"


class Quadra(Espaco):
    TIPO = "quadra"
    PRECO_HORA = 80
    SUPERFICIE = "piso de quadra"
    JOGADORES = 10
    TAXA_COBERTURA = 20

    def valor_hora(self):
        return super().valor_hora() + int(self._coberta) * self.TAXA_COBERTURA

    def descricao(self):
        return super().descricao() + " (quadra)"


class Campo(Espaco):
    TIPO = "campo"
    PRECO_HORA = 150
    SUPERFICIE = "grama"
    JOGADORES = 14
    TAXA_ILUMINACAO = 30

    def valor_hora(self):
        return super().valor_hora() + self.TAXA_ILUMINACAO

    def descricao(self):
        return super().descricao() + " (campo, com iluminação)"


PERFIS = {
    "quadra": Quadra,
    "campo": Campo,
}


def carregar_espacos():
    return [
        PERFIS[item["tipo"]](item["id"], item["nome"], item["coberta"])
        for item in ESPACOS
    ]
