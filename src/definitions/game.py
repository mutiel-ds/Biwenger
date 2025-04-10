from datetime import datetime
from pydantic import BaseModel

from src.definitions.status import Status

class Game(BaseModel):
    game_id: int # ID del partido
    round_id: int # ID de la jornada
    home_team_id: int # ID del equipo local
    away_team_id: int # ID del equipo visitante
    date: int # Fecha del partido (timestamp)
    game_status: str # Estado del partido
    _status: Status = Status.DESCONOCIDO # Estado del partido (automáticamente generado)
    home_team_score: int # Goles del equipo local
    away_team_score: int # Goles del equipo visitante

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._status = Status.from_value(value=self.game_status)

    def _convert_date(self) -> str:
        """
        Converts a timestamp to a datetime object.
        """
        return datetime.fromtimestamp(timestamp=self.date).isoformat()

    @classmethod
    def from_dict(cls, data: dict) -> "Game":
        """
        Crea un objeto Game a partir de un diccionario.
        """
        return cls(**data)

    def to_dict(self) -> dict:
        """
        Convierte el objeto Game a un diccionario.
        """
        return {
            "game_id": self.game_id,
            "round_id": self.round_id,
            "home_team_id": self.home_team_id,
            "away_team_id": self.away_team_id,
            "date": self.date,
            "game_status": self.game_status,
            #"_status": self._status.value,
            "home_team_score": self.home_team_score,
            "away_team_score": self.away_team_score
        }

    def __str__(self) -> str:
        """
        Devuelve una representación en string del partido.
        """
        return f"{'-' * 30}\nPartido\nID del partido: {self.game_id}\nJornada: {self.round_id}\nEquipo Local (ID: {self.home_team_id}) {self.home_team_score} - {self.away_team_score} Equipo Visitante (ID: {self.away_team_id})\nFecha: {datetime.fromtimestamp(timestamp=self.date).strftime(format='%d/%m/%Y %H:%M')}\nEstado: {self._status.get_value()}\n{'-' * 30}"