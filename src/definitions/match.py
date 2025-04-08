from pydantic import BaseModel

from definitions.status import Status

class Match(BaseModel):
    match_id: int # ID del partido
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