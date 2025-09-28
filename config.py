import os
from dotenv import load_dotenv

# Load .env into environment
load_dotenv()


class Config:
    ENV = os.getenv("ENV", "PROD")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", "5000"))
    COURSES_ROOT_DIRECTORY_ABS_PATH = os.getenv("COURSES_ROOT_DIRECTORY_ABS_PATH", "")
