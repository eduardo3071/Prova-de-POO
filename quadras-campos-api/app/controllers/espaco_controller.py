from app.models.espaco import carregar_espacos


class EspacoController:
    def __init__(self):
        self._espacos = carregar_espacos()

    def _para_dicionario(self, espaco):
        return {
            "id": espaco.mostrar_id(),
            "nome": espaco.mostrar_nome(),
            "tipo": espaco.mostrar_tipo(),
            "coberta": espaco.mostrar_coberta(),
            "descricao": espaco.descricao(),
            "valor_hora": espaco.valor_hora(),
        }

    def listar(self, tipo=None):
        return [
            self._para_dicionario(e)
            for e in self._espacos
            if tipo is None or e.mostrar_tipo() == tipo.lower()
        ]

    def listar_objetos(self):
        return list(self._espacos)

    def buscar_objeto(self, id):
        achados = [e for e in self._espacos if e.mostrar_id() == id]
        return achados[0] if achados else None

    def buscar_por_id(self, id):
        espaco = self.buscar_objeto(id)
        return self._para_dicionario(espaco) if espaco else None
