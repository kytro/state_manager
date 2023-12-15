from .const import DOMAIN

async def async_setup(hass, config):
    # Initialization of your component.
    hass.data[DOMAIN] = config[DOMAIN]['name']
    return True
