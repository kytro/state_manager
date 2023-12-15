from homeassistant.helpers import device_registry as dr
from .const import DOMAIN
from .switch import StateManagerEnabled

async def async_setup_entry(hass, entry):
    hass.data[DOMAIN] = entry.data['name']

    device_registry = dr.async_get(hass)

    device_info = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.data['name'])},
        name=entry.data['name'],
    )

    # Create a switch for each device
    for device in device_registry.devices.values():
        if entry.entry_id in device.config_entries:
            switch = StateManagerEnabled(device, entry)
            hass.add_job(switch.async_update_ha_state, True)

    return True
