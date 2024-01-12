import logging
from datetime import timedelta

from homeassistant.helpers.entity_component import EntityComponent
from .const import DOMAIN, SERVICE_DONE

ENTITY_ID_FORMAT = DOMAIN + ".{}"

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=86400)


async def async_setup(hass, config):
    component = hass.data[DOMAIN] = EntityComponent(
        _LOGGER, DOMAIN, hass, SCAN_INTERVAL
    )

    await component.async_setup(config)

    component.async_register_entity_service(
        SERVICE_DONE, {}, "done",
    )

    return True


async def async_setup_entry(hass, entry):
    return await hass.data[DOMAIN].async_setup_entry(entry)


async def async_unload_entry(hass, entry):
    return await hass.data[DOMAIN].async_unload_entry(entry)