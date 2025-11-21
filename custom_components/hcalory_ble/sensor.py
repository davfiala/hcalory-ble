
from __future__ import annotations
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .coordinator import HCaloryCoordinator

SENSOR_TYPES = {
    "heater_state": {"name": "Heater State"},
    "body_temperature": {"name": "Body Temperature", "unit": "°C"},
    "ambient_temperature": {"name": "Ambient Temperature", "unit": "°C"},
    "voltage": {"name": "Voltage", "unit": "V"},
    "heater_setting": {"name": "Heater Setting"},
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["hcalory_ble"][entry.entry_id]["coordinator"]
    entities = []
    for key, meta in SENSOR_TYPES.items():
        entities.append(HeaterSensor(coordinator, key, meta["name"]))
    async_add_entities(entities)

class HeaterSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: HCaloryCoordinator, key: str, name: str):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name

    @property
    def state(self):
        data = self.coordinator.data or {}
        return data.get(self._key)
