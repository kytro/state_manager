import logging
from homeassistant.components.input_boolean import InputBoolean

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the State Manager platform."""
    add_entities([StateManager(config.get('name'))])

class StateManager(InputBoolean):
    """Representation of a State Manager."""

    def __init__(self, name):
        """Initialize the State Manager."""
        self.entity_id = "input_boolean." + name + "_enabled"
        self._name = name + "_enabled"
        self._state = False
        _LOGGER.info("Initialized input_boolean: %s", self._name)

    @property
    def name(self):
        """Return the name of the input boolean."""
        return self._name

    @property
    def is_on(self):
        """Return true if the input boolean is enabled."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the input boolean on."""
        self._state = True
        self.schedule_update_ha_state()
        _LOGGER.info("Turned on input_boolean: %s", self._name)

    def turn_off(self, **kwargs):
        """Turn the input boolean off."""
        self._state = False
        self.schedule_update_ha_state()
        _LOGGER.info("Turned off input_boolean: %s", self._name)