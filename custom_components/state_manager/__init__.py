from homeassistant.helpers import device_registry as dr
from .const import DOMAIN
from .input_boolean import create_input_boolean

async def async_setup_entry(hass, entry):
    hass.data[DOMAIN] = entry.data['name']

    device_registry = dr.async_get(hass)

    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.data['name'])},
        name=entry.data['name'],
    )

    # Create an input boolean for each device
    for device in device_registry.devices.values():
        if entry.entry_id in device.config_entries:
            create_input_boolean(hass, device)

    return True
