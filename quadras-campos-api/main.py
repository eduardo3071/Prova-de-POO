from fastapi import FastAPI
from app.routes import espaco_routes, reserva_routes, cliente_routes

app = FastAPI(
    title="Quadras & Campos API",
    description="Agendamento de horários para aluguel de quadras e campos.",
)

app.include_router(cliente_routes.router)
app.include_router(espaco_routes.router)
app.include_router(reserva_routes.router)
