from typing import Dict, Optional

import requests
from requests import Response

from config import PICAS, SOFASCORE, MEDIA
from config import USER_AGENT, X_USER, X_LEAGUE, X_VERSION
from config import LOGIN_URL, SEASON_DATA_URL, ROUND_DATA_URL 

import time
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Wrapper:
    def __init__(self, email: str, password: str) -> None:
        logging.info(msg="Creando instancia de Wrapper.")
        self.email: str = email
        self.password: str = password

        logging.info(msg="Iniciando sesión en Biwenger.")
        self.token: str = self.login()
        logging.info(msg="Login exitoso. Token obtenido.")

    def login(self) -> str:
        """
        Realiza el login en Biwenger y devuelve el token de autenticación.

        Returns:
            str: Token de autenticación.
        """
        headers: Dict[str, str] = {
            "User-Agent": USER_AGENT,
        }
        payload: Dict[str, str] = {
            "email": self.email,
            "password": self.password
        }
        
        try:
            response: Response = requests.post(url=LOGIN_URL, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(msg=f"Error iniciando sesión: {e}")
            raise Exception("Error iniciando sesión. Compruebe sus credenciales.")

        try:
            data: Dict = response.json()
        except ValueError as e:
            logging.error(msg=f"Error al parsear la respuesta JSON: {e}")
            raise Exception("Error al parsear la respuesta JSON. Compruebe sus credenciales.")

        token: str | None = data.get("token")
        if not token:
            logging.error(msg=f"Token no encontrado en la respuesta: {data}")
            raise Exception("Token no encontrado en la respuesta. Compruebe sus credenciales.")
        
        return token
    
    def get_user_agent_header(self) -> Dict:
        """
        Devuelve un diccionario con el User-Agent necesario para realizar peticiones a la API de Biwenger.

        Returns:
            Dict: Diccionario con el User-Agent.
        """
        return {
            "User-Agent": USER_AGENT
        }
    
    def get_user_headers(self, token: str, user_agent: str = USER_AGENT, x_user: str = X_USER, x_league: str = X_LEAGUE, x_version: str = X_VERSION) -> Dict:
        """
        Devuelve un diccionario con los headers necesarios para realizar peticiones a la API de Biwenger.

        Args:
            token (str): Token de autenticación.
            user_agent (str): User-Agent a utilizar. Default: USER_AGENT.
            x_user (str): X-User a utilizar. Default: X_USER.
            x_league (str): X-League a utilizar. Default: X_LEAGUE.
            x_version (str): X-Version a utilizar. Default: X_VERSION.
        """
        return {
            "Authorization": f"Bearer {token}",
            "User-Agent": user_agent,
            "X-User": x_user,
            "X-League": x_league,
            "X-Version": x_version
        }
    
class Extractor(Wrapper):
    def _make_request_with_retry(self, url: str, headers: Dict, max_retries: int = 5) -> Dict:
        """
        Makes a request with retry logic for rate limiting.
        
        Args:
            url (str): URL to make the request to
            headers (Dict): Headers to use in the request
            max_retries (int): Maximum number of retries before failing
        """
        data: Dict = {}
        for attempt in range(max_retries):
            response: Response = requests.get(url=url, headers=headers)
            data: Dict = response.json()
            
            if data.get("status") != 429:
                return data
                
            wait_time: int = min(2 ** attempt, 60)
            logging.warning(msg=f"Rate limit exceeded. Attempt {attempt + 1}/{max_retries}. "
                          f"Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)
            
        raise Exception(f"Failed after {max_retries} attempts: {data.get('userMessage', 'Unknown error')}")

    def get_season_data(self, year: int, score: int) -> Dict:
        """
        Obtiene los datos de la temporada especificada.
        
        Args:
            year (int): Año de la temporada.
            score (int): Sistema de puntuación a utilizar.
        """
        header: Dict = self.get_user_agent_header()
        url: str = SEASON_DATA_URL.format(year=year, score=score)
        return self._make_request_with_retry(url=url, headers=header)
    
    def get_round_data(self, round: Optional[int]) -> Dict:
        """
        Obtiene los datos de la jornada especificada.

        Args:
            round (int, Opcional): Número de la jornada. Selecciona la jornada actual si no se especifica.
        """
        header: Dict = self.get_user_agent_header()
        if round:
            url: str = ROUND_DATA_URL.format(round=round)
        else:
            url: str = ROUND_DATA_URL.split(sep="/{round}")[0]
        return self._make_request_with_retry(url=url, headers=header)