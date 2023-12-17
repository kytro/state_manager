from homeassistant.helpers import entity_registry
from .const import DOMAIN

async def async_setup_entry(hass, entry):
    hass.data[DOMAIN] = entry.data['name']

    # Get the entity registry
    registry = await entity_registry.async_get(hass)

    # Create a new group
    group = registry.entities.get(hass.data[DOMAIN])

    if group is None:
        group = registry.async_get_or_create(
            domain=DOMAIN,
            platform='group',
            unique_id=hass.data[DOMAIN],
            suggested_object_id=hass.data[DOMAIN],
            config_entry=entry,
        )

    # Add the input_boolean to the group
    input_boolean_entity_id = f"input_boolean.{hass.data[DOMAIN]}_enabled"
    group.entities.append(input_boolean_entity_id)

    return True
