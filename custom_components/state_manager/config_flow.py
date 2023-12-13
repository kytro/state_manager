from homeassistant import config_entries

class StateManagerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="State Manager", data=user_input)
        return self.async_show_form(step_id="user")
