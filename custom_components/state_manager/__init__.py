"""The state_manager component."""
from homeassistant.helpers import discovery

DOMAIN = "state_manager"

def setup(hass, config):
    """Set up the state_manager component."""
    hass.data[DOMAIN] = {}
    discovery.load_platform(hass, "input_boolean", DOMAIN, {}, config)
    return True
