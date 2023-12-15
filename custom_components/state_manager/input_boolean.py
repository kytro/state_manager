from homeassistant.components import input_boolean

def create_input_boolean(hass, device):
    input_boolean_entity_id = f"input_boolean.{device.name}_enabled"
    hass.states.async_set(input_boolean_entity_id, 'off', {"friendly_name": f"{device.name} Enabled"})