from datetime import datetime

from .notizia import Notizia


class Bacheca:
    """Istanza delle lezioni di oggi."""

    def __init__(
        self,
        timestamp: datetime,
        notizie: list[Notizia] = []
    ) -> None:
        """Costruttore della classe."""

        self.timestamp = timestamp
        self.notizie = notizie

    def to_dict(self) -> dict:
        """Converte l'oggetto in dict."""
        return {
            "timestamp": self.timestamp,
            "notizie": [notizia.to_dict() for notizia in self.notizie],
        }

 