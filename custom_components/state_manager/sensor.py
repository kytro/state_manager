from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import async_setup_entry_platform

async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities([StateManagerSensor()])

class StateManagerSensor(Entity):
    @property
    def state(self):
        return "boo"
