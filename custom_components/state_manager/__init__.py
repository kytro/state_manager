from typing import List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import EntityPlatform

DOMAIN = "state_manager"

class StateManagerPlatform(EntityPlatform):

    def __init__(self, hass: HomeAssistant):
        super().__init__(hass)
        self._devices: List[StateManagerDevice] = []

    async def async_setup(self, config_entry: ConfigEntry, async_add_entities):
        for device_config in config_entry.data:
            device = StateManagerDevice(self, device_config["name"])
            self._devices.append(device)
            async_add_entities([device])
        return True


class StateManagerDevice(Entity):

    def __init__(self, platform: StateManagerPlatform, name: str):
        self.platform = platform
        self._name = name
        self._expected_state = True

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._expected_state

    @property
    def unique_id(self):
        return f"state_manager_{self._name}"

    @property
    def device_info(self):
        return {
            "identifiers": {("state_manager", self._name)},
            "manufacturer": "Custom Component Example",
            "model": "State Manager Device",
            "name": self._name,
        }

    @property
    def should_poll(self):
        return False

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.platform.hass.async_create_task(self.update_expected_state())

    async def update_expected_state(self):
        # Replace this with your logic for updating expected state
        self._expected_state = True
        self.async_schedule_update_ha_state()

async def async_setup(hass: HomeAssistant, config: dict):
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    platform = StateManagerPlatform(hass)
    hass.data[DOMAIN][entry.entry_id] = platform
    await platform.async_setup(entry)
    return True