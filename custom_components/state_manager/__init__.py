from homeassistant.components.input_boolean import async_setup as async_setup_input_boolean
from .const import DOMAIN

async def async_setup(hass, config):

    input_boolean_config = {
        "unique_id": "porch_light_managed_enabled",
        "name": "Porch Light Managed Enabled",
        "initial": True,
    }
    
    await async_setup_input_boolean(hass, input_boolean_config)    

    return True
