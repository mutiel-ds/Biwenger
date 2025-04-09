from pydantic import BaseModel

from src import Status

class Round(BaseModel):
    round_id: int # ID de la jornada
    season_id: int # ID de la temporada
    name: str # Nombre de la jornada
    status: str # Estado de la jornada
    _status: Status = Status.DESCONOCIDO # Estado de la jornada (automáticamente generado)

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._status = Status.from_value(value=self.status)

    def __str__(self) -> str:
        """
        Devuelve una representación en string de la jornada.
        """
        return f"{'-' * 30}\nJornada\nID: {self.round_id}\nTemporada ID: {self.season_id}\nNombre: {self.name}\nEstado: {self._status.get_value()}\n{'-' * 30}"