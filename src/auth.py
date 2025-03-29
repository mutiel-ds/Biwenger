import logging

import requests
from requests import Response

from typing import Dict

from config import BIWENGER_EMAIL, BIWENGER_PASSWORD, LOGIN_URL, USER_AGENT

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def login(email: str, password: str) -> str | None:
    """
    Realiza el login en Biwenger y devuelve el token de autenticación.
    Retorna None en caso de error.
    """
    headers: Dict[str, str] = {
        "User-Agent": USER_AGENT,
    }
    payload: Dict[str, str] = {
        "email": email,
        "password": password
    }
    
    try:
        response: Response = requests.post(url=LOGIN_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(msg=f"Error en la petición de autenticación: {e}")
        return None

    try:
        data: Dict = response.json()
    except ValueError as e:
        logging.error(msg=f"Error al parsear la respuesta JSON: {e}")
        return None

    token: str | None = data.get("token")
    if not token:
        logging.error(msg=f"Token no encontrado en la respuesta: {data}")
    else:
        logging.info(msg="Login exitoso. Token obtenido.")
    return token

if __name__ == "__main__":
    # Prueba de autenticación utilizando las credenciales del archivo de configuración
    token: str | None = login(email=BIWENGER_EMAIL, password=BIWENGER_PASSWORD)
    if token:
        print("Token:", token)
    else:
        print("Fallo en la autenticación.")
