from homeassistant.helpers import device_registry as dr
from .const import DOMAIN
from .input_boolean import StateManagerEnabled

async def async_setup_entry(hass, entry):
    hass.data[DOMAIN] = entry.data['name']

    device_registry = dr.async_get(hass)

    for device in device_registry.devices.values():
        if entry.entry_id in device.config_entries:
            # Get or create the device
            device = device_registry.async_get_or_create(
                config_entry_id=entry.entry_id,
                identifiers={(DOMAIN, device.id)},
                name=device.name,
            )
            #input_boolean = StateManagerEnabled(hass, device)
            #input_boolean.unique_id = entry.entry_id
            #hass.add_job(input_boolean.update_state, 'off')

    return True
