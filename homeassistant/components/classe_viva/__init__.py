from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import ClasseVivaCoordinator

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config):
    """Indica che è necessaria la configurazione."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Setup della integrazione."""
    coordinator = ClasseVivaCoordinator(hass, entry.data)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def handle_refresh(call):
        await coordinator.async_request_refresh()

    async def handle_reload(call) -> None:
        """Handle the reload service call."""
        await hass.config_entries.async_reload(entry.entry_id)

    hass.services.async_register(DOMAIN, "aggiorna", handle_refresh)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload dell'integrazione."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

