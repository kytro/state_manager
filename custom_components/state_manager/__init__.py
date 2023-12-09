"""The state_manager component."""
import logging
import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.restore_state import RestoreEntity


_LOGGER = logging.getLogger(__name__)

DOMAIN = "state_manager"

CONFIG_SCHEMA = vol.Schema(
    {vol.Optional(DOMAIN): vol.Schema({})}, extra=vol.ALLOW_EXTRA
)

class StateManager(Entity):

    def __init__(self, hass, config):
        """Initialize My Device."""
        self.hass = hass
        self._name = config["name"]
        self._entity_id = config["entity_id"]
        self._related_entity_id = config["related_entity"]["entity_id"]
        self._expected_state = config["related_entity"]["expected_state"]
        self._enabled = False
        _LOGGER.debug(f"Created entity {self._entity_id} with enabled state {self._enabled}")

    async def async_added_to_hass(self):
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()
        # Use the async_get_last_state method of the RestoreEntity class
        state = await self.async_get_last_state()
        if state:
            self._enabled = state.state == 'on'

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
        # Here you can check the state of the related entity and return the state of My Device
        return None

    @property
    def is_enabled(self):
        """Return whether My Device is enabled."""
        return self._enabled.state

    def update(self):
        """Update the state of My Device."""
        # Here you can check the state of the related entity and update the state of My Device
        pass

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the state_manager component."""
    _LOGGER.info("Setting up state_manager")

    # Get the devices from the configuration
    devices = config[DOMAIN].values()

    _LOGGER.info("Devices")

    # Create a StateManager entity for each device
    entities = [StateManager(hass, device) for device in devices]

    # Log the number of entities created
    _LOGGER.debug(f"Created {len(entities)} entities")

    # Create an EntityComponent
    component = EntityComponent(_LOGGER, DOMAIN, hass)

    # Add the entities to the component
    await component.async_add_entities(entities)

    return True


