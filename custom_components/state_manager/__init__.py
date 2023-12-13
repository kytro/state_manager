import logging
from homeassistant.helpers.entity import DeviceInfo, Entity
from homeassistant.helpers.device_registry import async_get as get_dev_reg
from homeassistant.helpers.entity_registry import async_get as get_ent_reg

_LOGGER = logging.getLogger(__name__)
DOMAIN = 'state_manager'

class StateManager(Entity):
    def __init__(self, hass, name, id):
        self._name = name
        self._id = id
        self._state = None
        self._attr_device_info = DeviceInfo(
            identifiers = {(DOMAIN, id)},
            name = name,
            manufacturer = "State Manager",
            model = "State Manager",
        )
        _LOGGER.info(f"Device created: {self._name}")

    @property
    def unique_id(self):
        return f"{DOMAIN}.{self._id}"

    @property
    def name(self):
        return self._name

    @property
    def device_info(self) -> DeviceInfo:
        """Return device registry information for this entity."""
        return self._attr_device_info

    @property
    def state(self):
        return self._state

    async def async_update(self):
        _LOGGER.info("Updating state")
        # Update the state of your entity here

async def async_setup_entry(hass, config_entry):
    _LOGGER.info("Setting up state_manager")
    devices = config_entry.data['devices']
    for device in devices:
        _LOGGER.info(f"Creating device: {device['id']}")
        entity = StateManager(hass, device['name'], device['id'])
        hass.add_job(entity.async_added_to_hass)
        
        # Create a new entity for the device
        entity_id = entity.unique_id
        hass.states.async_set(entity_id, 'off')

        # Add the entity to the entity registry
        ent_reg = get_ent_reg(hass)
        ent_reg.async_get_or_create(
            domain=DOMAIN,
            platform=DOMAIN,
            unique_id=entity.unique_id,
            device_id=entity._id,
            config_entry_id=entity.unique_id,
            name=entity._name,
        )
    return True
