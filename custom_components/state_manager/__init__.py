"""Home Assistant custom integration."""
import logging

from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([BathroomLightSensor(hass)])

class BathroomLightSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self._state = None
        self.hass = hass

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Bathroom Light'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor."""
        self._state = self.hass.states.get('light.bathroom').state == 'on'
