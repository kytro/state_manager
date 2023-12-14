from typing import Any

from homeassistant.config_entries import ConfigFlow


class StateManagerConfigFlow(ConfigFlow, domain="state_manager"):

    async def async_step_user(self, user_input: Any = None):
        if user_input is None:
            return self.show_form(step_id="user")

        return self.async_create_entry(
            title=user_input["name"], data={"name": user_input["name"]}
        )

    async def async_step_import(self, config: Any):
        return self.async_create_entry(
            title=config["name"], data={"name": config["name"]}
        )

    async def async_step_config(self, config: Any = None):
        return await self.async_step_user(config)

