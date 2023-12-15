from homeassistant.helpers import device_registry as dr
from .const import DOMAIN
from .input_boolean import StateManagerEnabled

async def async_setup_entry(hass, entry):
    hass.data[DOMAIN] = entry.data['name']

    device_registry = dr.async_get(hass)

    for device in device_registry.devices.values():
        if entry.entry_id in device.config_entries:
            device_info = device_registry.async_get_or_create(
                identifiers={(DOMAIN, device.id)},
                name=device.name,
                device_info={
                    "identifiers": {(DOMAIN, device.id)},
                    "name": f"{device.name} Enabled",
                    "manufacturer": "Your Manufacturer",
                    "model": "Your Model",
                    "sw_version": "1.0",
                    "via_device": (DOMAIN, device.id),
                },
            )
            input_boolean = StateManagerEnabled(hass, device)
            hass.add_job(input_boolean.update_state, 'off')

    return True
