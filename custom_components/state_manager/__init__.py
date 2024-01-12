"""The state_manager component."""
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import CONF_NAME
from homeassistant.components.input_boolean import DOMAIN as INPUT_BOOLEAN

DOMAIN = "state_manager"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_NAME): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    """Set up the state_manager component."""
    conf = config[DOMAIN]

    # Ensure the platform is loaded
    hass.async_create_task(
        hass.helpers.discovery.async_load_platform(INPUT_BOOLEAN, DOMAIN, {}, config)
    )

    # Create the input_boolean
    hass.states.async_set(
        f"{INPUT_BOOLEAN}.{conf[CONF_NAME]}", "off", {"friendly_name": conf[CONF_NAME]}
    )

    return True