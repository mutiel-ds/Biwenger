import os
from dotenv import load_dotenv

from enum import Enum

load_dotenv()

# Credenciales y configuración
class Credentials(Enum):
    BIWENGER_EMAIL = os.environ["BIWENGER_EMAIL"]
    BIWENGER_PASSWORD = os.environ["BIWENGER_PASSWORD"]

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

# Sistema de Puntuaciones
class ScoringSystem(Enum):
    PICAS = 1
    SOFASCORE = 2
    MEDIA = 5