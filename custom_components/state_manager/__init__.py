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
    _LOGGER.info("Setting up the State Manager component")

    hass.data[DOMAIN] = {}  # Initialize hass.data[DOMAIN] as a dictionary

    for name, data in config[DOMAIN].items():
        # Append '_enabled' to the name
        switch_name = name + "_enabled"
        unique_id = data["unique_id"] + "_enabled"

        # Create the switch entity using the function from switch.py
        switch_entity = switch.create_switch_entity(hass, switch_name, unique_id)

        hass.data[DOMAIN][unique_id] = switch_entity
        _LOGGER.info(f"Created switch entity: {switch_name} with unique_id: {unique_id}")

    return True

