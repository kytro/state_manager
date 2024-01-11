import logging
from .const import DOMAIN
from homeassistant.components.input_boolean import async_setup_platform
from homeassistant.const import CONF_NAME, CONF_ICON
from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.components.input_boolean import DOMAIN as INPUT_BOOLEAN_DOMAIN
from homeassistant.helpers.entity_component import EntityComponent

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    # Create a new EntityComponent named 'input_boolean'
    component = EntityComponent(_LOGGER, INPUT_BOOLEAN_DOMAIN, hass)

    # Define the configuration for the input boolean
    switch_config = {
        'name': "Porch Light Manager Enabled",
        'initial': False,
        'icon': "mdi:lightbulb",
    }

    # Create a new input boolean entity
    entity = await component.async_add_entity(switch_config)

    # If the entity was created successfully, set its state
    if entity:
        hass.states.async_set(entity.entity_id, 'off', {
            'friendly_name': switch_config['name'],
            'icon': switch_config['icon'],
        })

    return True