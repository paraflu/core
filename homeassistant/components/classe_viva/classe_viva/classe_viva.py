from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime

from .lezione import Lezione
from .oggi import Oggi
from .notizia import Notizia
from .bacheca import Bacheca

def parse_date(date:str) -> datetime:
    mesi_italiani = {
        'gennaio': 1, 'febbraio': 2, 'marzo': 3, 'aprile': 4,
        'maggio': 5, 'giugno': 6, 'luglio': 7, 'agosto': 8,
        'settembre': 9, 'ottobre': 10, 'novembre': 11, 'dicembre': 12
    }

    data_str = "23 ottobre 2025"
    parti = data_str.split()
    giorno = int(parti[0])
    mese = mesi_italiani[parti[1].lower()]
    anno = int(parti[2])

    return datetime(anno, mese, giorno)

class Utils:
    """Classe necessaria per generizzare alcune operazioni ripetitive."""

    @staticmethod
    def wait(
        driver: RemoteWebDriver,
        element: WebElement | tuple[str, str],
        timeout: int = 10,
    ):
        """Attendo che un elemento sia visibile.

        Args:
            driver (RemoteWebDriver): _description_
            element (WebElement | tuple[str, str]): _description_
            timeout (int, optional): _description_. Defaults to 10.

        Returns:
            _type_: _description_
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.element_to_be_clickable(element))

    @staticmethod
    def type(
        driver: RemoteWebDriver,
        element: WebElement | tuple[str, str],
        text: str,
        timeout: int = 10,
    ):
        el = Utils.wait(driver=driver, element=element, timeout=timeout)
        el.clear()
        el.send_keys(text)

    @staticmethod
    def click(
        driver: RemoteWebDriver,
        element: WebElement | tuple[str, str],
        timeout: int = 10,
    ):
        Utils.wait(driver, element, timeout).click()


class ClasseViva(Utils):
    """Istanza che esegue lo scraper del sito."""

    def __init__(self, username: str, password: str, headless=True) -> None:
        """Inizializzazione."""
        opts = Options()
        if headless:
            opts.add_argument("--headless")
            opts.add_argument("--no-sandbox")
            opts.add_argument("--disable-dev-shm-usage")

        self.b = webdriver.Chrome(options=opts)
        self._username = username
        self._password = password
        self.logged = False

    def login(self):
        self.b.get("https://web.spaggiari.eu/home/app/default/login.php")

        self.type(self.b, (By.ID, "login"), text=self._username)
        self.type(self.b, (By.ID, "password"), text=self._password)
        self.click(self.b, (By.CSS_SELECTOR, ".accedi"))
        self.wait(self.b, (By.CSS_SELECTOR, ".lastaccess-label"))

        self.logged = True

    def quit(self):
        """Chiude il browser."""
        self.b.quit()

    def _get_section_text(self, titolo):
        try:
            # Trova la sezione con il titolo richiesto
            section = self.wait(
                self.b,
                (By.XPATH, f"//h2[normalize-space()='{titolo}']/ancestor::section"),
            )
            # Trova lo span col testo all’interno della sezione
            span = section.find_element(
                By.XPATH,
                ".//span[contains(@class,'open-sans') and contains(@class,'fs-25')]",
            )
            return span.text.strip()
        except Exception:  # noqa: BLE001
            return None

    def oggi(self) -> Oggi:
        """Recupera le attività di oggi.

        Returns:
            Oggi: attività della giornata
        """
        if not self.logged:
            self.login()

        self.b.get("https://web.spaggiari.eu/fml/app/default/attivita_studente.php")
        note = self._get_section_text("NOTE DISCIPLINARI")
        annotazione = self._get_section_text("ANNOTAZIONI")
        h2 = self.b.find_element(By.CSS_SELECTOR,'section.mx-15:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > h2:nth-child(1)')
        timestamp = parse_date(h2.text)

        return Oggi(
            timestamp=timestamp,
            nota_disciplinare=note
            if note is not None and "Nessuna nota disciplinare presente" not in note
            else None,
            annotazione=annotazione
            if annotazione is not None and "Nessuna annotazione" not in annotazione
            else None,
            lezioni=[
                self._parse_lezione(lezione)
                for lezione in self.b.find_elements(By.CSS_SELECTOR, "div.table-row")
            ],
        )
    
    def bacheca(self) -> Bacheca:
        if not self.logged:
            self.login()

        self.b.get("https://web.spaggiari.eu/sif/app/default/bacheca_personale.php")

        self.wait(self.b, (By.CSS_SELECTOR, "#box_row_other"))

        b = Bacheca(timestamp=datetime.now())
        for row in self.b.find_elements(By.CSS_SELECTOR, '#box_row_other > tr'):
            print(row.text)
            titolo, _, data, _ = row.text.split('\n')
            notizia = Notizia(parse_date(data), titolo)
            row.find_element(By.CSS_SELECTOR, 'a.specifica').click()
            self.wait(self.b, (By.CSS_SELECTOR, '.ui-dialog-title'))
            notizia.testo = self.b.find_element(By.CSS_SELECTOR, '.comunicazione_testo').text

            b.notizie.append(notizia)

        return b

            

    def _parse_lezione(self, lezione: WebElement) -> Lezione:
        # _, presente, ora, materia, materia_short, docente, argomento = lezione.text.split(
        #     '\n')

        # return {
        #     'presente': presente.lower() == 'presente',
        #     'ora': ora,
        #     'materia': materia,
        #     'materia_short': materia_short,
        #     'docente': docente,
        #     'argomento': argomento.replace('Lezione: ', '')
        # }
        return Lezione.from_text(lezione)
