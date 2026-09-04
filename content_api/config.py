import os
from dotenv import load_dotenv
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
env_path = project_root / ".env"
load_dotenv(env_path)

SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
AWS_PROFILE = os.environ.get("AWS_PROFILE")
AWS_REGION = os.environ.get("AWS_REGION")
BUCKET_NAME = os.environ.get("CONTENT_AI_BUCKET_NAME")
