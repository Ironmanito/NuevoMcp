import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Campus configuration
    campus_user: str = os.getenv("CAMPUS_USER", "")
    campus_password: str = os.getenv("CAMPUS_PASSWORD", "")
    campus_url: str = os.getenv("CAMPUS_URL", "https://campus.example.com")
    
    # Server configuration
    server_host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    server_port: int = int(os.getenv("SERVER_PORT", "5000"))
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = environment == "development"
    
    # MCP Configuration
    mcp_transport: str = os.getenv("MCP_TRANSPORT", "sse")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
