from homeassistant.helpers.entity import Entity

def create_switch_entity(hass, name, unique_id):
    """Creates a State Manager switch entity."""
    return StateManagerSwitch(hass, name, unique_id)

class StateManagerSwitch(Entity):
    """Representation of a State Manager switch."""

    def __init__(self, hass, name, unique_id):
        """Initialize the State Manager switch."""
        self._name = name
        self._unique_id = unique_id
        self._is_on = False

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique ID of the switch."""
        return self._unique_id

    @property
    def is_on(self):
        """Return the state of the switch."""
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        self._is_on = True
        await self.async_update_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        self._is_on = False
        await self.async_update_ha_state()
