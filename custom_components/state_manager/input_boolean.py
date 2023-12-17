from homeassistant.components.input_boolean import InputBoolean
from .const import DOMAIN

async def async_setup(hass, config):
    # Create an input_boolean
    input_boolean_entity_id = f"input_boolean.{hass.data[DOMAIN]}_enabled"
    await hass.services.async_call('input_boolean', 'create', {
        'entity_id': input_boolean_entity_id
    })

    return True
