from enum import Enum

class Status(Enum):
    DESCONOCIDO = "unknown"
    PENDING = "pending"
    PREVIEW = "preview"
    FINISHED = "finished"
    IN_PROGRESS = "in_progress"

    @classmethod
    def from_value(cls, value: str) -> "Status":
        """
        Devuelve un objeto Status a partir de su valor.
        """
        for round_status in cls:
            if round_status.value == value:
                return round_status
        raise ValueError("Valor de estado no soportado.")

    def get_value(self) -> str:
        """
        Devuelve el valor de un objeto Status.
        """
        return self.value

