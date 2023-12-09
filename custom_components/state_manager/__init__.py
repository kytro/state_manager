# Import necessary libraries
import homeassistant.helpers.entity as entity
from homeassistant.const import (
    STATE_UNKNOWN,
)


# Define custom domain
DOMAIN = "state_manager"


# Define a custom entity class for the state manager
class StateManagerEntity(entity.Entity):

    def __init__(self, hass, name):
        """Initialize a StateManagerEntity."""
        self.hass = hass
        self._name = name
        self._state = STATE_UNKNOWN

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name

    @property
    def state(self):
        """Return the current state of the entity."""
        return self._state

    def set_state(self, new_state):
        """Set the state of the entity."""
        self._state = new_state
        self.schedule_update_ha_state()


# Define the configuration schema for the component
async def async_setup(hass, config):
    """Set up the state_manager component."""
    # Get the list of names from the configuration
    names = config[DOMAIN].get("names", [])

    # Initialize hass.data[DOMAIN] as an empty list
    hass.data[DOMAIN] = []

    # Create entities for each name
    for name in names:
        entity = StateManagerEntity(hass, name)
        hass.data[DOMAIN].append(entity)

    return True

# Setup and expose the component
async_setup_entry = async_setup
