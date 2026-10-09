from typing import Optional

from fastapi import APIRouter, HTTPException

from app.controllers.cliente_controller import ClienteController
from app.controllers.espaco_controller import EspacoController
from app.controllers.reserva_controller import ReservaController

espacos = EspacoController()
clientes = ClienteController()
reservas = ReservaController(espacos, clientes)

router = APIRouter(prefix="/api", tags=["Espaços"])


@router.get("/espacos")
def listar_espacos(tipo: Optional[str] = None):
    """Lista quadras e campos. Filtro opcional: ?tipo=quadra ou ?tipo=campo."""
    return espacos.listar(tipo)


@router.get("/espacos/{id}")
def buscar_espaco(id: int):
    espaco = espacos.buscar_por_id(id)
    if espaco is None:
        raise HTTPException(status_code=404, detail="Espaço não encontrado.")
    return espaco


@router.get("/espacos/{id}/agenda/{data}")
def agenda_do_espaco(id: int, data: str):
    """Reservas do dia e horários livres (data no formato AAAA-MM-DD)."""
    agenda = reservas.agenda(id, data)
    if agenda is None:
        raise HTTPException(status_code=404, detail="Espaço não encontrado.")
    return agenda
