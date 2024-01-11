import logging
from homeassistant.components.input_boolean import (
    DOMAIN as INPUT_BOOLEAN_DOMAIN,
    InputBoolean,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up state_manager from a config entry."""
    name = config_entry.data["name"]
    enabled_name = f"{name}_enabled"

    input_boolean = InputBoolean(enabled_name, f"{name} Enabled")
    await input_boolean.async_add_to_hass(hass)

    async_add_entities([input_boolean])

    _LOGGER.info("State Manager input boolean '%s' created", enabled_name)

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
