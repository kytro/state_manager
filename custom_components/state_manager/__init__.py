from homeassistant.components.input_boolean import InputBoolean
from .const import DOMAIN

async def async_setup(hass, config):

    input_boolean = InputBoolean("porch_light_managed_enabled", "Porch Light Managed Enabled")
    
    hass.async_create_task(hass.helpers.entity_component.async_add_entities([input_boolean]))   

    return True
