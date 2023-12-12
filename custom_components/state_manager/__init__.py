import logging
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)
DOMAIN = 'state_manager'

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

async def async_setup_entry(hass, config_entry):
    _LOGGER.info("Setting up state_manager")
    # Set up your component here
    devices = config_entry.data['devices']
    for device in devices:
        hass.states.async_set(device['id'], 'off')
    return True
