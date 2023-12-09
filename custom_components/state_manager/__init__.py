"""The state_manager component."""
import logging
import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.restore_state import RestoreEntity


_LOGGER = logging.getLogger(__name__)

DOMAIN = "state_manager"

# Define the schema for the related_entity configuration
RELATED_ENTITY_SCHEMA = vol.Schema({
    vol.Required("entity_id"): cv.string,
    vol.Required("expected_state"): cv.string,
})

# Define the schema for the device configuration
DEVICE_SCHEMA = vol.Schema({
    vol.Required("name"): cv.string,
    vol.Required("entity_id"): cv.string,
    vol.Required("related_entity"): cv.validate_config(RELATED_ENTITY_SCHEMA),
})

# Define the schema for the state_manager configuration
STATE_MANAGER_SCHEMA = vol.Schema({
    DOMAIN: vol.All(cv.ensure_list, [DEVICE_SCHEMA])
})

CONFIG_SCHEMA = STATE_MANAGER_SCHEMA


class StateManager(Entity, RestoreEntity):

    def __init__(self, hass, config):
        """Initialize My Device."""
        super().__init__()
        self.hass = hass
        self._name = config["name"]
        self._entity_id = config["entity_id"]
        self._related_entity_id = config["related_entity"]["entity_id"]
        self._expected_state = config["related_entity"]["expected_state"]
        self._enabled = False

    async def async_added_to_hass(self):
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()

        # Restore state
        state = await self.async_get_last_state()
        if state:
            self._enabled = state.state == "on"

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def name(self):
        """Return the name of My Device."""
        return self._name

    @property
    def state(self):
        """Return the state of My Device."""
        # Update state if needed
        self.update()
        return "on" if self._enabled else "off"

    @property
    def is_enabled(self):
        """Return whether My Device is enabled."""
        return self._enabled

    def update(self):
        """Update the state of My Device."""
        related_state = self.hass.states.get(self._related_entity_id)

        if related_state:
            self._enabled = related_state.state == self._expected_state

        self.async_schedule_update_ha_state()

    async def async_restore_last_state(self, last_state):
        """Restore previous state."""
        self._enabled = last_state.state == "on"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the state_manager component."""
    _LOGGER.info("Setting up state_manager")

    # Get the devices from the configuration
    devices = config[DOMAIN]

    # Create a StateManager entity for each device
    entities = [StateManager(hass, device) for device in devices]

    # Log the number of entities created
    _LOGGER.debug(f"Created {len(entities)} entities")

    # Add the entities to Home Assistant
    hass.add_job(hass.helpers.entity_component.async_add_entities, entities)

    return True
