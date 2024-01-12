from logging import getLogger

from voluptuous import Required, Schema

from homeassistant.components.automation import EVENT_AUTOMATION_RELOADED
from homeassistant.const import CONF_ENTITY_ID, CONF_STATE, EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import HomeAssistant, Event
from homeassistant.helpers.config_validation import string
from .helper import create_automations, create_entities_and_automations, CONFIG_INPUT_BOOLEAN, COMPONENT_INPUT_BOOLEAN, \
    CONFIG_INPUT_DATETIME, COMPONENT_INPUT_DATETIME, CONFIG_INPUT_NUMBER, COMPONENT_INPUT_NUMBER, CONFIG_INPUT_TEXT, \
    COMPONENT_INPUT_TEXT, CONFIG_TIMER, COMPONENT_TIMER

DOMAIN = 'auxiliary'

SCHEMA_SET_STATE = Schema(
    {
        Required(CONF_ENTITY_ID): string,
        Required(CONF_STATE): string
    }
)

_LOGGER = getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    CONFIG_INPUT_BOOLEAN.update(config.get(COMPONENT_INPUT_BOOLEAN, {}))
    CONFIG_INPUT_DATETIME.update(config.get(COMPONENT_INPUT_DATETIME, {}))
    CONFIG_INPUT_NUMBER.update(config.get(COMPONENT_INPUT_NUMBER, {}))
    CONFIG_INPUT_TEXT.update(config.get(COMPONENT_INPUT_TEXT, {}))
    CONFIG_TIMER.update(config.get(COMPONENT_TIMER, {}))

    async def handle_home_assistant_started_event(event: Event):
        await create_entities_and_automations(hass)

    async def handle_automation_reload_event(event: Event):
        await create_automations(hass)

    hass.bus.async_listen(EVENT_HOMEASSISTANT_STARTED, handle_home_assistant_started_event)
    hass.bus.async_listen(EVENT_AUTOMATION_RELOADED, handle_automation_reload_event)

    return True