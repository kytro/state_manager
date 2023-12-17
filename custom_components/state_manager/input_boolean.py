from homeassistant.components import input_boolean
from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_DEVICES
from homeassistant.helpers import config_validation as cv
from homeassistant.components.light import PLATFORM_SCHEMA
from .const import DOMAIN

import voluptuous as vol

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES): vol.All(cv.ensure_list, [cv.string]),
})

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the platform."""
    devices = config.get(CONF_DEVICES)
    entities = [StateManagerEnabled(device) for device in devices]
    async_add_entities(entities, True)

class StateManagerEnabled(Entity):

    def __init__(self, hass, device):
        self.entity_id = f"input_boolean.{device.name}_enabled"
        self.device = device
        self.hass = hass

    @property
    def unique_id(self):
        return self._attr_unique_id

    @unique_id.setter
    def unique_id(self, unique_id):
        self._attr_unique_id = unique_id

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
