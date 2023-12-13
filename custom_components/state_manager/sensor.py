from homeassistant.helpers.entity import Entity
from . import async_setup_entry

class StateManagerSensor(Entity):
    @property
    def state(self):
        return "boo"
