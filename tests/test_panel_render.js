// SPDX-License-Identifier: GPL-3.0-only
// Basic smoke tests without browser dependencies, for GitHub Actions Node.js.
const fs = require("node:fs");
const vm = require("node:vm");
const assert = require("node:assert/strict");

let Panel;
class StubElement {
  attachShadow() {
    const shadow = {
      innerHTML: "",
      querySelector: () => null,
      querySelectorAll: () => [],
    };
    this.shadowRoot = shadow;
    return shadow;
  }
}

const context = {
  HTMLElement: StubElement,
  customElements: { define: (_name, cls) => { Panel = cls; } },
  Date,
  String,
  Number,
  Array,
  Object,
};
const script = fs.readFileSync("custom_components/winnet_stove/frontend/panel.js", "utf8");
vm.runInNewContext(script, context, { filename: "panel.js" });
assert.equal(typeof Panel, "function");

const panel = new Panel();
panel.panel = {
  config: {
    lovelace_available: true,
    stoves: [{
      entry_id: "test-entry",
      title: "Test stove (192.168.2.140)",
      entities: {
        climate: "climate.test",
        state: "sensor.test_state",
        crono_switch: "switch.test_crono",
        pilot_power: "select.pilot_power",
        pilot_fan: "select.pilot_fan",
        pellet_refill_log: "sensor.test_refill_log",
        insights_today_cost: "sensor.today_cost",
      },
    }],
  },
};
panel.hass = {
  states: {
    "climate.test": {
      state: "heat",
      attributes: { current_temperature: 21, temperature: 21 },
    },
    "sensor.test_state": { state: "In Funzione", attributes: {} },
    "switch.test_crono": { state: "on", attributes: {} },
    "select.pilot_power": { state: "1", attributes: {} },
    "select.pilot_fan": { state: "2", attributes: {} },
    "sensor.today_cost": { state: "2.5", attributes: { unit_of_measurement: "€" } },
    "sensor.test_refill_log": {
      state: "1",
      attributes: { total_kg: 15, events: [{
        id: "11111111-1111-4111-8111-111111111111",
        at: "2026-11-21T12:00:00+00:00",
        kg: 15, source: "manual",
      }] },
    },
  },
};
assert.match(panel.shadowRoot.innerHTML, /WiNET Stove/);
assert.match(panel.shadowRoot.innerHTML, /data-tab="consumption"/);
assert.match(panel.shadowRoot.innerHTML, /data-tab="maintenance"/);
assert.match(panel.shadowRoot.innerHTML, /Running/);
assert.doesNotMatch(panel.shadowRoot.innerHTML, /192\\.168\\.2\\.140/);
assert.match(panel.shadowRoot.innerHTML, /Lovelace dashboard/);
assert.match(panel.shadowRoot.innerHTML, /class="power-action power-stop"/);
assert.match(panel.shadowRoot.innerHTML, /class="control-summary"/);
assert.match(panel.shadowRoot.innerHTML, /class="crono-control"/);
assert.match(panel.shadowRoot.innerHTML, /class="pilot-panel"/);
assert.match(panel.shadowRoot.innerHTML, /data-pilot-step="select.pilot_fan"/);
assert.match(panel.shadowRoot.innerHTML, /data-pilot-temp="21.5"/);
assert.match(panel.shadowRoot.innerHTML, /data-crono="switch.test_crono"/);
assert.match(panel.shadowRoot.innerHTML, /data-crono-action="turn_off"/);
assert.match(panel.shadowRoot.innerHTML, /Disable Crono/);
assert.match(panel.shadowRoot.innerHTML, /class="health-strip"/);
assert.match(panel.shadowRoot.innerHTML, /<svg class="ico"/);
assert.equal((panel.shadowRoot.innerHTML.match(/data-climate=/g) || []).length, 1,
  "Only one primary power button should exist in Control");
assert.doesNotMatch(panel.shadowRoot.innerHTML, /class="metrics key-metrics"/);
assert.match(panel.shadowRoot.innerHTML, /var\(--secondary-background-color\)/);

panel._activeTab = "consumption";
panel._last = "";
panel.render();
assert.match(panel.shadowRoot.innerHTML, /Consumption and costs/);
panel._activeTab = "refills";
panel._last = "";
panel.render();
assert.match(panel.shadowRoot.innerHTML, /Record refill/);
assert.match(panel.shadowRoot.innerHTML, /15 kg/);

// Home Assistant language must localize the same panel and retain English
// as the fallback for other language codes.
panel.hass = { ...panel._hass, locale: { language: "it" } };
panel._activeTab = "control";
panel._last = "";
panel.render();
assert.match(panel.shadowRoot.innerHTML, /Controllo/);
assert.match(panel.shadowRoot.innerHTML, /In funzione/);
assert.match(panel.shadowRoot.innerHTML, /Temperatura ambiente/);
assert.match(panel.shadowRoot.innerHTML, /Spegni stufa/);
assert.match(panel.shadowRoot.innerHTML, /Disattiva Crono/);
assert.match(panel.shadowRoot.innerHTML, /Dettagli tecnici/);
panel._activeTab = "consumption";
panel._last = "";
panel.render();
assert.match(panel.shadowRoot.innerHTML, /Consumi e costi/);
assert.match(panel.shadowRoot.innerHTML, /Configura il consumo del pellet/);
panel._activeTab = "refills";
panel._last = "";
panel.render();
assert.match(panel.shadowRoot.innerHTML, /Registra rifornimento/);
panel._activeTab = "maintenance";
panel._last = "";
panel.render();
assert.match(panel.shadowRoot.innerHTML, /Manutenzione/);
assert.match(panel.shadowRoot.innerHTML, /maintenance-label/);
panel._activeTab = "settings";
panel._last = "";
panel.render();
assert.match(panel.shadowRoot.innerHTML, /Pellet e prezzi/);
panel.hass = { ...panel._hass, locale: { language: "sl" } };
panel._last = "";
panel.render();
assert.match(panel.shadowRoot.innerHTML, /Pellet and prices/);
console.log("WiNET panel render smoke tests passed");
