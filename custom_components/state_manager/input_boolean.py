from homeassistant.components import input_boolean
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

class StateManagerEnabled(Entity):
    def __init__(self, hass, device):
        self.hass = hass
        self.device = device
        self.entity_id = f"input_boolean.{device.name}_enabled"
        self._state = 'off'
        self._name = f"{device.name} Enabled"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.device.id)},
            "name": self._name,
            "manufacturer": "Your Manufacturer",
            "model": "Your Model",
            "sw_version": "1.0",
            "via_device": (DOMAIN, self.device.id),
        }

    @property
    def state(self):
        return self._state

    @property
    def name(self):
        return self._name

    def update_state(self, state):
        self._state = state
        self.async_write_ha_state()
