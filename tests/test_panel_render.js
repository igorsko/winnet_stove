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
      title: "Test stove",
      entities: {
        climate: "climate.test",
        state: "sensor.test_state",
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
      attributes: { current_temperature: 21 },
    },
    "sensor.test_state": { state: "In Funzione", attributes: {} },
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
assert.match(panel.shadowRoot.innerHTML, /In Funzione/);
assert.match(panel.shadowRoot.innerHTML, /Lovelace dashboard/);
panel._activeTab = "consumption";
panel._last = "";
panel.render();
assert.match(panel.shadowRoot.innerHTML, /Consumption and costs/);
panel._activeTab = "refills";
panel._last = "";
panel.render();
assert.match(panel.shadowRoot.innerHTML, /Record refill/);
assert.match(panel.shadowRoot.innerHTML, /15 kg/);
console.log("WiNET panel render smoke tests passed");
