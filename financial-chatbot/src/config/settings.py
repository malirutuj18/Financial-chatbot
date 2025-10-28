import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()

class Settings(BaseModel):
    """Application configuration settings"""
    
    # OpenAI Settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    model_name: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    temperature: float = float(os.getenv("TEMPERATURE", "0.1"))
    max_tokens: int = int(os.getenv("MAX_TOKENS", "2000"))
    
    # Alpha Vantage Settings
    alpha_vantage_api_key: str = os.getenv("ALPHA_VANTAGE_API_KEY", "")
    
    class Config:
        arbitrary_types_allowed = True
    
    def validate_keys(self) -> bool:
        """Validate that all required API keys are set"""
        errors = []
        
        if not self.openai_api_key:
            errors.append("OPENAI_API_KEY is not set")
        
        if not self.alpha_vantage_api_key:
            errors.append("ALPHA_VANTAGE_API_KEY is not set")
        
        if errors:
            error_msg = "\n".join([f"  • {err}" for err in errors])
            raise ValueError(f"\n❌ Configuration Error:\n{error_msg}\n\nPlease set these in your .env file")
        
        return True

# Create singleton instance
settings = Settings()
