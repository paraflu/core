from selenium.webdriver.remote.webelement import WebElement


class Lezione:
    """Rappresenta una singola lezione."""

    def __init__(
        self, presente, ora, materia, docente, argomento, materia_short=None
    ) -> None:
        self.presente = presente
        self.ora = ora
        self.materia = materia
        self.materia_short = materia_short
        self.docente = docente
        self.argomento = argomento

    def to_dict(self) -> dict:
        return {
            "presente": self.presente,
            "ora": self.ora,
            "materia": self.materia,
            "materia_short": self.materia_short,
            "docente": self.docente,
            "argomento": self.argomento,
        }

    @staticmethod
    def from_text(data: WebElement):
        _, presente, ora, materia, materia_short, docente, argomento = data.text.split(
            "\n"
        )
        return Lezione(
            presente=presente,
            ora=ora,
            materia=materia,
            materia_short=materia_short,
            docente=docente,
            argomento=argomento,
        )

    def __str__(self) -> str:
        return f'ora {self.ora} materia {self.materia} con {self.docente}: {self.argomento}'
