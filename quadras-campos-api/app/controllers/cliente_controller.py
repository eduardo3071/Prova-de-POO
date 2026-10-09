from app.models.cliente import carregar_clientes


class ClienteController:
    def __init__(self):
        self._clientes = carregar_clientes()

    def _para_dicionario(self, cliente):
        return {
            "id": cliente.mostrar_id(),
            "nome": cliente.mostrar_nome(),
            "telefone": cliente.mostrar_telefone(),
        }

    def listar(self):
        return [self._para_dicionario(c) for c in self._clientes]

    def listar_objetos(self):
        return list(self._clientes)

    def buscar_objeto(self, id):
        achados = [c for c in self._clientes if c.mostrar_id() == id]
        return achados[0] if achados else None

    def buscar_por_id(self, id):
        cliente = self.buscar_objeto(id)
        return self._para_dicionario(cliente) if cliente else None
