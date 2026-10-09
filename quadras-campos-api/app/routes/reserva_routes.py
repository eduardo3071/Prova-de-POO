from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.erros import ConflitoError
from app.routes.espaco_routes import clientes, reservas

router = APIRouter(prefix="/api", tags=["Reservas"])


class NovaReserva(BaseModel):
    espaco_id: int
    cliente_id: int
    data: str
    hora_inicio: int
    duracao: int


@router.post("/reservas", status_code=201)
def criar_reserva(corpo: NovaReserva):
    try:
        reserva = reservas.criar(
            corpo.espaco_id, corpo.cliente_id, corpo.data, corpo.hora_inicio, corpo.duracao
        )
    except ConflitoError as erro:
        raise HTTPException(status_code=409, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=422, detail=str(erro))
    if reserva is None:
        raise HTTPException(status_code=404, detail="Espaço ou cliente não encontrado.")
    return reserva


@router.delete("/reservas/{id}")
def cancelar_reserva(id: int):
    reserva = reservas.cancelar(id)
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva não encontrada.")
    return {"mensagem": "Reserva cancelada.", "reserva": reserva}


@router.get("/clientes/{id}/reservas")
def reservas_do_cliente(id: int):
    if clientes.buscar_por_id(id) is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return reservas.listar_por_cliente(id)


@router.get("/relatorio/faturamento")
def faturamento():
    return reservas.faturamento()
