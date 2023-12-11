import logging

from . import DOMAIN

from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the State Manager sensor."""
    _LOGGER.info("Setting up State Manager sensor")
    devices = hass.data["state_manager"]
    sensors = [StateManagerSensor(device) for device in devices.values()]
    add_entities(sensors, True)

class StateManagerSensor(Entity):
    def __init__(self, device):
        """Initialize the sensor."""
        self._device = device

        # Add the device to the device registry
        self._device.device_registry.async_get_or_create(
            identifiers={(DOMAIN, self._device.unique_id)},
            name=self._device.name,
            via_device=(DOMAIN, "state_manager")  
        )

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._device.name} Expected State"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.hass.states.is_state(self._device.target_entity_id, self._device.expected_state)
