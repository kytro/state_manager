import logging
import voluptuous as vol

import homeassistant.helpers.config_validation as cv

from homeassistant.helpers import discovery
from homeassistant.helpers.template import Template


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
                    vol.Required('expected_state'): cv.string,
                })]),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

class StateManager:
    def __init__(self, hass, name, unique_id, target_entity_id, expected_state):
        self.hass = hass
        self.name = name
        self.unique_id = unique_id
        self.target_entity_id = target_entity_id
        self._expected_state = expected_state
        self.expected_state_template = Template(expected_state, hass)

    @property
    def expected_state(self):
        """Return the expected state after rendering the template."""
        return self.expected_state_template.async_render()

    @expected_state.setter
    def expected_state(self, value):
        """Ignore attempts to set this property."""
        pass

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self.name,
            "model": "State Manager",
            "manufacturer": "State Manager",
        }

def setup(hass, config):
    """Set up the state_manager component."""
    try:
        devices = config[DOMAIN][CONF_DEVICES]

        if DOMAIN not in hass.data:
            hass.data[DOMAIN] = {}

        for device in devices:
            """Adding device: {device['id']}..."""
            _LOGGER.info("Adding device: %s...", device['id'])
            manager = StateManager(hass, device['id'], device['id'], device['target_entity_id'], device['expected_state'])
            hass.data[DOMAIN][device['id']] = manager

            # Load the switch platform with the current devices
            discovery.load_platform(
                hass,
                "switch",
                DOMAIN,
                {"device_info": device.device_info},
                config,
            )

            discovery.load_platform(
                hass,
                "sensor",
                DOMAIN,
                {"device_info": device.device_info},
                config,
            )

        return True  # Return True if setup was successful
    except Exception as e:
        _LOGGER.error("Error setting up state_manager: %s", e)
        return False  # Return False if there was an error
