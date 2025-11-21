from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database.db import connect_to_mongo, close_connection_to_mongo
from .routes.auth import router as auth_router
from .routes.user import router as user_router
from .routes.lab import router as lab_router
from .routes.reservation import router as reservation_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando aplicação")
    if await connect_to_mongo():
        print("✅ Conexão com MongoDB bem-sucedida!")
    else:
        print("❌ Erro ao conectar no MongoDB")
    yield
    if await close_connection_to_mongo():
        print("✅ Conexão com MongoDB fechada")


app = FastAPI(
    title="Sistema de reservas de salas e de laboratórios",
    description="API para gerenciamento de reservas de salas e laboratórios",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API do Sistema de Reservas funcionando!"}


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(lab_router)
app.include_router(reservation_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
