import os
from dotenv import load_dotenv

from enum import Enum
from uuid import uuid4
from typing import Dict, Any

load_dotenv()

# Credenciales y configuración
BIWENGER_EMAIL: str = os.environ["BIWENGER_EMAIL"]
BIWENGER_PASSWORD: str = os.environ["BIWENGER_PASSWORD"]

class Credentials:
    email: str
    password: str

    def __init__(
        self,
        email: str = BIWENGER_EMAIL,
        password: str = BIWENGER_PASSWORD
    ) -> None:
        self.email = email
        self.password = password
        

## Headers a usar en las peticiones de usuario
class Headers(Enum):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
    X_USER = os.environ["X-USER"]
    X_LEAGUE = os.environ["X-LEAGUE"]
    X_VERSION = os.environ["X-VERSION"]

# URLs de la API
class APIUrls(Enum):
    LOGIN_URL = "https://biwenger.as.com/api/v2/auth/login"
    SEASON_DATA_URL = "https://cf.biwenger.com/api/v2/competitions/la-liga/season/{year}"
    ROUND_DATA_URL = "https://biwenger.as.com/api/v2/rounds/la-liga/{round}"
    GAME_DATA_URL = "https://cf.biwenger.com/api/v2/matches/la-liga/{game}?score={score}"

# URLs adicionales
class AdditionalUrls(Enum):
    COMPETITION_URL = "https://biwenger.as.com/api/v2/competitions/la-liga/data?lang=es&score=1"
    MARKET_DATA_URL = "https://biwenger.as.com/api/v2/market/active"
    JORNADA_DATA_URL_TEMPLATE = "https://biwenger.as.com/api/v2/rounds/la-liga/{round_id}"
    USER_DATA_URL_TEMPLATE = "https://biwenger.as.com/api/v2/user?fields=*,lineup"

# SUpabase DB configuration
SUPABASE_URL: str = os.environ["SUPABASE_URL"]
SUPABASE_SECRET_KEY: str = os.environ["SUPABASE_SECRET_KEY"]
SUPABASE_PUBLIC_KEY: str = os.environ["SUPABASE_PUBLIC_KEY"]

# Postgres DB configuration
DB_CONFIG: Dict[str, Any] = {
    "host": os.environ["DB_HOST"],
    "port": os.environ["DB_PORT"],
    "database": os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"]
}

# Database PKs
PK_COLUMNS: Dict[str, Dict] = {
    "events": {
        "column": os.environ["EVENTS"],
        "value": "None"
    },
    "performance_scores": {
        "column": os.environ["PERFORMANCE_SCORES"],
        "value": "None"
    },
    "player_performances": {
        "column": os.environ["PLAYER_PERFORMANCES"],
        "value": "None"
    },
    "players": {
        "column": os.environ["PLAYERS"],
        "value": -1
    },
    "games": {
        "column": os.environ["GAMES"],
        "value": -1
    },
    "teams": {
        "column": os.environ["TEAMS"],
        "value": -1
    },
    "rounds": {
        "column": os.environ["ROUNDS"],
        "value": -1
    },
    "seasons": {
        "column": os.environ["SEASONS"],
        "value": -1
    },
}