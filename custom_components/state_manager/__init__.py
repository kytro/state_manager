import logging
from homeassistant.helpers import discovery
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.const import CONF_DEVICES

_LOGGER = logging.getLogger(__name__)

DOMAIN = "state_manager"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_DEVICES): cv.ensure_list,
            }
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
    devices = config[DOMAIN][CONF_DEVICES]

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    for unique_id in devices:
        name = unique_id  # Modify this line if the name should be different from the unique_id
        manager = StateManager(name, unique_id)
        hass.data[DOMAIN][unique_id] = manager
        discovery.load_platform(hass, "switch", DOMAIN, {"manager": manager}, config)

    return True
