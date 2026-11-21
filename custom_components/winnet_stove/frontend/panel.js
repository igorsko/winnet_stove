/* SPDX-License-Identifier: GPL-3.0-only */
/** WiNET Stove — independent Home Assistant side panel. No external UI libraries. */
class WinetStovePanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._last = "";
  }

  set hass(value) {
    this._hass = value;
    this.render();
  }

  set panel(value) {
    this._panel = value;
    this.render();
  }

  escape(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  format(entityId) {
    const entity = this._hass?.states?.[entityId];
    if (!entity) return "—";
    if (entity.state === "unavailable" || entity.state === "unknown") return "Unavailable";
    const units = entity.attributes?.unit_of_measurement;
    return this.escape(entity.state) + (units ? " " + this.escape(units) : "");
  }

  render() {
    if (!this._hass || !this._panel) return;
    const stoves = this._panel.config?.stoves || [];
    const blocks = stoves.map((stove, index) => {
      const m = stove.entities || {};
      const climate = m.climate;
      const current = climate ? this._hass.states[climate] : null;
      const mode = current?.state || "unavailable";
      const isOn = mode === "heat";
      const keys = [
        ["Stove status", m.state], ["Power", m.power],
        ["Fan", m.fan], ["Wi-Fi", m.rssi],
        ["Alarms", m.alarm], ["Timer schedule", m.crono]
      ];
      const rows = keys.filter(([_, id]) => id).map(([label, id]) =>
        `<div class="metric"><span>${this.escape(label)}</span><strong>${this.format(id)}</strong></div>`
      ).join("");
      const buttons = climate ? `
        <div class="controls">
          <button data-climate="${this.escape(climate)}" data-mode="heat" ${mode === "unavailable" || isOn ? "disabled" : ""}>Turn on</button>
          <button data-climate="${this.escape(climate)}" data-mode="off" class="secondary" ${mode === "unavailable" || !isOn ? "disabled" : ""}>Turn off</button>
        </div>` : "";
      const temp = current?.attributes?.current_temperature;
      return `
        <section class="stove">
          <div class="top">
            <div><span class="eyebrow">WI-FI PELLET STOVE</span><h2>${this.escape(stove.title || "WiNET Stove " + (index + 1))}</h2></div>
            <span class="status ${isOn ? "on" : ""}">${this.escape(mode)}</span>
          </div>
          <div class="temperature"><span>Room temperature</span><strong>${temp == null ? "—" : this.escape(temp) + " °C"}</strong></div>
          <div class="metrics">${rows}</div>
          ${buttons}
        </section>`;
    }).join("");
    const html = `
      <style>
        :host { display: block; color: var(--primary-text-color); background: var(--primary-background-color); min-height: 100%; }
        * { box-sizing: border-box; }
        .wrap { max-width: 1000px; margin: 0 auto; padding: 24px 20px 64px; font-family: var(--paper-font-body1_-_font-family, sans-serif); }
        .header { display: flex; justify-content: space-between; gap: 12px; align-items: center; margin-bottom: 26px; }
        h1 { margin: 4px 0; font-size: 28px; letter-spacing: -.5px; }
        h2 { margin: 6px 0 0; font-size: 19px; }
        .eyebrow { color: var(--secondary-text-color); font-size: 11px; letter-spacing: 1.6px; font-weight: 700; }
        .small-link { font-size: 13px; color: var(--primary-color); text-decoration: none; }
        .stove { background: var(--card-background-color, #fff); border: 1px solid var(--divider-color, #ddd);
          border-radius: 18px; padding: 24px; margin-bottom: 20px; box-shadow: var(--ha-card-box-shadow, none); }
        .top { display:flex; gap: 20px; justify-content: space-between; align-items: start; }
        .status { padding: 7px 11px; border-radius: 18px; font-size: 12px; background: var(--secondary-background-color); color: var(--secondary-text-color); }
        .status.on { background: color-mix(in srgb, var(--success-color, #32946d) 15%, transparent); color: var(--success-color, #32946d); }
        .temperature { display: flex; flex-direction: column; gap: 4px; padding: 25px 0; }
        .temperature span { color: var(--secondary-text-color); font-size: 13px; }
        .temperature strong { font-size: clamp(28px, 7vw, 42px); letter-spacing: -1px; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(155px,1fr)); gap: 10px; }
        .metric { background: var(--secondary-background-color); border-radius: 12px; padding: 13px; display:flex; flex-direction: column; gap: 7px; }
        .metric span { font-size: 12px; color: var(--secondary-text-color); }
        .metric strong { font-size: 17px; font-weight: 600; overflow-wrap: anywhere; }
        .controls { display:flex; gap: 10px; margin-top: 20px; flex-wrap: wrap; }
        button { border: none; border-radius: 12px; padding: 13px 20px; color: var(--text-primary-color, white);
          background: var(--primary-color); font: inherit; font-weight: 600; cursor: pointer; }
        button.secondary { background: var(--secondary-background-color); color: var(--primary-text-color); }
        button:disabled { opacity: .45; cursor: default; }
        .empty { padding: 24px; }
        @media(max-width:500px) { .wrap{padding:18px 12px 44px} .stove{padding:18px} .header{align-items:start;flex-direction:column} }
      </style>
      <main class="wrap">
        <div class="header">
          <div><span class="eyebrow">SMART HEATING</span><h1>WiNET Stove</h1></div>
          <a class="small-link" href="/winnet-stove-dashboard">Lovelace dashboard</a>
        </div>
        ${blocks || '<p class="empty">No active WiNET Stove devices found.</p>'}
      </main>`;
    if (html !== this._last) {
      this._last = html;
      this.shadowRoot.innerHTML = html;
      this.shadowRoot.querySelectorAll("button[data-climate]").forEach(button => {
        button.addEventListener("click", async () => {
          if (button.disabled) return;
          button.disabled = true;
          try {
            await this._hass.callService("climate", "set_hvac_mode", {
              entity_id: button.dataset.climate,
              hvac_mode: button.dataset.mode
            });
          } catch (error) {
            this._hass?.showToast?.({message: "WiNET command failed"});
            button.disabled = false;
          }
        });
      });
    }
  }
}
customElements.define("winnet-stove-panel", WinetStovePanel);
