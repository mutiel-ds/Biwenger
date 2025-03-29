import os
from dotenv import load_dotenv

load_dotenv()

# Credenciales y configuración
BIWENGER_EMAIL: str = os.environ["BIWENGER_EMAIL"]
BIWENGER_PASSWORD: str = os.environ["BIWENGER_PASSWORD"]

# URLs de la API
LOGIN_URL = "https://biwenger.as.com/api/v2/auth/login"
COMPETITION_URL = "https://biwenger.as.com/api/v2/competitions/la-liga/data?lang=es&score=1"

# User-Agent a usar en las peticiones
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
