from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles

from app.common.sqlalchemy_ext import session_context
from app.common.starlette_cors_ext import CorrectCORSMiddleware
from app.config import POSTGRES_AUTOMIGRATE, Base, engine, sessionmaker


async def reinit_database() -> None:  # pragma: no cover
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    if POSTGRES_AUTOMIGRATE:
        await reinit_database()

    yield


app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)

app.mount("/openapi-static", StaticFiles(directory="openapi-static"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html() -> Response:
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="ScanQuest API",
        swagger_js_url="/openapi-static/swagger-ui-bundle.js",
        swagger_css_url="/openapi-static/swagger-ui.css",
    )


app.add_middleware(
    CorrectCORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def database_session_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    async with sessionmaker.begin() as session:
        session_context.set(session)
        return await call_next(request)
