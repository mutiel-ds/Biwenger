import os
from dotenv import load_dotenv

from enum import Enum
from typing import Dict

load_dotenv()

# Credenciales y configuración
class MyCredential(Enum):
    BIWENGER_EMAIL = os.environ["BIWENGER_EMAIL"]
    BIWENGER_PASSWORD = os.environ["BIWENGER_PASSWORD"]

class Credentials:
    email: str
    password: str

    def __init__(
        self,
        email: str = MyCredential.BIWENGER_EMAIL.value,
        password: str = MyCredential.BIWENGER_PASSWORD.value
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

# Sistema de Puntuaciones
class ScoringSystem(Enum):
    PICAS = 1
    SOFASCORE = 2
    MEDIA = 5

    @classmethod
    def from_value(cls, value: int) -> "ScoringSystem":
        """
        Devuelve un objeto ScoringSystem a partir de su valor.
        """
        for scoring_system in cls:
            if scoring_system.value == value:
                return scoring_system
        raise ValueError("Valor de sistema de puntuación no soportado.")
    
    def get_value(self) -> int:
        """
        Devuelve el valor de un objeto ScoringSystem.
        """
        return self.value
    
    def get_scoring_system(self) -> str:
        """
        Devuelve la descripción de un objeto ScoringSystem.
        """
        descriptions: Dict[ScoringSystem, str] = {
            ScoringSystem.PICAS: "Picas",
            ScoringSystem.SOFASCORE: "SofaScore",
            ScoringSystem.MEDIA: "Media"
        }

        return descriptions.get(self, "Sistema de puntuación desconocido")