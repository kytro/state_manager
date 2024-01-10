"""Platform for input_boolean integration."""
from homeassistant.components.input_boolean import InputBoolean

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the input_boolean platform."""
    entities = []
    for name in discovery_info:
        entities.append(StateManagerInputBoolean(name))
    add_entities(entities, True)

class StateManagerInputBoolean(InputBoolean):
    """Representation of a State Manager Input Boolean."""

    def __init__(self, name):
        """Initialize the State Manager Input Boolean."""
        self._name = name + "_enabled"
        self._state = False

    @property
    def name(self):
        """Return the name of the input boolean."""
        return self._name

    @property
    def is_on(self):
        """Return true if the input boolean is enabled."""
        return self._state
