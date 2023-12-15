from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    device_registry = await dr.async_get_registry(hass)

    # Create a switch for each device
    switches = []
    for device in device_registry.devices.values():
        if config_entry.entry_id in device.config_entries:
            switches.append(StateManagerEnabled(device, config_entry))
    async_add_entities(switches, True)

class StateManagerEnabled(SwitchEntity):
    def __init__(self, device, config_entry):
        self._device = device
        self._config_entry = config_entry
        self.entity_id = f"switch.{device.name}_enabled"
        self._state = False
        self._name = f"{device.name} Enabled"

    @property
    def unique_id(self):
        return self.entity_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device.id)},
            "name": self._name,
            "manufacturer": "Your Manufacturer",
            "model": "Your Model",
            "sw_version": "1.0",
            "via_device": (DOMAIN, self._device.id),
        }

    @property
    def is_on(self):
        return self._state

    @property
    def name(self):
        return self._name

    def turn_on(self, **kwargs):
        self._state = True
        self.async_write_ha_state()

    def turn_off(self, **kwargs):
        self._state = False
        self.async_write_ha_state()
