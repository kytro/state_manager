from homeassistant.helpers import device_registry as dr
from .const import DOMAIN
from .input_boolean import StateManagerEnabled
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from homeassistant.const import (
    Platform,
)

PLATFORMS: list[Platform] = [Platform.SWITCH]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data[DOMAIN] = {entry.data['name']: {}}

    device_registry = dr.async_get(hass)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "devices": device_registry.devices
        }

    #for device in device_registry.devices.values():
    #    if entry.entry_id in device.config_entries:
    #        # Get or create the device
    #        device = device_registry.async_get_or_create(
    #            #config_entry_id=entry.entry_id,
    #            identifiers={(DOMAIN, device.id)},
    #            name=device.name,
    #        )
    #        #input_boolean = StateManagerEnabled(hass, device)
    #        #input_boolean.unique_id = entry.entry_id
    #        #hass.add_job(input_boolean.update_state, 'off')

    return True
