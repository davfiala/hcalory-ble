
from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

class HCaloryConfigFlow(config_entries.ConfigFlow, domain="hcalory_ble"):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input.get("address") or "hcalory", data=user_input)
        data_schema = vol.Schema(
            {
                vol.Optional("address", default=""): str,
                vol.Optional("socket_path", default=""): str,
                vol.Optional("poll_interval", default=1.0): float,
            }
        )
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
