
# HCalory BLE (socket) - HACS custom component

This custom component uses a local `hcalory_control` daemon that holds the BLE connection to the heater.
The integration connects to the daemon via a UNIX socket and exposes sensors and services in Home Assistant.

## Quick start

1. Run the `hcalory_control` daemon on the same host:
   ```
   python heater_slower_socket.py --daemon --address EC:B1:B6:05:FB:2A --debug
   ```
2. Install this custom component into `custom_components/hcalory_ble`.
3. Add integration via UI and provide either `address` or `socket_path` (socket path defaults to `/tmp/hcalory-control-<mac>.sock`).
4. Configure poll interval in options if desired.

## Notes
- For HA OS users, running the daemon as an Add-on is recommended.
- Ensure the HA process can access the socket file (permissions or group).
