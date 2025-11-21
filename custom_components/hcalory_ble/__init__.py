
"""HCalory BLE integration (socket-based) - minimal HACS custom component skeleton."""
from __future__ import annotations

import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .daemon_client import DaemonClient
from .coordinator import HCaloryCoordinator

DOMAIN = "hcalory_ble"

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up hcalory_ble from a config entry."""
    data = entry.data
    # compute socket path from address if not provided
    socket_path = data.get("socket_path")
    address = data.get("address")
    if not socket_path and address:
        socket_path = f"/tmp/hcalory-control-{address.lower().replace(':','_')}.sock"

    client = DaemonClient(socket_path)
    interval = entry.options.get("poll_interval", 1.0)
    coordinator = HCaloryCoordinator(hass, client, interval=interval)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
    }

    # first refresh
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as e:
        _LOGGER.warning("Initial refresh failed: %s", e)

    # forward platforms
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload config entry."""
    tasks = []
    if entry.entry_id in hass.data.get(DOMAIN, {}):
        hass.data[DOMAIN].pop(entry.entry_id, None)
    tasks.append(hass.config_entries.async_unload_platforms(entry, ["sensor"]))
    await asyncio.gather(*tasks)
    return True
