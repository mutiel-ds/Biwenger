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

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """
        Crea un objeto Player a partir de un diccionario.
        """
        return cls(**data)

    def to_dict(self) -> dict:
        """
        Convierte el objeto Player a un diccionario.
        """
        return {
            "player_id": self.player_id,
            "player_name": self.player_name,
            "player_position": self.player_position
        }

    def __str__(self) -> str:
        """
        Devuelve una representación en string del jugador.
        """
        return f"{'-' * 30}\nJugador: {self.player_name}\nID: {self.player_id}\nPosición: {self._player_position_name}\n{'-' * 30}"

class PlayerPerformance(BaseModel):
    player_performance_id: str = "" # ID único de la actuación del jugador (automáticamente generado)
    player_id: int # ID del jugador
    game_id: int # ID del partido
    team_id: int # ID del equipo

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.player_performance_id = f"{self.player_id}_{self.game_id}_{self.team_id}"

    @classmethod
    def from_dict(cls, data: dict) -> "PlayerPerformance":
        """
        Crea un objeto PlayerPerformance a partir de un diccionario.
        """
        if "player_performance_id" in data:
            del data["player_performance_id"]
        return cls(**data)

    def to_dict(self) -> dict:
        """
        Convierte el objeto PlayerPerformance a un diccionario.
        """
        return {
            "player_performance_id": self.player_performance_id,
            "player_id": self.player_id,
            "game_id": self.game_id,
            "team_id": self.team_id
        }

    def __str__(self) -> str:
        """
        Devuelve una representación en string de la actuación del jugador.
        """
        return f"{'-' * 30}\nActuación del Jugador\nID de actuación: {self.player_performance_id}\nID del jugador: {self.player_id}\nID del partido: {self.game_id}\nID del equipo: {self.team_id}\n{'-' * 30}"