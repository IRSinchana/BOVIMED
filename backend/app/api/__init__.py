from fastapi import APIRouter

from app.api import alerts, analyze, auth, chat, cows, dashboard, health, history, model_info, notifications, vets

api_router = APIRouter(prefix="/api")
api_router.include_router(health.router)
api_router.include_router(model_info.router)
api_router.include_router(auth.router)
api_router.include_router(analyze.router)
api_router.include_router(cows.router)
api_router.include_router(history.router)
api_router.include_router(dashboard.router)
api_router.include_router(alerts.router)
api_router.include_router(notifications.router)
api_router.include_router(chat.router)
api_router.include_router(vets.router)
