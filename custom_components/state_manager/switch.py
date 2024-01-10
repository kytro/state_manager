from homeassistant.helpers.entity import Entity
from homeassistant.components.switch import SwitchEntity

_LOGGER = logging.getLogger(__name__)

def create_switch_entity(hass, name, unique_id):
    """Creates a State Manager switch entity."""
    _LOGGER.info(f"Creating switch entity: {name} with unique_id: {unique_id}")
    return StateManagerSwitch(hass, name, unique_id)

class StateManagerSwitch(SwitchEntity):
    """Representation of a State Manager switch."""

    def __init__(self, hass, name, unique_id):
        """Initialize the State Manager switch."""
        self._name = name
        self._unique_id = unique_id
        self._is_on = False
        _LOGGER.info(f"Initialized switch: {name} with unique_id: {unique_id}")

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
        _LOGGER.info(f"Turned on switch: {self._name}")
        await self.async_update_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        self._is_on = False
        _LOGGER.info(f"Turned off switch: {self._name}")
        await self.async_update_ha_state()

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the switch platform."""
    _LOGGER.info("Setting up the switch platform")
    switches = []
    for name, data in config.items():
        # Append '_enabled' to the name
        switch_name = name + "_enabled"
        unique_id = data["unique_id"]

        # Create the switch entity
        switch_entity = create_switch_entity(hass, switch_name, unique_id)

        switches.append(switch_entity)
        _LOGGER.info(f"Added switch entity: {switch_name} to the list of switches")

    async_add_entities(switches, True)
    _LOGGER.info("Added all switch entities to Home Assistant")
