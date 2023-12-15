from homeassistant.helpers import device_registry as dr
from .switch import async_setup_platform
from .const import DOMAIN

async def async_setup_entry(hass, entry):
    hass.data[DOMAIN] = entry.data['name']

    # Forward the setup to the switch platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "switch")
    )

    return True
