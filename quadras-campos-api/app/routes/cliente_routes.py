from fastapi import APIRouter, HTTPException
from app.routes.espaco_routes import clientes

router = APIRouter(prefix="/api", tags=["Clientes"])

@router.get("/clientes")
def listar_clientes():
    return clientes.listar()

@router.get("/clientes/{id}")
def buscar_cliente(id: int):
    cliente = clientes.buscar_por_id(id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return cliente