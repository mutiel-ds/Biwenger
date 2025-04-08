from pydantic import BaseModel

from .status import Status

class Round(BaseModel):
    round_id: int # ID de la jornada
    season_id: int # ID de la temporada
    name: str # Nombre de la jornada
    status: str # Estado de la jornada
    _status: Status = Status.DESCONOCIDO # Estado de la jornada (automáticamente generado)

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._status = Status.from_value(value=self.status)