import os

from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    APP_NAME = "Ichiba Merchant Support Assistant"
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "demo-key")
    GROQ_API_BASE = os.getenv("GROQ_API_BASE", "https://api.groq.com/openai/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    ENV = os.getenv("ENV", "dev")

settings = Settings()