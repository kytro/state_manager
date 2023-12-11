
Unfortunately, I can't provide an updated init file without the complete configuration and the specific line number where the error occurs. However, I can offer some general guidance on how to update your init file based on the information provided:

1. Loop through individual devices:

Make sure your loop iterates through the actual list of devices within the devices configuration variable. Use the following syntax:

Python
for device in devices:
    # ...
Use code with caution. Learn more
2. Access device_info attribute:

Within the loop, ensure you access the device_info attribute of the current device object, not the devices dictionary or any temporary variables. Use the following syntax:

Python
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
Use code with caution. Learn more
3. Update line 92:

Specifically address the issue at line 92, which might be related to accessing the device_info attribute incorrectly. Ensure the code around this line aligns with the recommended solutions above.

4. Restart Home Assistant:

After making changes to your init file, restart Home Assistant for the changes to take effect.

Here's an example of an updated init file based on the information provided:

Python
import logging
import voluptuous as vol

import homeassistant.helpers.config_validation as cv

from homeassistant.helpers
 
import discovery
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

      # Load the switch platform with the current device
      discovery.load_platform(
        hass,
        "switch",
        DOMAIN,
        {"device_info": device.device_info},
        config,
      )

      # Load the sensor platform with the current device
      discovery.load_platform(
        hass,
        "sensor",
        DOMAIN,
        {"device_info": device.device_info},
        config,
      )

    return True # Return True if setup