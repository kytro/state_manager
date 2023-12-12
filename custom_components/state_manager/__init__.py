import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers import config_validation as cv

_LOGGER = logging.getLogger(__name__)
DOMAIN = 'state_manager'

DEVICE_SCHEMA = vol.Schema({
    vol.Required('name'): cv.string,
    vol.Required('id'): cv.string,
})

class StateManager(Entity):
    def __init__(self, name, id):
        self._name = name
        self._id = id
        self._state = None
        self._device_info = DeviceInfo(
            identifiers = {(DOMAIN, id)},
            name = name,
            manufacturer = "State Manager",
            model = "State Manager",
        )
        _LOGGER.info(f"Device created: {self._name}")

    @property
    def unique_id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def device_info(self):
        return self._device_info

    @property
    def state(self):
        return self._state

    async def async_update(self):
        _LOGGER.info("Updating state")
        # Update the state of your entity here

class StateManagerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # TODO: process user_input and add new device
            _LOGGER.info(f"New device added: {user_input['name']}")
            return self.async_create_entry(title="New Device", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=DEVICE_SCHEMA
        )

async def async_setup(hass, config):
    hass.config_entries.async_register_flow(DOMAIN, "StateManager", StateManagerConfigFlow)
    _LOGGER.info("Setting up state_manager")
    # Set up your component here
    devices = config[DOMAIN]['devices']
    for device in devices:
        hass.states.async_set(device['id'], 'off')
    return True
