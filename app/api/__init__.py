from fastapi import APIRouter
from app.api.hangouts import router as hangouts_router
from app.api.webrtc import router as webrtc_router

# Main API router
api_router = APIRouter()

# Include all route modules
api_router.include_router(hangouts_router)
api_router.include_router(webrtc_router)
