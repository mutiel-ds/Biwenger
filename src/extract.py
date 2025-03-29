import logging

from typing import Dict

import requests
from requests import Response

from auth import login
from config import BIWENGER_EMAIL, BIWENGER_PASSWORD
from config import USER_AGENT, X_USER, X_LEAGUE, X_VERSION
from config import USER_DATA_URL_TEMPLATE, MARKET_DATA_URL, JORNADA_DATA_URL_TEMPLATE

def get_user_data(token: str) -> Dict | None:
    """
    Obtiene los datos del usuario (información del equipo, mercado, etc.)
    utilizando el endpoint correspondiente.
    """
    url: str = USER_DATA_URL_TEMPLATE
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {token}",
        "User-Agent": USER_AGENT,
        "X-User": X_USER,
        "X-League": X_LEAGUE,
        "X-Version": X_VERSION
    }
    try:
        response: Response = requests.get(url=url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(msg=f"Error al obtener datos del usuario: {e}")
        return None

    try:
        data: Dict = response.json()
    except ValueError as e:
        logging.error(msg=f"Error al parsear JSON de datos del usuario: {e}")
        return None

    logging.info(msg="Datos del usuario obtenidos exitosamente.")
    return data

def get_market_data(token: str) -> Dict | None:
    """
    Obtiene la información actual del mercado (fichajes activos, ofertas, etc.)
    """
    headers: Dict[str, str] = {"Authorization": f"Bearer {token}", "User-Agent": USER_AGENT}
    try:
        response: Response = requests.get(url=MARKET_DATA_URL, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(msg=f"Error al obtener datos del mercado: {e}")
        return None

    try:
        data: Dict = response.json()
    except ValueError as e:
        logging.error(msg=f"Error al parsear JSON del mercado: {e}")
        return None

    logging.info(msg="Datos del mercado obtenidos exitosamente.")
    return data

def get_jornada_data(token: str, round_id: int) -> Dict | None:
    """
    Obtiene los datos de una jornada (por ejemplo, estadísticas, puntuaciones de jugadores)
    dada la identificación de la jornada.
    """
    url: str = JORNADA_DATA_URL_TEMPLATE.format(round_id=round_id)
    headers: Dict[str, str] = {"Authorization": f"Bearer {token}", "User-Agent": USER_AGENT}
    try:
        response: Response = requests.get(url=url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(msg=f"Error al obtener datos de la jornada: {e}")
        return None

    try:
        data: Dict = response.json()
    except ValueError as e:
        logging.error(msg=f"Error al parsear JSON de la jornada: {e}")
        return None

    logging.info(msg="Datos de la jornada obtenidos exitosamente.")
    return data

if __name__ == "__main__":
    # Ejemplo de uso: primero se autentica y luego se extraen algunos datos.
    token: str | None = login(email=BIWENGER_EMAIL, password=BIWENGER_PASSWORD)
    if token:
        # Ejemplo: obtener datos de la jornada 1
        #jornada_data: Dict | None = get_jornada_data(token=token, round_id=1)
        #if jornada_data:
        #    print("Datos de la jornada 1:")
        #    print(jornada_data)
        
        # Ejemplo: obtener datos del mercado
        #market_data: Dict | None = get_market_data(token=token)
        #if market_data:
        #    print("Datos del mercado:")
        #    print(market_data)
        
        # Ejemplo: obtener datos de usuario (necesitas conocer el user_id)
        # Sustituye 'tu_user_id' por el ID correspondiente (se puede extraer en el proceso de login)
        user_data: Dict | None = get_user_data(token=token)
        if user_data:
            print("Datos del usuario:")
            print(user_data)
    else:
        print("Error en la autenticación. No se pudieron obtener datos.")