from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ClasseVivaSensor(coordinator)], True)


class ClasseVivaSensor(SensorEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator

    @property
    def name(self):
        return "ClasseViva Attività"

    @property
    def state(self):
        if self.coordinator.data.lezioni is None or len(self.coordinator.data.lezioni) == 0:
            return 'Nessuna attività'
        eventi = ", ".join([str(lezione) for lezione in self.coordinator.data.lezioni])
        if len(eventi) > 255:
            eventi = eventi[:252] + "..."
        return eventi

    @property
    def extra_state_attributes(self):
        return {
            'data': self.coordinator.data.timestamp,
            'nota_disciplinare': self.coordinator.data.nota_disciplinare,
            'annotazione': self.coordinator.data.annotazione,
            'lezioni': [
                str(lezione) for lezione in self.coordinator.data.lezioni
            ]
        }
