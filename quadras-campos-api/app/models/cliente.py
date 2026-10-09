from app.data.cliente_mock import CLIENTES


class Cliente:
    def __init__(self, id, nome, telefone):
        self._id = id
        self.alterar_nome(nome)
        self.alterar_telefone(telefone)

    def mostrar_id(self):
        return self._id

    def mostrar_nome(self):
        return self._nome

    def mostrar_telefone(self):
        return self._telefone

    def alterar_nome(self, nome):
        if not nome or len(nome.strip()) < 3:
            raise ValueError("O nome do cliente precisa ter pelo menos 3 caracteres.")
        self._nome = nome.strip()

    def alterar_telefone(self, telefone):
        digitos = "".join(c for c in str(telefone) if c.isdigit())
        if not 10 <= len(digitos) <= 11:
            raise ValueError("O telefone precisa ter 10 ou 11 dígitos.")
        self._telefone = digitos

    def __repr__(self):
        return f"Cliente(id={self._id}, nome={self._nome!r})"


def carregar_clientes():
    return [Cliente(i["id"], i["nome"], i["telefone"]) for i in CLIENTES]
