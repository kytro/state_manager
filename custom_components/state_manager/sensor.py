from homeassistant.helpers.entity import Entity

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    # Fix: call the correct setup method
    if "state_manager" in config:
        async_add_entities([StateManagerSensor(config["state_manager"])])
    return True

class StateManagerSensor(Entity):
    def __init__(self, config):
        self._config = config

    @property
    def state(self):
        # Use data from config if available
        return self._config.get("state", "boo")
