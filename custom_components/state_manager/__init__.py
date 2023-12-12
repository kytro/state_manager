"""The state_manager component."""

from homeassistant.helpers import device_registry as dr

DOMAIN = "state_manager"

def setup(hass, config):
    """Set up the state_manager component."""
    # Register a new device
    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id="state_manager",
        identifiers={(DOMAIN, "state_manager_test")},
        name="State Manager Device",
        manufacturer="state_manager",
        model="state_manager"
    )
    return True
