import logging
import voluptuous as vol
from homeassistant import config_entries, core
from homeassistant.helpers.entity import Entity

from .const import (
    DOMAIN,
)

async def async_setup(hass: core.HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: core.HomeAssistant, config_entry: config_entries.ConfigEntry):
    hass.data[DOMAIN][config_entry.entry_id] = config_entry.data
    # Fix: forward entry setup to "sensor" platform
    await hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    return True

class StateManagerEntity(Entity):
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self.name,
            "manufacturer": "CustomComponent",
        }
