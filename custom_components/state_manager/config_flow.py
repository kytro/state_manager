from homeassistant import config_entries
from .const import DOMAIN
import voluptuous as vol

class CustomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_UNKNOWN

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id='user',
                data_schema=vol.Schema({vol.Required('name'): str}),
            )

        return self.async_create_entry(
            title=user_input['name'],
            data=user_input,
        )
