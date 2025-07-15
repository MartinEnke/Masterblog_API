# backend/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "blog.db")
print("Using DB path:", DB_PATH)

print("POSTGRES_USER:", os.getenv("POSTGRES_USER"))
print("POSTGRES_PASSWORD:", os.getenv("POSTGRES_PASSWORD"))
print("POSTGRES_DB:", os.getenv("POSTGRES_DB"))
print("POSTGRES_HOST:", os.getenv("POSTGRES_HOST"))
print("POSTGRES_PORT:", os.getenv("POSTGRES_PORT"))

POSTGRES_USER = os.getenv("POSTGRES_USER", "your_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "your_password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "your_dbname")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

print("Connecting to DB with:", DATABASE_URL)

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()



