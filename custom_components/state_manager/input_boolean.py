from homeassistant.components import input_boolean
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

class StateManagerEnabled(input_boolean.InputBoolean):

    def __init__(self, hass, device):
        super().__init__(hass, f"input_boolean.{device.name}_enabled")
        self.device = device

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.device.id)},
            "name": f"{self.device.name} Enabled",
            "manufacturer": "Your Manufacturer",
            "model": "Your Model",
            "sw_version": "1.0",
            "via_device": (DOMAIN, self.device.id),
        }

    @property
    def icon(self):
        return "mdi:toggle-switch"  # Replace with desired icon

    def update_state(self, state):
        self._state = state
        self.async_write_ha_state()

    def configure_entity(self, hass, config_entry, options=None):
        super().configure_entity(hass, config_entry, options=options)
        # ... additional configuration based on options (optional) ...
