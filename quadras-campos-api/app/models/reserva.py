from datetime import date

from app.data.reserva_mock import RESERVAS
from app.models.erros import ConflitoError


class Reserva:
    ABERTURA = 8
    FECHAMENTO = 23
    DURACAO_MAXIMA = 4

    def __init__(self, id, espaco, cliente, data, hora_inicio, duracao):
        if espaco is None or cliente is None:
            raise ValueError("Uma reserva precisa de um espaço e de um cliente.")
        self._id = id
        self._espaco = espaco
        self._cliente = cliente
        self.alterar_data(data)
        self.alterar_horario(hora_inicio, duracao)

    def mostrar_id(self):
        return self._id

    def mostrar_espaco(self):
        return self._espaco

    def mostrar_cliente(self):
        return self._cliente

    def mostrar_data(self):
        return self._data.isoformat()

    def mostrar_hora_inicio(self):
        return self._hora_inicio

    def mostrar_duracao(self):
        return self._duracao

    def alterar_data(self, data):
        try:
            self._data = date.fromisoformat(str(data))
        except ValueError:
            raise ValueError("Data inválida. Use o formato AAAA-MM-DD.")

    def alterar_horario(self, hora_inicio, duracao):
        if not 1 <= duracao <= self.DURACAO_MAXIMA:
            raise ValueError(f"A duração precisa ser de 1 a {self.DURACAO_MAXIMA} horas.")
        if hora_inicio < self.ABERTURA or hora_inicio + duracao > self.FECHAMENTO:
            raise ValueError(
                f"Funcionamos das {self.ABERTURA}h às {self.FECHAMENTO}h; "
                "a reserva precisa terminar até o fechamento."
            )
        self._hora_inicio = hora_inicio
        self._duracao = duracao

    def horas_ocupadas(self):
        return list(range(self._hora_inicio, self._hora_inicio + self._duracao))

    def valor_total(self):
        return self._espaco.valor_hora() * self._duracao

    def conflita_com(self, outra):
        mesmo_lugar = self._espaco.mostrar_id() == outra.mostrar_espaco().mostrar_id()
        mesmo_dia = self.mostrar_data() == outra.mostrar_data()
        sobrepoe = bool(set(self.horas_ocupadas()) & set(outra.horas_ocupadas()))
        return mesmo_lugar and mesmo_dia and sobrepoe

    def verificar_disponibilidade(self, existentes):
        conflitos = [r for r in existentes if r.conflita_com(self)]
        if conflitos:
            raise ConflitoError(
                f"{self._espaco.mostrar_nome()} já está reservado nesse horário."
            )

    def __repr__(self):
        return (
            f"Reserva(id={self._id}, espaco={self._espaco.mostrar_id()}, "
            f"cliente={self._cliente.mostrar_id()}, data={self.mostrar_data()}, "
            f"{self._hora_inicio}h por {self._duracao}h)"
        )


def carregar_reservas(espacos, clientes):
    por_espaco = {e.mostrar_id(): e for e in espacos}
    por_cliente = {c.mostrar_id(): c for c in clientes}
    return [
        Reserva(
            i["id"],
            por_espaco[i["espaco_id"]],
            por_cliente[i["cliente_id"]],
            i["data"],
            i["hora_inicio"],
            i["duracao"],
        )
        for i in RESERVAS
    ]
