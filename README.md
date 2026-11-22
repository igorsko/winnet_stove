# WiNET Stove — Home Assistant integration

[![License: GPL-3.0-only](https://img.shields.io/badge/License-GPL--3.0--only-blue)](LICENSE)

## Bring your pellet stove into your smart home

Already have a pellet stove with a **WiNET Wi-Fi module**? **WiNET Stove** helps you connect it to **Home Assistant** so you can see what the stove is doing and control supported functions from the same place as the rest of your home — without relying on a cloud account for everyday communication.

With WiNET Stove you can check whether your stove is running, see its reported temperature and operating status, view alarms, and turn it on or off using Home Assistant. It is designed for people who want a simpler, more connected heating experience, while keeping the stove's built-in controls and safety systems in charge.

### Supported stove

WiNET Stove is currently developed and tested **only with the Thermorossi Slimquadro 9 Evo**. Other manufacturers may use WiNET-branded hardware, but that does **not** make their stoves compatible with this integration. Register layouts and commands can differ between controllers and firmware.

**Other stove brands and models are not supported or maintained by this project.** Please do not assume a different WiNET-equipped stove will work, and do not use unverified commands on other hardware.

## Features

- Climate: stove on/off and measured temperature (target temperature adjustment is not implemented).
- Sensors: stove state, power, fan speed, Wi-Fi RSSI, active alarm, numeric alarm code, timer (crono) state.
- Switch: enable or disable the stove's built-in timer (crono).
- Two native binary sensors: **Stove active** (operating cycle) and **Stove burning** (state `working`), providing on/off history through Home Assistant Recorder.
- Usage sensors: **Current session duration**, **Last ignition** (observed transition), and persistent **Total combustion hours**.
- Configurable polling interval: 10–300 seconds (30 seconds by default).
- One WiNET Stove sidebar entry: dedicated responsive panel with internal **Control, Consumption, Refills, Maintenance, Settings** views. The separately editable Lovelace dashboard remains accessible via a link without duplicating sidebar items.
- Communication errors make Home Assistant entities unavailable instead of falsely reporting the stove as off.
- Register diagnostics remain available separately from the normal climate entity attributes.

**Consumption remains an estimate, never a direct pellet measurement.** Maintenance reminders, user-defined pellet prices, refill history and consumption calibration are included. Combustion time is based on confirmed samples; offline periods are not counted.

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

## Crono scheduling control

The dedicated Control tab exposes an **Enable/Disable Crono** action whenever
the existing Home Assistant `crono_switch` is available. It uses the already
implemented switch entity and its verified local commands, asks for
confirmation, and is disabled when the switch state is unavailable. It toggles
the stove's previously configured weekly schedule; this panel does not edit
individual schedule times.

**Temperature setpoint, burner power and room fan speed remain read-only**
until register mapping, encoding and safe limits are verified on the tested
Thermorossi Slimquadro 9 Evo. Cloud-app controls do not prove the equivalent
local write register numbers. No speculative controller writes are included.

## Responsive visual controls

Since v1.3.0 the dedicated WiNET panel uses light, dependency-free inline vector icons.
It inherits Home Assistant's theme tokens, so cards automatically follow light and dark
mode. **Control** has one prominent, contextual power action at the top (turn on
or turn off, with confirmation); the stove's state, room temperature, power, fan,
combustion hours and current alarm are not duplicated in the visible view.
Detailed status and scheduling remain accessible under **Technical details**.

The other four views use the same iconography and spacing: consumption summaries
show sources of estimates, refills keep their dated audit trail and correction
actions, maintenance keeps its hour-based progress bars, and settings retain
collapsed advanced calibration and diagnostics. No new controller register
writes, dependencies, or non-measured sensor claims were added.

## Integration icon

WiNET Stove includes an original flame-and-Wi-Fi brand icon with a transparent
background, available at 256 × 256 and 512 × 512 pixels:

- `custom_components/winnet_stove/brand/icon.png`
- `custom_components/winnet_stove/brand/icon@2x.png`

Home Assistant **2026.3 or later** reads these brand images directly from the
installed custom integration. The square icon also serves as the integration
logo when a separate wide logo is not provided. Brand icons require no extra
frontend dependencies and are suitable for both light and dark backgrounds.

Some HACS versions have not displayed integration-local icons correctly,
even when they work in Home Assistant's Integrations page. HACS presentation
depends on the installed HACS version and its icon source; a placeholder
there does not necessarily mean that the integration's icon is missing.
After upgrading, restart Home Assistant and refresh HACS.

## Dashboard language and user experience

The WiNET Stove dedicated panel supports **Italian and English**, automatically following
the signed-in Home Assistant user's language preference. English is the default for
other languages. The redesigned responsive panel groups information into **Control,
Consumption, Refills, Maintenance and Settings**, prioritizes everyday controls,
hides advanced diagnostics and per-power calibration in expandable sections,
and explains unavailable estimates instead of displaying repeated unavailable values.
Detailed refill records, automations, and the editable Lovelace dashboard are preserved.

## Automatic user interfaces

After adding WiNET Stove, the integration provides a dedicated panel and an editable Lovelace dashboard (both enabled by default). They share **at most one sidebar entry**:

1. **WiNET Stove panel** at `/winnet-stove`: an independent, responsive page with temperature, stove status, power, fan and an on/off control based on the existing climate entity. It requires no Mushroom card or other external frontend dependency.
2. **WiNET Stove Lovelace dashboard** at `/winnet-stove-dashboard`: a native dashboard created on first setup with climate, monitoring entities and a 24-hour history graph. You can edit its cards normally in Home Assistant. Its contents are not overwritten by later updates or option changes.

If both are enabled, only the **dedicated panel** appears in the sidebar; it includes a link to the Lovelace dashboard. If the panel is disabled, the dashboard may appear as the sole sidebar item. Neither is shown when both options are off. The Lovelace dashboard's saved content is not overwritten.

Open **Settings → Devices & services → WiNET Stove → Configure** to change **Show dedicated panel** and **Show Lovelace dashboard** independently. You can show only one or **hide both**. Hiding the Lovelace dashboard removes it from the sidebar but preserves its URL and content; it is **not deleted**. The dedicated panel is unregistered when hidden.

When more than one WiNET stove is configured, both visibility switches apply to the shared views: if any configured stove enables a view, the corresponding view is shown. Existing non-WiNET dashboards are never modified. If a user has already created a dashboard with the reserved URL, WiNET Stove will leave it alone. A dashboard previously deleted by the user is not automatically recreated.

**Note:** this implementation uses Home Assistant's dashboard storage APIs, which can change between Home Assistant versions. Test it on your Home Assistant installation before relying on it. If UI registration fails, the stove entities can still operate.

## Automatic pellet refill inference (optional)

WiNET alarm **bit 0** is labelled **NO PELLET / CLEAN BURNER**. It is **not definitive proof** that the hopper is empty. For this reason the **Infer pellet refill after alarm** switch is **disabled by default**. When enabled, WiNET Stove watches for this alarm, an observed off/starting state, a cleared alarm, and **two consecutive working-state polls**. It then records **one presumed pellet bag** using the configured bag weight for any future calculations, and decreases stock by one if positive.

One presumed bag is logged per observed alarm episode; reconnects and normal polls do not generate further bags. Pending alarm state and counters persist across restarts. This operation **never sends a command to the stove**. Cleaning a burner, clearing a pellet blockage, or a partial refill can make the inferred bag count inaccurate. The user can disable the switch or correct or delete an inferred refill in the refill history.

## Pellet and hours accounting

- **Initial stove hours**: enter the pre-existing hours from the stove's display. The separate sensor *Total stove hours incl. initial* adds the confirmed Home Assistant combustion time to that number. Initial hours are not included in pellet estimates.
- **Bag weight** (default 15 kg): set the weight of your bags.
- **Estimated burn rate** (kg/h): enter an approximate average for your stove; **default is zero, meaning not configured**. No estimated consumption will be shown until you provide a nonzero rate. Real pellet use varies with power, fuel, ignition and operating conditions.
- **Bags in stock**: edit the available number of bags, if you want inventory tracking.
- **Refill editor** in the dedicated WiNET panel: choose kilograms or bags, save a dated manual refill, and edit or delete any recent manual or automatically inferred refill. The earlier single-bag button remains as a compatibility entity for existing automations, but is no longer displayed in the panel.
- Sensors show counted bags loaded, **estimated kg and bags consumed**, **estimated bags/hour**, and **estimated hours/bag** based on confirmed `working` hours. The consumed estimates do **not** count the manual bags as physically burned; they are separate indicators. Historical hours are never treated as consumption observed by Home Assistant.

Data is stored locally by Home Assistant per device and is preserved across restarts. An already-existing editable Lovelace dashboard is intentionally **not overwritten** by updates: add the new entities manually, or create a new dashboard for the full pellet section. The original dashboard generated on a first install includes the pellet controls and sensors.

### Refill history and migration

The refill log records **quantity (kg)**, **date**, and **source** (manual or automatically inferred). In the WiNET dedicated panel, open **Record refill** to add a quantity; use **Edit** or **Delete** next to an event to correct a mistaken entry. Automatic inference is explicitly labeled, because the WiNET alarm may also mean *clean burner*. No refill record sends any command to the stove.

Already-recorded bag counters are preserved as historical totals, but past bags lack a known weight or timestamp. They are therefore **not fabricated into the new refill history or kilogram total**. Only newly recorded events have editable details. The dedicated panel shows the **20 most recent events**; the underlying local store retains up to 5,000 events. A full-bag event decreases whole-bag stock only if stock is positive; partial-kg refills are not automatically deducted from whole-bag inventory.

Home Assistant service actions `winnet_stove.record_refill`, `winnet_stove.edit_refill`, and `winnet_stove.remove_refill` are used by the panel. The legacy `Log one pellet bag loaded` button is retained for compatibility with existing automations. Existing user-edited Lovelace dashboards are **not overwritten** by updates; the new panel manages refill history while Lovelace can show the `Pellet refills` sensor.

## Consumption, expenses and calibration

The **Consumption** tab tracks confirmed combustion hours by local calendar day and reports
raw controller power values and time spent at each power. Raw register values are **not
assumed to be manufacturer-calibrated power levels**. Nothing is written to the stove.

The plugin supports these estimation paths:

1. **Average kg/h:** input a user-estimated pellet rate. Without a configured rate
   estimates are unavailable, not zero.
2. **Two full-hopper events:** when recording refills, optionally check **Hopper returned
   to the same full level**. If two confirmed full events exist, calculate an observed
   interval average as **all kg added after the first full event up to and including the
   second full event / confirmed burning hours between them**. Missing unrecorded top-ups
   invalidate this calibration. Ordinary and automatically inferred refills are *not*
   marked as full by default.
3. **Power-aware rates:** optionally configure kg/h for each reported raw power value
   1–5. The plugin uses this profile **only if all observed power time has configured rates**;
   otherwise it falls back to an interval-calibrated or user-average rate. Do not enter
   arbitrary manufacturer estimates as measured facts.

The **estimated cost** uses the configured bag price, bag weight and estimated kg.
Daily totals are retained for up to 400 local days from the time this feature is installed;
there is no historical reconstruction. Current-day and month statistics update after
validated working samples. Unknown prices or missing rates produce unavailable costs.

## Maintenance

The **Maintenance** tab monitors confirmed working hours since each maintenance event.
Default reminder thresholds are burner cleaning **12 hours**, deep cleaning **100 hours**,
and annual maintenance **1,000 hours**. These are **illustrative configurable defaults,
not manufacturer maintenance recommendations**. Consult the Thermorossi manual for actual
maintenance intervals. Tap **Completed** after performing a task; a confirmation is
required and the corresponding timer restarts. A Home Assistant persistent notification
is created once per maintenance cycle when overdue.

## Diagnostics and backups

The dedicated panel's **Settings** tab provides **Connection diagnostics**:
last valid controller response, current consecutive communication failures and
accumulated errors. A lost WiNET connection is not interpreted as the stove
switching off, and unavailable periods are excluded from combustion accounting.

The plugin saves its measurements, counter corrections, refill history and
maintenance state to Home Assistant's local `.storage` area. To restore these
values after a server failure, use a **Home Assistant configuration backup**
containing `.storage`. Back up before installing updates; restoring a backup
rolls back subsequent records. The plugin does not silently delete existing
data or generate a fake history.

## Counter correction and migration

The **Settings** tab includes a confirmed **Reset legacy bag counter** action.
This affects only pre-ledger bag counts, and **never deletes your refill records or
operating-time history**. It is intended for one-off corrections, not regular use.

All statistics, maintenance baselines and calibration events are stored locally with
the pre-existing usage data. Legacy combustion hours are preserved; first-time
maintenance intervals begin at the observed total on migration, preventing immediate
false reminders. Neither the original pellet readings nor built-in stove safety controls
are replaced. For backups, protect the Home Assistant configuration and `.storage`
directory before updates. Check your dashboard after migration because user-editable
Lovelace cards are not overwritten.

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

## Frontend refresh after updates

The dedicated WiNET panel URL is `/winnet-stove`; the optional, user-editable
Lovelace dashboard URL is `/winnet-stove-dashboard`. These are **different UIs**.

Since v1.2.1 the dedicated panel loads its JavaScript using a release-versioned
module URL (for example, `/api/winnet_stove/panel.js?v=1.2.1`) to avoid stale
ES-module imports across updates. After updating with HACS, **restart Home
Assistant and reload the browser tab**. If the screen still looks unchanged,
check the browser URL: `/winnet-stove-dashboard` displays the independently
editable legacy Lovelace view, which is intentionally not overwritten.

The manifest version and `manifest_version.py` version must be kept in sync
when publishing future releases.
