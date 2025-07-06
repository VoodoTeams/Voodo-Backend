from fastapi import APIRouter, Depends
from app.services.webrtc import TurnCredentialsService

router = APIRouter(
    prefix="/webrtc",
    tags=["webrtc"],
    responses={404: {"description": "Not found"}}
)

@router.get("/ice-servers")
async def get_ice_servers(
    turn_service: TurnCredentialsService = Depends(lambda: TurnCredentialsService())
):
    """Get ICE server configuration for WebRTC"""
    return turn_service.get_ice_servers()
