from pydantic import BaseModel

from definitions.status import Status

class Season(BaseModel):
    season_id: int # ID de la temporada
    name: str # Nombre de la temporada
    status: str # Estado de la temporada
    _status: Status = Status.DESCONOCIDO # Estado de la temporada (automáticamente generado)

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._status = Status.from_value(value=self.status)