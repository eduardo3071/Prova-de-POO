"""Verificação da API de Quadras & Campos. Rode: python verificar.py"""
import pathlib
import sys

from fastapi import HTTPException

from app.models.cliente import Cliente
from app.models.erros import ConflitoError
from app.models.espaco import PERFIS, Campo, Espaco, Quadra
from app.models.reserva import Reserva
from app.routes import espaco_routes, reserva_routes
from app.routes.reserva_routes import NovaReserva
from main import app

resultados = []


def checar(descricao, condicao):
    resultados.append(bool(condicao))
    print(f"[{'OK' if condicao else 'FALHOU'}] {descricao}")


def levanta(excecao, funcao, *args):
    try:
        funcao(*args)
    except excecao:
        return True
    return False


def status_da_rota(caminho, metodo):
    achadas = [r for r in app.routes if getattr(r, "path", "") == caminho and metodo in r.methods]
    return achadas[0].status_code if achadas else None


def codigo_http(funcao, *args):
    try:
        funcao(*args)
    except HTTPException as erro:
        return erro.status_code
    return 200


def corpo(**mudancas):
    base = dict(espaco_id=2, cliente_id=1, data="2026-12-01", hora_inicio=10, duracao=2)
    base.update(mudancas)
    return NovaReserva(**base)


quadra = Quadra(1, "Quadra Teste", True)
campo = Campo(2, "Campo Teste")
cliente = Cliente(1, "Fulano de Tal", "11999998888")

# --- Models: encapsulamento e regras
checar("Atributos são protegidos (sem acesso público a nome/id)", not hasattr(quadra, "nome") and not hasattr(quadra, "id"))
checar("Não existe alterar_id em nenhuma classe", not any(hasattr(c, "alterar_id") for c in (Espaco, Cliente, Reserva)))
checar("Construtor valida: nome curto de espaço levanta ValueError", levanta(ValueError, Quadra, 9, "ab"))
checar("Construtor valida: telefone inválido levanta ValueError", levanta(ValueError, Cliente, 9, "Fulano", "123"))
checar("Regra: data inválida levanta ValueError", levanta(ValueError, Reserva, 9, quadra, cliente, "31/12/2026", 10, 1))
checar("Regra: duração fora de 1-4h levanta ValueError", levanta(ValueError, Reserva, 9, quadra, cliente, "2026-12-01", 10, 5))
checar("Regra: fora do horário de funcionamento levanta ValueError", levanta(ValueError, Reserva, 9, quadra, cliente, "2026-12-01", 22, 2))

# --- Herança e polimorfismo
checar("Hierarquia: Quadra e Campo herdam de Espaco", issubclass(Quadra, Espaco) and issubclass(Campo, Espaco))
checar("Constante de classe PRECO_HORA difere nas filhas", Quadra.PRECO_HORA != Campo.PRECO_HORA)
checar("super() estende valor_hora (quadra coberta = base + taxa)", quadra.valor_hora() == Quadra.PRECO_HORA + Quadra.TAXA_COBERTURA)
checar("Polimorfismo: valor_hora difere entre quadra e campo", quadra.valor_hora() != campo.valor_hora())
checar("PERFIS mapeia texto do mock para classe", PERFIS["quadra"] is Quadra and PERFIS["campo"] is Campo)
checar("Valor total da reserva = valor_hora x duração", Reserva(9, campo, cliente, "2026-12-01", 10, 2).valor_total() == campo.valor_hora() * 2)
checar("Conflito de horário levanta ConflitoError", levanta(ConflitoError, Reserva(9, quadra, cliente, "2026-12-01", 10, 2).verificar_disponibilidade, [Reserva(8, quadra, cliente, "2026-12-01", 11, 2)]))

# --- Rotas e códigos HTTP
checar("GET /api/espacos devolve a lista", len(espaco_routes.listar_espacos()) >= 5)
checar("Filtro ?tipo=campo só devolve campos", {e["tipo"] for e in espaco_routes.listar_espacos("campo")} == {"campo"})
checar("GET /api/espacos/{id} inexistente -> 404", codigo_http(espaco_routes.buscar_espaco, 999) == 404)
checar("GET /api/espacos/{id}/agenda/{data} mostra horas livres", 18 not in espaco_routes.agenda_do_espaco(1, "2026-10-20")["horas_livres"])
checar("POST /api/reservas declara status 201", status_da_rota("/api/reservas", "POST") == 201)
checar("POST /api/reservas válida cria a reserva", reserva_routes.criar_reserva(corpo())["valor_total"] == 2 * Quadra.PRECO_HORA)
checar("POST /api/reservas no mesmo horário -> 409", codigo_http(reserva_routes.criar_reserva, corpo()) == 409)
checar("POST /api/reservas fora do expediente -> 422", codigo_http(reserva_routes.criar_reserva, corpo(hora_inicio=22)) == 422)
checar("POST /api/reservas com espaço inexistente -> 404", codigo_http(reserva_routes.criar_reserva, corpo(espaco_id=999)) == 404)
checar("GET /api/clientes/{id}/reservas inexistente -> 404", codigo_http(reserva_routes.reservas_do_cliente, 999) == 404)
checar("DELETE /api/reservas/{id} inexistente -> 404", codigo_http(reserva_routes.cancelar_reserva, 999) == 404)
checar("Cancelar libera o horário (recriar não dá 409)", codigo_http(reserva_routes.cancelar_reserva, 7) == 200 and codigo_http(reserva_routes.criar_reserva, corpo()) == 200)
checar("GET /api/relatorio/faturamento soma as reservas", reserva_routes.faturamento()["total"] > 0)

# --- Camadas e estilo
fontes_models = "".join(p.read_text(encoding="utf-8") for p in pathlib.Path("app/models").glob("*.py"))
todas_fontes = "".join(
    p.read_text(encoding="utf-8") for p in pathlib.Path("app").rglob("*.py")
)
checar("Nenhum import de FastAPI dentro de app/models", "fastapi" not in fontes_models)
checar("Nenhum if comparando tipo ou nome de classe no projeto", "isinstance" not in todas_fontes and "__name__ ==" not in todas_fontes and "type(" not in todas_fontes.replace("type(self).__name__", ""))
checar("Mocks não têm import nem classe", not any("import" in p.read_text(encoding="utf-8") or "class " in p.read_text(encoding="utf-8") for p in pathlib.Path("app/data").glob("*_mock.py")))

print(f"\n{sum(resultados)}/{len(resultados)} checagens passaram.")
sys.exit(0 if all(resultados) else 1)
