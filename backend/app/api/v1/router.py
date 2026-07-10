from fastapi import APIRouter

from app.api.v1.routes import auth, panels, providers, subscriptions, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(panels.router, prefix="/panels", tags=["Panels"])
api_router.include_router(providers.router, prefix="/providers", tags=["Providers"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])
