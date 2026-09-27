"""
BOVIMED FastAPI application entrypoint.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api import api_router
from app.config import get_settings
from app.database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bovimed")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    settings = get_settings()
    init_db()
    logger.info(
        "BOVIMED API started | demo_mode=%s | model_path=%s | model_exists=%s",
        settings.should_use_demo_mode(),
        settings.resolved_model_path,
        settings.resolved_model_path.exists(),
    )
    yield


app = FastAPI(
    title="BOVIMED API",
    description=(
        "AI-powered dairy health & early mastitis detection platform.\n\n"
        "BOVIMED provides **AI-assisted screening** and is not a substitute for "
        "professional veterinary diagnosis."
    ),
    version="0.2.0",
    lifespan=lifespan,
)

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list
    or [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "https://bovimed.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/media/uploads",
    StaticFiles(directory=str(settings.uploads_dir)),
    name="uploads",
)
app.mount(
    "/media/results",
    StaticFiles(directory=str(settings.results_dir)),
    name="results",
)

app.include_router(api_router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "detail": exc.detail},
        )
    logger.exception("Unhandled error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "detail": "An unexpected server error occurred. Please try again.",
            "error_code": "internal_error",
        },
    )


@app.get("/")
def root():
    s = get_settings()
    return {
        "name": "BOVIMED",
        "tagline": "Smart Vision for Healthier Herds",
        "status": "running",
        "step": 2,
        "docs": "/docs",
        "demo_mode": s.should_use_demo_mode(),
        "disclaimer": (
            "BOVIMED provides AI-assisted screening and is not a substitute for "
            "professional veterinary diagnosis."
        ),
    }
