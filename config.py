import os

class Settings:
    APP_NAME = "Ichiba Merchant Support Assistant"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "demo-key")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
    ENV = os.getenv("ENV", "dev")

settings = Settings()