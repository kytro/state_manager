import logging
import voluptuous as vol
from homeassistant.helpers.entity import Entity
from homeassistant.helpers import config_validation as cv

_LOGGER = logging.getLogger(__name__)
DOMAIN = 'state_manager'

DEVICE_SCHEMA = vol.Schema({
    vol.Required('name'): cv.string,
    vol.Required('id'): cv.string,
})

CONFIG_SCHEMA = vol.Schema({
    vol.Required('state_manager'): vol.Schema({
        vol.Required('devices'): vol.All(cv.ensure_list, [DEVICE_SCHEMA])
    })
}, extra=vol.ALLOW_EXTRA)


class StateManager(Entity):
    def __init__(self, name, id):
        self._name = name
        self._id = id
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
    devices = config[DOMAIN]['devices']
    for device in devices:
        hass.states.async_set(device['id'], 'off')
    return True
