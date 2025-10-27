import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NebiusConfig:
    """Configuration for Nebius AI integration"""
    
    API_KEY = os.getenv('NEBIUS_API_KEY')
    BASE_URL = os.getenv('NEBIUS_BASE_URL', 'https://api.nebius.ai/v1')
    MODEL = os.getenv('NEBIUS_MODEL', 'meta-llama/Llama-3.3-70B-Instruct')
    
    # Model parameters
    MAX_TOKENS = 4000
    TEMPERATURE = 0.1  # Low temperature for consistent medical analysis
    TOP_P = 0.9
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.API_KEY:
            raise ValueError("NEBIUS_API_KEY not found in environment variables")
        return True