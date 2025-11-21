
from __future__ import annotations
from datetime import timedelta
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

class HCaloryCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, client, interval: float = 1.0):
        self.client = client
        super().__init__(
            hass,
            _LOGGER,
            name="hcalory",
            update_interval=timedelta(seconds=interval),
        )

    async def _async_update_data(self):
        try:
            data = await self.client.get_status(force=False, timeout=3.0)
            return data
        except Exception as e:
            _LOGGER.warning("Error fetching status from daemon: %s", e)
            raise UpdateFailed(e)
