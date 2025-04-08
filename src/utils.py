from time import sleep

def wait(seconds: int = 5) -> None:
    """
    Espera un tiempo determinado en segundos.

    Args:
        seconds (int): Tiempo a esperar en segundos.
    """
    sleep(seconds)