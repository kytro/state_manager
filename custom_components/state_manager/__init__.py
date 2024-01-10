from .const import DOMAIN
import logging
import voluptuous as vol

from homeassistant.helpers.config_validation import (  # Updated import
    PLATFORM_SCHEMA,
    PLATFORM_SCHEMA_BASE,
)
from homeassistant.helpers.entity import Entity
from . import switch

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(  # Use PLATFORM_SCHEMA for validation
    {
        vol.Required("name"): vol.All(str, vol.Length(min=1)),
        vol.Required("unique_id"): str,
    }
)

async def async_setup(hass, config):
    """Set up the State Manager component."""
    for name, data in config[DOMAIN].items():
        unique_id = data["unique_id"]

        # Create the switch entity using the function from switch.py
        switch_entity = switch.create_switch_entity(hass, name, unique_id)

        hass.data[DOMAIN][unique_id] = switch_entity

    return True


