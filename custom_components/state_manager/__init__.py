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
                vol.Required(CONF_DEVICES): vol.All(cv.ensure_list, [vol.Schema({
                    vol.Required('id'): cv.string,
                    vol.Required('target_entity_id'): cv.string,
                })]),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)



class StateManager:
    def __init__(self, name, unique_id, target_entity_id):
        self.name = name
        self.unique_id = unique_id
        self.target_entity_id = target_entity_id

def setup(hass, config):
    """Set up the state_manager component."""
    try:
        devices = config[DOMAIN][CONF_DEVICES]

        if DOMAIN not in hass.data:
            hass.data[DOMAIN] = {}

        for device in devices:
            """Adding device: {device['id']}..."""
            _LOGGER.info("Adding device: %s...", device['id'])
            manager = StateManager(device['id'], device['id'], device['target_entity_id'])
            hass.data[DOMAIN][device['id']] = manager

        # Load the switch platform with the current devices
        discovery.load_platform(hass, 'switch', DOMAIN, {}, config)

        return True  # Return True if setup was successful
    except Exception as e:
        _LOGGER.error("Error setting up state_manager: %s", e)
        return False  # Return False if there was an error
