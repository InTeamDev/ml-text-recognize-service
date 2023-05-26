from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .containers import configure
from .settings import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f'{settings.BASE_URL}/openapi.json',
        docs_url=f'{settings.BASE_URL}/docs',
        redoc_url=f'{settings.BASE_URL}/redoc',
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.container = configure()
    app.container.wire(packages=['backend'])

    return app
