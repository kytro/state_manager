from homeassistant.helpers.entity import Entity

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([StateManagerSensor()])

class StateManagerSensor(Entity):
    @property
    def state(self):
        return "boo"
