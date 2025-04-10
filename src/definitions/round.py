from pydantic import BaseModel

from src.definitions.status import Status

class Round(BaseModel):
    round_id: int # ID de la jornada
    season_id: int # ID de la temporada
    round_name: str # Nombre de la jornada
    round_status: str # Estado de la jornada
    _status: Status = Status.DESCONOCIDO # Estado de la jornada (automáticamente generado)

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._status = Status.from_value(value=self.round_status)

    @classmethod
    def from_dict(cls, data: dict) -> "Round":
        """
        Crea un objeto Round a partir de un diccionario.
        """
        return cls(**data)

    def to_dict(self) -> dict:
        """
        Convierte el objeto Round a un diccionario.
        """
        return {
            "round_id": self.round_id,
            "season_id": self.season_id,
            "round_name": self.round_name,
            "round_status": self.round_status,
            #"_status": self._status.value
        }

    def __str__(self) -> str:
        """
        Devuelve una representación en string de la jornada.
        """
        return f"{'-' * 30}\nJornada\nID: {self.round_id}\nTemporada ID: {self.season_id}\nNombre: {self.round_name}\nEstado: {self._status.get_value()}\n{'-' * 30}"