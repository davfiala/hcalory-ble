
async def async_register_services(hass, client, coordinator):
    async def _call_cmd(cmd):
        try:
            await client.command(cmd)
            await coordinator.async_request_refresh()
        except Exception as e:
            raise

    hass.services.async_register("hcalory_ble", "start_heat", lambda call: _call_cmd("start_heat"))
    hass.services.async_register("hcalory_ble", "stop_heat", lambda call: _call_cmd("stop_heat"))
    hass.services.async_register("hcalory_ble", "up", lambda call: _call_cmd("up"))
    hass.services.async_register("hcalory_ble", "down", lambda call: _call_cmd("down"))
    hass.services.async_register("hcalory_ble", "gear", lambda call: _call_cmd("gear"))
    hass.services.async_register("hcalory_ble", "thermostat", lambda call: _call_cmd("thermostat"))
