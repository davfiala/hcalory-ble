
import asyncio
import json
import os
import time
from typing import Any, Optional

class DaemonError(RuntimeError):
    pass

class DaemonClient:
    def __init__(self, socket_path: str, connect_timeout: float = 1.0):
        self.socket_path = socket_path
        self.connect_timeout = connect_timeout
        self._cache: Optional[dict[str, Any]] = None
        self._cache_ts: float = 0.0

    async def _open_connection(self, timeout: float):
        if not os.path.exists(self.socket_path):
            raise DaemonError(f"Socket not found: {self.socket_path}")
        try:
            return await asyncio.wait_for(asyncio.open_unix_connection(self.socket_path), timeout=timeout)
        except (OSError, asyncio.TimeoutError) as e:
            raise DaemonError(f"Cannot open socket {self.socket_path}: {e}") from e

    async def _send_raw(self, payload: str, timeout: float = 3.0) -> str:
        reader, writer = await self._open_connection(timeout=self.connect_timeout)
        try:
            writer.write((payload + "\n").encode())
            await writer.drain()
            try:
                data = await asyncio.wait_for(reader.read(-1), timeout=timeout)
            except asyncio.TimeoutError:
                raise DaemonError("Timeout waiting for daemon response")
            if not data:
                raise DaemonError("Empty response from daemon")
            text = data.decode().strip()
            return text
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

    async def command(self, cmd: str, timeout: float = 3.0) -> str:
        text = await self._send_raw(cmd, timeout=timeout)
        if text.startswith("OK:"):
            return text
        if text.startswith("ERROR:"):
            raise DaemonError(text)
        return text

    async def get_status(self, force: bool = False, timeout: float = 3.0) -> dict[str, Any]:
        now = time.time()
        if not force and self._cache is not None and (now - self._cache_ts) < 0.5:
            return self._cache
        cmd = "pump_data" if not force else "pump_data_force"
        text = await self._send_raw(cmd, timeout=timeout)
        try:
            data = json.loads(text)
        except Exception as e:
            raise DaemonError(f"Invalid JSON from daemon: {e}; raw={text!r}")
        self._cache = data
        self._cache_ts = now
        return data
