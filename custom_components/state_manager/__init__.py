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

def setup(hass, config):
    """Set up the state_manager component."""
    devices = config[DOMAIN][CONF_DEVICES]

    for device in devices:
        discovery.load_platform(hass, "switch", DOMAIN, {"device": device}, config)

    return True