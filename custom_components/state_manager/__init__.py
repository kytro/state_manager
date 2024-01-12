"""The state_manager component."""
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import CONF_FRIENDLY_NAME
from homeassistant.components.input_boolean import DOMAIN as INPUT_BOOLEAN

DOMAIN = "state_manager"

ENTITY_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_FRIENDLY_NAME): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {cv.slug: ENTITY_SCHEMA}
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

async def async_setup(hass, config):
    """Set up the state_manager component."""
    conf = config[DOMAIN]

    # Ensure the platform is loaded
    hass.async_create_task(
        hass.helpers.discovery.async_load_platform(INPUT_BOOLEAN, DOMAIN, {}, config)
    )

    # Create the input_boolean for each entity in the configuration
    for entity_id, entity_conf in conf.items():
        hass.states.async_set(
            f"{INPUT_BOOLEAN}.{entity_id}_enabled",
            "off",
            {"friendly_name": f"{entity_conf.get(CONF_FRIENDLY_NAME, entity_id)} Enabled"}
        )

    return True