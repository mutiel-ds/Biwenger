from datetime import datetime
from pydantic import BaseModel

from .status import Status

class Game(BaseModel):
    game_id: int # ID del partido
    round_id: int # ID de la jornada
    home_team_id: int # ID del equipo local
    away_team_id: int # ID del equipo visitante
    date: int # Fecha del partido (timestamp)
    status: str # Estado del partido
    _status: Status = Status.DESCONOCIDO # Estado del partido (automáticamente generado)
    home_team_score: int # Goles del equipo local
    away_team_score: int # Goles del equipo visitante

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._status = Status.from_value(value=self.status)

    def __str__(self) -> str:
        """
        Devuelve una representación en string del partido.
        """
        return f"{'-' * 30}\nPartido\nID del partido: {self.game_id}\nJornada: {self.round_id}\nEquipo Local (ID: {self.home_team_id}) {self.home_team_score} - {self.away_team_score} Equipo Visitante (ID: {self.away_team_id})\nFecha: {datetime.fromtimestamp(timestamp=self.date).strftime(format='%d/%m/%Y %H:%M')}\nEstado: {self._status.get_value()}\n{'-' * 30}"