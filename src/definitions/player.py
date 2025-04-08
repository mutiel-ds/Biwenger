from enum import Enum
from typing import Dict
from uuid import uuid4, UUID
from pydantic import BaseModel

class PlayerPosition(Enum):
    DESCONOCIDA = 0
    PORTERO = 1
    DEFENSA = 2
    CENTROCAMPISTA = 3
    DELANTERO = 4

    @classmethod
    def from_value(cls, value: int) -> "PlayerPosition":
        """
        Devuelve un objeto PlayerPosition a partir de su valor.
        """
        for player_position in cls:
            if player_position.value == value:
                return player_position
        raise ValueError("Valor de posición de jugador no soportado.")
    
    def get_value(self) -> int:
        """
        Devuelve el valor de un objeto PlayerPosition.
        """
        return self.value
    
    def get_position(self) -> str:
        """
        Devuelve la descripción de un objeto PlayerPosition.
        """
        descriptions: Dict[PlayerPosition, str] = {
            PlayerPosition.DESCONOCIDA: "Posición desconocida",
            PlayerPosition.PORTERO: "Portero",
            PlayerPosition.DEFENSA: "Defensa",
            PlayerPosition.CENTROCAMPISTA: "Centrocampista",
            PlayerPosition.DELANTERO: "Delantero"
        }

        return descriptions.get(self, "Posición desconocida")

class Player(BaseModel):
    player_id: int # ID del jugador
    player_name: str # Nombre del jugador
    player_position: int # ID de la posición del jugador
    _player_position: PlayerPosition = PlayerPosition.DESCONOCIDA # Posición del jugador (automáticamente generado)
    _player_position_name: str = "" # Nombre de la posición del jugador (automáticamente generado)

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._player_position = PlayerPosition.from_value(value=self.player_position)
        self._player_position_name = self._player_position.get_position()

class PlayerPerformance(BaseModel):
    player_performance_id: UUID = uuid4() # ID único de la actuación del jugador (automáticamente generado)
    player_id: int # ID del jugador
    game_id: int # ID del partido
    team_id: int # ID del equipo
    points: int # Puntos obtenidos por el jugador en el partido