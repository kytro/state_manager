"""The state_manager component."""
import logging
import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.restore_state import async_get_last_state


_LOGGER = logging.getLogger(__name__)

DOMAIN = "state_manager"

CONFIG_SCHEMA = vol.Schema(
    {vol.Optional(DOMAIN): vol.Schema({})}, extra=vol.ALLOW_EXTRA
)

class StateManager(Entity):
    """Representation of My Device."""

    def __init__(self, hass, config):
        """Initialize My Device."""
        self.hass = hass
        self._name = config["name"]
        self._entity_id = config["entity_id"]
        self._related_entity_id = config["related_entity"]["entity_id"]
        self._expected_state = config["related_entity"]["expected_state"]
        self._enabled = False

    async def async_added_to_hass(self):
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()
        state = await async_get_last_state(self.hass, self.entity_id)
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
    return True
