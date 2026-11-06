import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
BOOKS_DIR = ROOT / "data" / "books"
CHROMA_DIR = ROOT / "data" / "chroma"

COLLECTION = "english_books"
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]