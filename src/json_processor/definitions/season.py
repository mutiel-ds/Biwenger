from pydantic import BaseModel

from src import Status

class Season(BaseModel):
    season_id: int # ID de la temporada
    season_name: str # Nombre de la temporada
    season_status: str # Estado de la temporada
    _status: Status = Status.DESCONOCIDO # Estado de la temporada (automáticamente generado)

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._status = Status.from_value(value=self.season_status)

    def __str__(self) -> str:
        """
        Devuelve una representación en string de la temporada.
        """
        return f"{'-' * 30}\nTemporada\nID: {self.season_id}\nNombre: {self.season_name}\nEstado: {self._status.get_value()}\n{'-' * 30}"