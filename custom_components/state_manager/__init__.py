from homeassistant.helpers import device_registry as dr
from .const import DOMAIN
from .input_boolean import StateManagerEnabled
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from homeassistant.const import (
    Platform,
)

PLATFORMS: list[Platform] = [Platform.SWITCH]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data[DOMAIN] = {entry.data['name']: {}}

    device_registry = dr.async_get(hass)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "devices": device_registry.devices
        }

    device = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, (entry.entry_id, "_device"))},
        name=entry.data['name'],
        manufacturer="Your Device Manufacturer",
        model="Your Device Model",
        sw_version="Your Device Software Version"
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True
