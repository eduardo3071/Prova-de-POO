# Divisão de tarefas

Cada tarefa mexe em arquivos diferentes para evitar conflito de merge. Ao terminar, rode `python verificar.py` (tem que passar inteiro) e faça o commit **com a sua própria conta**.

| Integrante | GitHub | Tarefa | Arquivos |
|---|---|---|---|
| Eduardo Oliveira | [@eduardo3071](https://github.com/eduardo3071) | **Hierarquia.** Adicionar uma terceira filha, `CampoSociety`, que herda de `Campo` e estende um método com `super()`. Registrar `"campo_society"` no `PERFIS` e criar um mock. | `app/models/espaco.py`, `app/data/espaco_mock.py` |
| Eduardo França | [@EduardoFranca2805](https://github.com/EduardoFranca2805) | **Regra de negócio.** Exigir antecedência mínima de 1 dia na reserva (`raise ValueError`, que a rota traduz em 422). Adicionar 2 checagens no `verificar.py`. | `app/models/reserva.py`, `verificar.py` |
| Gabriel Jesus | [@Senseei](https://github.com/Senseei) | **Controllers e mocks.** Ampliar os mocks para pelo menos 5 registros bem variados por entidade. Adicionar busca de cliente por nome no `ClienteController` (compreensão de lista). | `app/data/*_mock.py`, `app/controllers/cliente_controller.py` |
| Gabriel Pilar | [@GenezisDev](https://github.com/GenezisDev) | **Rotas e documentação.** Criar `GET /api/clientes` e `GET /api/clientes/{id}` (404 quando não existe). Revisar o README (tabela de rotas, diagrama) e colar a saída final do `verificar.py`. | `app/routes/`, `README.md` |

## Fluxo de trabalho

1. Clonar: `git clone https://github.com/eduardo3071/Prova-de-POO.git`
2. Antes de começar: `git pull`
3. Fazer a tarefa, em commits pequenos e com mensagem clara
4. Rodar `python verificar.py`
5. Enviar: `git push`

## Regras do grupo

- Nada de FastAPI dentro de `app/models/`.
- Nenhum `if` comparando tipo ou nome de classe.
- Validação fica na model (`raise ValueError`), nunca na rota.
- Na arguição, qualquer integrante pode ser chamado a explicar qualquer linha. Leiam também o código dos colegas.
