import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    USE_OPENAI = os.getenv("USE_OPENAI", "false").lower() == "true"
    MAX_HISTORY_TURNS = int(os.getenv("MAX_HISTORY_TURNS", 12))
