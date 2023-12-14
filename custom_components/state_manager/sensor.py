from homeassistant.components.sensor import SensorEntity

from . import StateManagerDevice


class StateManagerExpectedSensor(SensorEntity):

    def __init__(self, device: StateManagerDevice):
        self._device = device

    @property
    def name(self):
        return f"{self._device.name}_expected_state"

    @property
    def native_value(self):
        return self._device.state

    @property
    def device_info(self):
        return self._device.device_info

    @property
    def should_poll(self):
        return False


