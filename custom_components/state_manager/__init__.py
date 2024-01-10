from .const import DOMAIN
import logging
import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity
from . import switch

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                cv.string: vol.Schema(
                    {
                        vol.Required("unique_id"): cv.string,
                    }
                )
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    """Set up the State Manager component."""
    for name, data in config[DOMAIN].items():
        unique_id = data["unique_id"]

        # Create the switch entity using the function from switch.py
        switch_entity = switch.create_switch_entity(hass, name, unique_id)

        hass.data[DOMAIN][unique_id] = switch_entity

    return True

    return True



