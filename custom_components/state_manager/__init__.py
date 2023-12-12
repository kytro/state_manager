import logging
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

class StateManager(Entity):
    def __init__(self, name):
        self._name = name
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_update(self):
        _LOGGER.info("Updating state")
        # Update the state of your entity here

async def async_setup(hass, config):
    _LOGGER.info("Setting up state_manager")
    # Set up your component here
    return True
