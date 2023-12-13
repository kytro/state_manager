# sensor.py
from homeassistant.helpers.entity import Entity

class StateManagerSensor(Entity):
    @property
    def state(self):
        return "boo"
