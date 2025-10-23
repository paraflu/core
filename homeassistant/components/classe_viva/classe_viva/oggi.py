from datetime import datetime

from .lezione import Lezione


class Oggi:
    """Istanza delle lezioni di oggi."""

    def __init__(
        self,
        timestamp: datetime,
        nota_disciplinare: str | None,
        annotazione: str | None,
        lezioni: list[Lezione],
    ) -> None:
        """Costruttore della classe.

        Args:
            timestamp: (datetime) data dell'evento
            nota_disciplinare (str | None): _description_
            annotazione (str | None): _description_
            lezioni (list[Lezione]): _description_
        """
        self.timestamp = timestamp
        self.nota_disciplinare = nota_disciplinare
        self.annotazione = annotazione
        self.lezioni = lezioni

    def to_dict(self) -> dict:
        """Converte l'oggetto in dict."""
        return {
            "timestamp": self.timestamp,
            "nota_disciplinare": self.nota_disciplinare,
            "annotazione": self.annotazione,
            "lezioni": [lezione.to_dict() for lezione in self.lezioni],
        }
