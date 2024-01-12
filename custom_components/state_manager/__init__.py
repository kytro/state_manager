import logging
from asyncio import async_create_task

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    _LOGGER.info("Setting up Porch Light Manager component")

    try:
        await async_create_task(hass.components.frontend.async_register_built_in_panel(
            "iframe",
            "porch_light_manager",
            "Porch Light Manager",
            "/api/hassio/app/entrypoint.js",
            {"entrypoint": "entrypoint.js"},
        ))

        await async_create_task( hass.services.async_register(DOMAIN, "set_porch_light_manager_enabled", set_porch_light_manager_enabled))

        # Create the input boolean entity
        hass.states.async_set("input_boolean.porch_light_manager_enabled", "off")
        _LOGGER.info("Input boolean 'porch_light_manager_enabled' created successfully")

        return True

    except Exception as e:
        _LOGGER.error("Failed to set up Porch Light Manager component: %s", e)
        return False
    
async def set_porch_light_manager_enabled(call):
    """Service to set the porch light manager enabled state."""
    # Get the desired state from the service call data
    enabled = call.data.get("enabled", True)

    try:
        # Set the input boolean state
        hass.states.async_set("input_boolean.porch_light_manager_enabled", str(enabled))

        _LOGGER.info("Porch light manager enabled state set to: %s", enabled)
    except Exception as e:
        _LOGGER.error("Failed to set porch light manager enabled state: %s", e)