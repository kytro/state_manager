from homeassistant.helpers import entity_component
from .const import DOMAIN

async def async_setup_entry(hass, entry):
    hass.data[DOMAIN] = entry.data['name']

    # Create a new group
    group = entity_component.EntityComponent(
        hass,
        DOMAIN,
        hass.data[DOMAIN]
    )

    # Add the group to Home Assistant
    await group.async_added_to_hass()

    return True
