from datetime import datetime

class Notizia:
    def __init__(self, timestamp: datetime, titolo: str, testo:str = '', allegati: list[str] = []) -> None:
        self.timestamp = timestamp
        self.titolo = titolo
        self.testo = testo
        self.allegati = allegati

    def to_dict(self)->dict:
        return {
            'timestamp': self.timestamp,
            'titolo': self.titolo,
            'testo': self.testo,
            'allegati': self.allegati,
        }