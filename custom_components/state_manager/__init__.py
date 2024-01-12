"""The state_manager component."""
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import CONF_FRIENDLY_NAME
from homeassistant.components.input_boolean import DOMAIN as INPUT_BOOLEAN
from homeassistant.helpers.entity_platform import async_get_platforms
from homeassistant.util import slugify
from homeassistant.components.input_boolean import async_setup as setup_input_boolean


DOMAIN = "state_manager"

COMPONENT_INPUT_BOOLEAN = 'input_boolean'

CONFIG_INPUT_BOOLEAN = {}

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

    # Get the input_boolean platform
    platform = None
    for p in async_get_platforms(hass, INPUT_BOOLEAN):
        if p.domain == INPUT_BOOLEAN:
            platform = p
            break

    # Create the input_boolean for each entity in the configuration
    for entity_id, entity_conf in conf.items():
        await create_input_boolean(f"{entity_id}_enabled")

    await setup_input_boolean(hass, {COMPONENT_INPUT_BOOLEAN: CONFIG_INPUT_BOOLEAN})

    return True


async def create_input_boolean(name: str, icon=None) -> str:
    data = {
        'name': name
    }

    if icon:
        data['icon'] = icon

    internal_name = slugify(name)

    CONFIG_INPUT_BOOLEAN[internal_name] = data

    global CUSTOM_INPUT_BOOLEAN
    CUSTOM_INPUT_BOOLEAN = True

    return 'input_boolean.{}'.format(internal_name)