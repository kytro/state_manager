import voluptuous as vol
from homeassistant import config_entries, core, exceptions
from homeassistant.const import CONF_NAME, CONF_ID
from homeassistant.helpers import config_validation as cv

from . import DOMAIN


_LOGGER = logging.getLogger(__name__)
DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME, default="Device Name"): cv.string,
    vol.Required(CONF_ID, default="Device ID"): cv.string,
})

async def validate_input(hass: core.HomeAssistant, data):
    # TODO: validate the user input
    _LOGGER.info(f"Validating user input: {data}")
    return {"title": data[CONF_NAME]}

class StateManagerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                _LOGGER.info(f"Creating new entry: {info}")
                return self.async_create_entry(title=info["title"], data={"devices": [user_input]})
            except exceptions.HomeAssistantError:
                errors["base"] = "unknown_error"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
