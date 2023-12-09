# Import necessary libraries
import homeassistant.helpers.entity as entity
from homeassistant.components.input_boolean import InputBoolean
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
        self.entity_id = f"state_manager.{name}"
        self._enabled = False

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name

    @property
    def state(self):
        """Return the current state of the entity."""
        return self._state

    @property
    def state_attributes(self):
        """Return the state attributes of the entity."""
        return {"enabled": self._enabled}

    def set_state(self, new_state):
        """Set the state of the entity."""
        self._state = new_state
        self.schedule_update_ha_state()

    def toggle_enabled(self):
        """Toggle the 'enabled' status of the entity."""
        self._enabled = not self._enabled
        self.schedule_update_ha_state()

class EnabledToggle(InputBoolean):
    def __init__(self, state_manager_entity):
        """Initialize the toggle."""
        self._state_manager_entity = state_manager_entity
        self.entity_id = f"{state_manager_entity.entity_id}_enabled"

    @property
    def name(self):
        """Return the name of the toggle."""
        return f"{self._state_manager_entity.name} Enabled"

    @property
    def is_on(self):
        """Return true if the toggle is on."""
        return self._state_manager_entity._enabled

    def turn_on(self, **kwargs):
        """Turn the toggle on."""
        if not self._state_manager_entity._enabled:
            self._state_manager_entity.toggle_enabled()
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the toggle off."""
        if self._state_manager_entity._enabled:
            self._state_manager_entity.toggle_enabled()
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
        state_manager_entity = StateManagerEntity(hass, name)
        hass.data[DOMAIN].append(state_manager_entity)

        # Add the state manager entity to the Home Assistant state machine
        hass.states.async_set(state_manager_entity.entity_id, state_manager_entity.state)

        # Create an enabled toggle for the state manager entity
        enabled_toggle = EnabledToggle(state_manager_entity)

        # Add the enabled toggle to the Home Assistant state machine
        hass.states.async_set(enabled_toggle.entity_id, enabled_toggle.state)

    return True

# Setup and expose the component
async_setup_entry = async_setup
