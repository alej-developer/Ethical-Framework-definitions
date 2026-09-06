"""EN: FastAPI application entrypoint with middleware and routing configuration. | ES: Punto de entrada de la aplicacion FastAPI con configuracion de middleware y enrutamiento."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.api.routes import router


def create_app() -> FastAPI:
    """EN: Application factory instantiating and configuring the FastAPI instance. | ES: Fabrica de aplicacion que instancia y configura la instancia de FastAPI."""
    app = FastAPI(
        title="AI Ethics Interactive Simulator API",
        description="Clean Architecture REST backend for evaluating AI systems against EU AI Act and IEEE standards.",
        version="0.1.0",
    )

    # EN: Configure CORS for local development with Vite frontend | ES: Configurar CORS para desarrollo local con frontend Vite
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # EN: Include API v1 router | ES: Incluir enrutador de API v1
    app.include_router(router)

    return app


app = create_app()
