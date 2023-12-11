from homeassistant.components.input_boolean import InputBoolean

def setup_platform(hass, config, add_entities, discovery_info=None):
    print(f"Discovery info: {discovery_info}")
    manager = discovery_info.get("manager")
    add_entities([StateInputBoolean(manager)])

class StateInputBoolean(InputBoolean):
    def __init__(self, manager):
        self.manager = manager
        self._state = False  # Initial state off

    @property
    def unique_id(self):
        """Return the unique ID of the input_boolean."""
        return f"{self.manager.unique_id}_input_boolean"

    @property
    def name(self):
        """Return the name of the input_boolean."""
        return f"{self.manager.name} Input Boolean"

    @property
    def is_on(self):
        """Return the current state of the input_boolean."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the input_boolean on."""
        self._state = True
        # Update state manager based on turn on
        self.manager.on_turn_on()

        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the input_boolean off."""
        self._state = False
        # Update state manager based on turn off
        self.manager.on_turn_off()

        self.schedule_update_ha_state()

    def update(self):
        """Update the state of the input_boolean."""
        self._state = self.manager.is_enabled()
        self.schedule_update_ha_state()
