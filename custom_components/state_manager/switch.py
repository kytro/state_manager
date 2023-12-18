import voluptuous as vol
from homeassistant.components.switch import (
    DOMAIN as SWITCH_DOMAIN,
    SwitchDeviceClass,
    SwitchEntity,
)

from .const import DOMAIN

class StateManagerEnabled(SwitchEntity):

    def __init__(self, hass, device):
        self._attr_name = f"{device.name} Enabled"
        self._attr_unique_id = f"{DOMAIN}_{device.id}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device.id)},
            "name": device.name,
            "manufacturer": device.manufacturer,
            "model": device.model,
            "sw_version": device.sw_version,
            "via_device": (DOMAIN, device.id),
        }
        self._attr_icon = "mdi:toggle-switch"  # Replace with desired icon
        self._attr_is_on = False
        self.device = device

    def turn_on(self, **kwargs):
        self._attr_is_on = True
        self.async_write_ha_state()

    def turn_off(self, **kwargs):
        self._attr_is_on = False
        self.async_write_ha_state()

    def configure_entity(self, hass, config_entry, options=None):
        # ... additional configuration based on options (optional) ...