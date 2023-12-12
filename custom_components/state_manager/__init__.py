import logging
import voluptuous as vol

import homeassistant.helpers.config_validation as cv

from homeassistant.helpers import discovery

from homeassistant.helpers.entity import DeviceInfo, Entity
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

class StateManager(Entity):
    def __init__(self, hass, name, unique_id, device_id, target_entity_id, expected_state):
        self.hass = hass
        self.name = name
        self.unique_id = unique_id
        self.device_id = device_id
        self.target_entity_id = target_entity_id
        self._expected_state = expected_state
        self.expected_state_template = Template(expected_state, hass)
        
        self.attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.device_id)},
            manufacturer="State Manager",
            name=self.device_name,
            model="State Manager",

        )
       
    @property
    def expected_state(self):
        """Return the expected state after rendering the template."""
        return self.expected_state_template.async_render()

    @expected_state.setter
    def expected_state(self, value):
        """Ignore attempts to set this property."""
        pass

    @property
    def device_info(self) -> DeviceInfo:
        """Return device registry information for this entity."""
        _LOGGER.info("Device info: %s", self.attr_device_info)
        return self.attr_device_info

def setup(hass, config):
    """Set up the state_manager component."""
    try:
        devices = config[DOMAIN][CONF_DEVICES]

        if DOMAIN not in hass.data:
            hass.data[DOMAIN] = {}

        for device in devices:
            _LOGGER.info("Adding device: %s...", device['id'])
            manager = StateManager(hass, device['id'], device['id'], device['id'], device['target_entity_id'], device['expected_state'])
            hass.data[DOMAIN][device['id']] = manager

            # Load the switch platform with the current device
            discovery.load_platform(
                hass,
                "switch",
                DOMAIN,
                {"device_info": manager.device_info},
                config,
            )

            # Load the sensor platform with the current device
            discovery.load_platform(
                hass,
                "sensor",
                DOMAIN,
                {"device_info": manager.device_info},
                config,
            )

        return True  # Return True if setup was successful
    except Exception as e:
        _LOGGER.error("Error setting up state_manager: %s", e)
        return False  # Return False if there was an error
