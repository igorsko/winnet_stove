# WiNET Stove — Home Assistant integration

[![License: GPL-3.0-only](https://img.shields.io/badge/License-GPL--3.0--only-blue)](LICENSE)

**WiNET Stove** is a custom Home Assistant integration for pellet stoves using a compatible **WiNET Wi-Fi controller**. It communicates locally over HTTP without relying on a cloud account.

> **Compatibility:** tested only on **Thermorossi Slimquadro 9 Evo**. WiNET hardware may appear on other stove brands, but support for other makes and models is unverified. Register mappings and commands may differ.

## Features

- Climate: stove on/off and measured temperature (target temperature adjustment is not implemented).
- Sensors: stove state, power, fan speed, Wi-Fi RSSI, active alarm, numeric alarm code, timer (crono) state.
- Switch: enable or disable the stove's built-in timer (crono).
- Configurable polling interval: 10–300 seconds (30 seconds by default).
- Optional **WiNET Stove dedicated panel** and **prebuilt Lovelace dashboard**, both added automatically to the sidebar and controlled independently from the integration options.
- Communication errors make Home Assistant entities unavailable instead of falsely reporting the stove as off.
- Register diagnostics remain available separately from the normal climate entity attributes.

**Not yet implemented:** operating-hours counters, pellet bag inventory, estimated pellet consumption, and maintenance reminders. These are planned follow-up enhancements.

## Requirements

- Home Assistant with support for custom integrations.
- A compatible WiNET controller reachable over HTTP on your local network.
- IP address or hostname of the WiNET controller.

## Installation

### HACS

1. Open **HACS** and add `https://github.com/igorsko/winnet_stove` as a **Custom repository** of type **Integration**.
2. Install **WiNET Stove**.
3. Restart Home Assistant.
4. Go to **Settings → Devices & services → Add integration**, search for **WiNET Stove**, and enter your controller's address.

### Manual

1. Copy the folder `custom_components/winnet_stove` into your Home Assistant configuration under `custom_components/`.
2. Restart Home Assistant.
3. Add **WiNET Stove** in **Settings → Devices & services**.

## Automatic user interfaces

After adding WiNET Stove, the integration provides two different views (both enabled by default):

1. **WiNET Stove panel** at `/winnet-stove`: an independent, responsive page with temperature, stove status, power, fan and an on/off control based on the existing climate entity. It requires no Mushroom card or other external frontend dependency.
2. **WiNET Stove Lovelace dashboard** at `/winnet-stove-dashboard`: a native dashboard created on first setup with climate, monitoring entities and a 24-hour history graph. You can edit its cards normally in Home Assistant. Its contents are not overwritten by later updates or option changes.

Open **Settings → Devices & services → WiNET Stove → Configure** to change **Show dedicated panel** and **Show Lovelace dashboard** independently. You can show only one or **hide both**. Hiding the Lovelace dashboard removes it from the sidebar but preserves its URL and content; it is **not deleted**. The dedicated panel is unregistered when hidden.

When more than one WiNET stove is configured, both visibility switches apply to the shared views: if any configured stove enables a view, the corresponding view is shown. Existing non-WiNET dashboards are never modified. If a user has already created a dashboard with the reserved URL, WiNET Stove will leave it alone. A dashboard previously deleted by the user is not automatically recreated.

**Note:** this implementation uses Home Assistant's dashboard storage APIs, which can change between Home Assistant versions. Test it on your Home Assistant installation before relying on it. If UI registration fails, the stove entities can still operate.

## Configuration

Set the controller host (for example `192.168.1.100`) in the UI. WiNET Stove communicates with `http://<host>/ajax`. The polling interval can be changed through the integration's **Options** menu; changes reload the integration.

## Updates and migration

**Back up your Home Assistant configuration before updating.** The correct integration folder and manifest domain are `winnet_stove`. Older source code accidentally used `winet_stufa` as an internal constant. This release aligns that constant with the declared manifest domain. Existing entity `unique_id` formats have not been changed, but manually modified installations or entries registered under the legacy domain may need to be reviewed.

## Troubleshooting

- **Cannot connect:** verify controller address, network access, and HTTP port 80.
- **Entities unavailable:** consult Home Assistant logs for `custom_components.winnet_stove`; the controller may be offline or return an invalid response.
- **Unexpected controller behavior:** verify model and firmware before issuing power or timer commands.
- **Other brands:** share sanitized details in a [GitHub issue](https://github.com/igorsko/winnet_stove/issues). Avoid sharing public IP addresses, passwords or sensitive logs.

## Safety

WiNET communication currently uses unencrypted HTTP and controller-specific register commands. Keep the controller on a trusted local network and do **not** expose it to the internet. The integration is not a substitute for the stove's safety mechanisms or manufacturer's maintenance instructions.

## Development

Bug reports, translations, tests and additional verified stove profiles are welcome. Hardware compatibility has to be validated on actual equipment; do not assume arbitrary WiNET controllers share command/register semantics.

## License

Copyright © 2026 igorsko.

Licensed under the **GNU General Public License version 3 only** (`GPL-3.0-only`); see [LICENSE](LICENSE) and [COPYRIGHT](COPYRIGHT). Earlier published MIT-licensed versions retain their historical terms.

## Support the project

If you find this integration useful, [star the repository](https://github.com/igorsko/winnet_stove), [buy me a coffee](https://www.buymeacoffee.com/igorsko), or [donate via PayPal](https://www.paypal.me/igorskorjanc).
