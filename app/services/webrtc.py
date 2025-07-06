import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TurnCredentialsService:
    """Service to provide TURN server credentials"""
    
    def __init__(self):
        self.turn_server_url = os.getenv("TURN_SERVER_URL", "turn:your-server-ip:3478")
        self.turn_server_username = os.getenv("TURN_SERVER_USERNAME", "username")
        self.turn_server_credential = os.getenv("TURN_SERVER_CREDENTIAL", "password")
    
    def get_turn_credentials(self):
        """Get TURN server credentials for WebRTC connections"""
        return {
            "urls": [self.turn_server_url],
            "username": self.turn_server_username,
            "credential": self.turn_server_credential
        }
    
    def get_ice_servers(self):
        """Get a list of ICE servers including TURN and STUN"""
        return {
            "iceServers": [
                {
                    "urls": ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302"]
                },
                self.get_turn_credentials()
            ]
        }
