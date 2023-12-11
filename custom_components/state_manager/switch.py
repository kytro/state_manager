import logging

from . import DOMAIN

from homeassistant.components.switch import SwitchEntity

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the State Manager switch."""
    devices = hass.data["state_manager"]
    switches = [StateManagerSwitch(device) for device in devices.values()]
    add_entities(switches, True)

class StateManagerSwitch(SwitchEntity):
    def __init__(self, device):
        """Initialize the switch."""
        self._device = device
        self._state = False

        # Add the device to the device registry
        self._device.device_registry.async_get_or_create(
            identifiers={(DOMAIN, self._device.unique_id)},
            name=self._device.name,
        )

    @property
    def name(self):
        """Return the name of the switch."""
        return f"{self._device.name} Enabled"

    @property
    def unique_id(self):
        """Return the unique ID of the switch."""
        return self._device.unique_id

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._state = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._state = False
        self.schedule_update_ha_state()
