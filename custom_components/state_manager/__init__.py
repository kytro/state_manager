import logging
from homeassistant.helpers import discovery
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.const import CONF_DEVICES, CONF_NAME

_LOGGER = logging.getLogger(__name__)

DOMAIN = "state_manager"

DEVICE_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
})

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            vol.All(dict, {cv.string: DEVICE_SCHEMA}),
        )
    },
    extra=vol.ALLOW_EXTRA,
)

class StateManager:
    def __init__(self, name, unique_id):
        self.name = name
        self.unique_id = unique_id

def setup(hass, config):
    """Set up the state_manager component."""
    devices = config[DOMAIN]

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    for unique_id, device_config in devices.items():
        """Adding device: {unique_id}..."""
        _LOGGER.info("Adding device: %s...", unique_id)
        name = device_config[CONF_NAME]
        manager = StateManager(name, unique_id)
        hass.data[DOMAIN][unique_id] = manager
        discovery.load_platform(
            hass,
            "input_boolean",
            DOMAIN,
            {"manager": manager, "device_name": name},
            config,
        )

    return True
