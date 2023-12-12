"""The state_manager component."""

import logging
from homeassistant.helpers import device_registry as dr

DOMAIN = "state_manager"

_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Set up the state_manager component."""
    # Register a new device
    device_registry = dr.async_get(hass)
    
    # Check if the device already exists
    device = device_registry.async_get_device({(DOMAIN, "state_manager_test")})
    if device is not None:
        _LOGGER.warning("Device with unique ID 'state_manager_test' already exists.")
        return True

    # Create the device
    try:
        device_registry.async_get_or_create(
            config_entry_id="state_manager",
            identifiers={(DOMAIN, "state_manager_test")},
            name="State Manager Device",
            manufacturer="state_manager",
            model="state_manager"
        )
        _LOGGER.info("Device 'State Manager Device' created successfully.")
    except Exception as e:
        _LOGGER.error(f"Failed to create device: {e}")
        return False

    return True
