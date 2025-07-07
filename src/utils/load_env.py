from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]

def load_env():
    load_dotenv(dotenv_path=BASE_DIR / '.env')
