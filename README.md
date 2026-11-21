# WiNET Stove — Home Assistant integration

[![License: GPL-3.0-only](https://img.shields.io/badge/License-GPL--3.0--only-blue)](LICENSE)

## Bring your pellet stove into your smart home

Already have a pellet stove with a **WiNET Wi-Fi module**? **WiNET Stove** helps you connect it to **Home Assistant** so you can see what the stove is doing and control supported functions from the same place as the rest of your home — without relying on a cloud account for everyday communication.

With WiNET Stove you can check whether your stove is running, see its reported temperature and operating status, view alarms, and turn it on or off using Home Assistant. It is designed for people who want a simpler, more connected heating experience, while keeping the stove's built-in controls and safety systems in charge.

### Could it work with my stove?

**WiNET is a controller/module, not a stove brand.** WiNET modules are documented or sold for selected pellet stove models from brands including:

- **Thermorossi** — **Slimquadro 9 Evo** is the model used to develop and test this integration.
- **La Nordica / Extraflame**, **Edilkamin**, **Cadel**, **Klover** and **Piazzetta** — WiNET module suppliers list selected stove models as compatible with the module. This does not mean those stoves already have WiNET installed; check your specific model and Wi-Fi accessory.

Sources for WiNET module/model listings: [WiFi-Stufe compatibility catalogue](https://www.wifi-stufe.com/compatibilita) and [StufaSmart's manufacturer list](https://stufasmart.it/marchi-e-stufe-combatibili/).

> **Important distinction:** these references establish **WiNET module use or compatibility**, **not confirmed compatibility with this Home Assistant integration**. The plugin has been **tested only on Thermorossi Slimquadro 9 Evo**. Different controller firmware, register mappings and commands may require additional work. Do not issue unverified commands to another stove.

**Not sure?** Look for WiNET in the documentation of your stove or its Wi-Fi accessory, and [open an issue](https://github.com/igorsko/winnet_stove/issues) with the **stove brand, model and WiNET controller details** (never share passwords or personal network information). Community testing can help expand the list of verified devices.

## Features

- Climate: stove on/off and measured temperature (target temperature adjustment is not implemented).
- Sensors: stove state, power, fan speed, Wi-Fi RSSI, active alarm, numeric alarm code, timer (crono) state.
- Switch: enable or disable the stove's built-in timer (crono).
- Two native binary sensors: **Stove active** (operating cycle) and **Stove burning** (state `working`), providing on/off history through Home Assistant Recorder.
- Usage sensors: **Current session duration**, **Last ignition** (observed transition), and persistent **Total combustion hours**.
- Configurable polling interval: 10–300 seconds (30 seconds by default).
- Communication errors make Home Assistant entities unavailable instead of falsely reporting the stove as off.
- Register diagnostics remain available separately from the normal climate entity attributes.

**Not yet implemented:** pellet bag inventory, estimated pellet consumption, and maintenance reminders. Counting begins only after the integration is installed. Session and combustion time are conservative estimates based on confirmed samples; offline periods are not inferred. These are planned follow-up enhancements.

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

## History and operating time

When Home Assistant Recorder is enabled and the entities are not excluded, open **Stove active** or **Stove burning** from the device page to view their state history. The original stove-state sensor continues to display the detailed operating phase.

**Current session duration** reports observed time in the ongoing active operating cycle. **Last ignition** records the last transition observed from an idle/off state into an active cycle (an ignition already in progress when Home Assistant starts does not invent a timestamp). **Total combustion hours** counts consecutive samples confirmed to be in the `working` state, and stores the accumulated total across Home Assistant restarts. Unknown state values or missing connectivity do not count as running time.

State mapping varies with firmware: active cycles currently include codes 2, 3, 4, 5, 8, 9, while 1, 6, 7 are treated as idle/off and 0 as unknown. Validate the physical mapping on your stove before relying on it for reports. These readings must not be used as safety interlocks.

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
