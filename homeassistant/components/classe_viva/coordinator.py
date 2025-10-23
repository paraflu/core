from datetime import date, timedelta
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .classe_viva import ClasseViva
from .const import DOMAIN, UPDATE_INTERVAL


class ClasseVivaCoordinator(DataUpdateCoordinator):
    """Coordinatore per accedere ai dati di classe viva."""

    def __init__(self, hass: HomeAssistant, config) -> None:
        """Costruttore."""

        self.logger = logging.getLogger(__name__)

        super().__init__(
            hass,
            self.logger,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.username = config["username"]
        self.password = config["password"]

    async def _async_update_data(self):
        return await self.hass.async_add_executor_job(self.scrape)

    def scrape(self):
        # driver = webdriver.Chrome(options=self._options())
        # driver.get("https://web.spaggiari.eu/home/app/default/login.php")
        # driver.find_element(By.ID, "login").send_keys(self.username)
        # driver.find_element(By.ID, "password").send_keys(self.password)
        # driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.ID, "main-content"))
        # )

        # driver.get("https://web.spaggiari.eu/fml/app/default/agenda_studenti.php")
        # oggi = date.today().strftime("%d/%m/%Y")
        # eventi = driver.find_elements(
        #     By.XPATH, f"//div[contains(text(), '{oggi}')]/following-sibling::div"
        # )

        # data = [e.text.strip() for e in eventi]
        # driver.quit()
        # return {"data": oggi, "eventi": data}
        classe_viva = ClasseViva(self.username, self.password)
        bacheca = classe_viva.bacheca()
        return classe_viva.oggi()
