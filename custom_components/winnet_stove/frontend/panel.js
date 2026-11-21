/* SPDX-License-Identifier: GPL-3.0-only */
/** WiNET Stove — independent Home Assistant side panel. No external UI libraries. */
class WinetStovePanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._last = "";
    this._activeTab = "control";
    this._refillDraft = null;
    this._uiMessage = "";
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
      const pelletMetrics = [
        ["Total stove hours", m.pellet_total_hours],
        ["Bags loaded", m.pellet_bags_loaded],
        ["Estimated pellet used", m.pellet_pellet_used],
        ["Estimated bags used", m.pellet_estimated_bags],
        ["Auto-refill detection", m.pellet_auto_refill],
        ["Bags per hour", m.pellet_bags_per_hour],
        ["Hours per bag", m.pellet_hours_per_bag],
        ["Estimated today", m.insights_today_pellet],
        ["Cost today", m.insights_today_cost],
        ["Cost this month", m.insights_month_cost],
        ["Calibrated / average rate", m.insights_effective_rate]
      ];
      const pelletNumbers = [
        ["Initial hours", m.pellet_setting_initial_hours],
        ["Bag weight", m.pellet_setting_bag_weight_kg],
        ["Average consumption", m.pellet_setting_rate_kg_h],
        ["Bags in stock", m.pellet_setting_bags_in_stock],
        ["Price per bag", m.pellet_setting_price_per_bag],
        ["Burner cleaning interval", m.maintenance_interval_burner],
        ["Deep cleaning interval", m.maintenance_interval_deep_clean],
        ["Annual service interval", m.maintenance_interval_annual_service],
        ["Reported power 1 (kg/h)", m.power_rate_1],
        ["Reported power 2 (kg/h)", m.power_rate_2],
        ["Reported power 3 (kg/h)", m.power_rate_3],
        ["Reported power 4 (kg/h)", m.power_rate_4],
        ["Reported power 5 (kg/h)", m.power_rate_5]
      ];
      const pelletReadings = pelletMetrics.filter(([_, id]) => id).map(([label, id]) =>
        `<div class="metric"><span>${this.escape(label)}</span><strong>${this.format(id)}</strong></div>`
      ).join("");
      const pelletSettings = pelletNumbers.filter(([_, id]) => id).map(([label, id]) =>
        `<button class="setting" data-info="${this.escape(id)}">
          <span>${this.escape(label)}</span><strong>${this.format(id)}</strong>
        </button>`
      ).join("");
      const ledger = m.pellet_refill_log
        ? this._hass.states?.[m.pellet_refill_log]?.attributes || {}
        : {};
      const refills = Array.isArray(ledger.events) ? ledger.events : [];
      const refillRows = refills.map(event => {
        const label = event.source === "auto" ? "Automatic · inferred" : "Manual";
        const date = new Date(event.at);
        const when = Number.isNaN(date.valueOf())
          ? "Date unavailable" : date.toLocaleString();
        return `<div class="refill-row">
          <div><strong>${this.escape(event.kg)} kg</strong>
            <small>${this.escape(label)} · ${this.escape(when)}</small></div>
          <div class="row-actions">
            <button class="secondary mini" data-refill-edit="${this.escape(event.id)}"
              data-entry="${this.escape(stove.entry_id)}"
              data-kg="${this.escape(event.kg)}"
            data-full="${event.full_hopper ? "true" : "false"}">Edit</button>
            <button class="secondary mini" data-refill-delete="${this.escape(event.id)}"
              data-entry="${this.escape(stove.entry_id)}">Delete</button>
          </div>
        </div>`;
      }).join("");
      const refillCard = stove.entry_id ? `
        <div class="refill-manager">
          <div class="refill-head"><div><h4>Refills</h4>
          <p class="hint">Record how much pellet you add. Automatic entries are
          only inferred from alarm recovery and may need correction.</p></div>
          <button data-refill-new="${this.escape(stove.entry_id)}">Record refill</button></div>
          <p class="refill-error" role="alert">${this.escape(this._refillDraft ? "" : this._uiMessage)}</p>
          <div class="refill-summary">
            Recorded: <strong>${this.escape(ledger.total_kg ?? "0")} kg</strong>
            · ${this.escape(refills.length)} recent entries
          </div>
          ${refillRows || '<p class="hint">No refills registered yet.</p>'}
        </div>` : "";
      const maintenance = [
        ["Burner cleaning", "burner", m.insights_maintenance_burner],
        ["Deep cleaning", "deep_clean", m.insights_maintenance_deep_clean],
        ["Annual service", "annual_service", m.insights_maintenance_annual_service]
      ].map(([title, key, entity]) => `
        <div class="maintenance-item">
          <div><strong>${this.escape(title)}</strong><br>
          <small>${entity ? this.format(entity) : "—"} until due</small></div>
          <button class="secondary" data-maint-kind="${this.escape(key)}"
            data-entry="${this.escape(stove.entry_id)}">Completed</button>
        </div>`).join("");
      const fullRateId = m.insights_effective_rate;
      const rateSource = fullRateId
        ? this._hass.states?.[fullRateId]?.attributes?.source
        : null;
      const dailyHistory = m.insights_month_cost
        ? this._hass.states?.[m.insights_month_cost]?.attributes?.daily_history || []
        : [];
      const dailyRows = dailyHistory.slice(-10).reverse().map(day =>
        `<div class="refill-row"><span>${this.escape(day.date)}</span>
          <strong>${this.escape(day.working_h)} h ·
          ${day.estimated_kg == null ? "—" : this.escape(day.estimated_kg) + " kg"} ·
          ${day.estimated_cost == null ? "—" : this.escape(day.estimated_cost) + " €"}</strong>
        </div>`).join("");
      const powerData = m.insights_power_profile
        ? this._hass.states?.[m.insights_power_profile]?.attributes?.power_hours || {}
        : {};
      const powerRows = Object.entries(powerData).map(([key, hours]) =>
        `<div class="metric"><span>Power ${this.escape(key)}</span>
        <strong>${this.escape(hours)} h</strong></div>`).join("");
      const temp = current?.attributes?.current_temperature;
      return `
        <section class="stove">
          <div class="top">
            <div><span class="eyebrow">WI-FI PELLET STOVE</span><h2>${this.escape(stove.title || "WiNET Stove " + (index + 1))}</h2></div>
            <span class="status ${isOn ? "on" : ""}">${this.escape(mode)}</span>
          </div>
          <section class="tab-content" ${this._activeTab !== "control" ? "hidden" : ""}>
            <div class="temperature"><span>Room temperature</span><strong>${temp == null ? "—" : this.escape(temp) + " °C"}</strong></div>
            <div class="metrics">${rows}</div>
            ${buttons}
          </section>
          <section class="tab-content" ${this._activeTab !== "consumption" ? "hidden" : ""}>
            <h3>Consumption and costs</h3>
            <p class="hint">Estimates, not measured pellet. Source: ${this.escape(rateSource || "unconfigured")}.
              Mark the hopper as full on two refills at the same level to calibrate an average consumption rate.</p>
            <div class="metrics">${pelletReadings}</div>
            <h4>Last 10 days</h4>${dailyRows || '<p class="hint">No tracked burning yet.</p>'}
            <h4>Burning hours per reported power</h4>
            <div class="metrics">${powerRows || '<p class="hint">No valid power samples yet.</p>'}</div>
          </section>
          <section class="tab-content" ${this._activeTab !== "refills" ? "hidden" : ""}>
            ${refillCard}
          </section>
          <section class="tab-content" ${this._activeTab !== "maintenance" ? "hidden" : ""}>
            <h3>Maintenance</h3>
            <p class="hint">Suggested intervals based on observed burning hours.
            Follow the stove manufacturer's maintenance instructions.</p>
            ${maintenance}
          </section>
          <section class="tab-content" ${this._activeTab !== "settings" ? "hidden" : ""}>
            <h3>Pellet and maintenance settings</h3>
            <p class="hint">Tap an item to modify it. Changes affect only Home Assistant accounting. Reported power rates are optional: zero means unconfigured. Values must be calibrated for your stove.</p>
            <div class="settings">${pelletSettings}</div>
            <div class="controls">
              <button class="secondary" data-reset-legacy="${this.escape(stove.entry_id)}">
                Reset legacy bag counter
              </button>
            </div>
            <p class="hint">This resets only the historical bag count, not detailed refill records.</p>
          </section>
        </section>`;
    }).join("");
    const draft = this._refillDraft;
    const modal = draft ? `
      <dialog class="refill-dialog" aria-label="Refill editor">
        <h3>${draft.id ? "Correct refill" : "Record pellet refill"}</h3>
        <p class="hint">Enter the actual amount of pellet placed in the hopper.
        An automatic entry is only an estimate based on the stove alarm.</p>
        <label for="refill-qty">Quantity</label>
        <div class="refill-input">
          <input id="refill-qty" type="number" min="0.001" step="any"
            value="${this.escape(draft.quantity)}" required>
          <select id="refill-unit">
            <option value="kg" ${draft.unit === "kg" ? "selected" : ""}>kg</option>
            <option value="bags" ${draft.unit === "bags" ? "selected" : ""}>bags</option>
          </select>
        </div>
        <label class="full-check"><input type="checkbox" id="refill-full" ${draft.full ? "checked" : ""}> Serbatoio riportato a pieno (per calibrare il consumo)</label>
        <p class="hint">One bag = ${this.escape(draft.weight)} kg.
        The quantity is converted to kilograms before saving.</p>
        <p class="refill-error" role="alert">${this.escape(this._uiMessage)}</p>
        <div class="controls">
          <button data-refill-save>Save refill</button>
          <button class="secondary" data-refill-cancel>Cancel</button>
        </div>
      </dialog>` : "";
    const html = `
      <style>
        :host { display: block; color: var(--primary-text-color); background: var(--primary-background-color); min-height: 100%; }
        * { box-sizing: border-box; }
        .wrap { max-width: 1000px; margin: 0 auto; padding: 24px 20px 64px; font-family: var(--paper-font-body1_-_font-family, sans-serif); }
        .tab-content[hidden] { display:none !important; }
        .tabs {display:flex; gap:7px; overflow-x:auto; margin:0 0 16px; padding:0 0 8px; }
        .tabs button {white-space:nowrap; padding:10px 14px; border-radius:999px; background:var(--secondary-background-color); color:var(--primary-text-color); }
        .tabs button.selected {background:var(--primary-color); color:var(--text-primary-color,white);}
        .maintenance-item {display:flex;justify-content:space-between;align-items:center;gap:10px;padding:15px 0;border-bottom:1px solid var(--divider-color);}
        .maintenance-item small {color:var(--secondary-text-color);}
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
        .pellet { margin-top: 24px; border-top: 1px solid var(--divider-color); padding-top: 18px; }
        .pellet h3 { font-size: 18px; margin: 0 0 6px; }
        .hint { font-size: 12px; line-height: 1.6; color: var(--secondary-text-color); margin: 0 0 16px; }
        .settings { display: grid; grid-template-columns: repeat(auto-fit,minmax(160px,1fr)); gap: 10px; margin-top: 14px; }
        .settings .setting { background: var(--secondary-background-color); color: var(--primary-text-color); display: flex; flex-direction: column; align-items: flex-start; gap: 8px; text-align: left; }
        .settings .setting span { color: var(--secondary-text-color); font-size: 12px; }
        .settings .setting strong { font-size: 17px; }
        .refill-manager { margin-top: 20px; padding-top: 15px; border-top: 1px solid var(--divider-color); }
        .refill-head { display:flex; gap:14px; align-items:center; justify-content:space-between; }
        .refill-head h4 { margin:0 0 7px; }
        .refill-head p { margin:0; max-width:550px; }
        .refill-summary { padding:13px 0; font-size:13px; color:var(--secondary-text-color); }
        .refill-row { display:flex; justify-content:space-between; gap:12px; align-items:center;
          border-top:1px solid var(--divider-color); padding:10px 0; }
        .refill-row small { display:block; margin-top:4px; color:var(--secondary-text-color); }
        .row-actions { display:flex; gap:5px; }
        button.mini { padding:7px 10px; font-size:12px; }
        .refill-dialog { max-width:min(420px,92vw); border:1px solid var(--divider-color);
          border-radius:16px; background:var(--card-background-color); color:var(--primary-text-color);
          padding:24px; box-shadow:0 16px 48px #0005; }
        .refill-dialog::backdrop { background:#0008; }
        .refill-dialog h3 { margin-top:0; }
        .refill-input { display:flex; gap:10px; margin-top:8px; }
        .refill-input input { min-width:0; flex:1; }
        .refill-input input,.refill-input select { background:var(--secondary-background-color);
          color:var(--primary-text-color); border:1px solid var(--divider-color);
          border-radius:8px; padding:10px; font:inherit; }
        .full-check {display:flex;align-items:center;gap:9px;margin-top:16px;font-size:13px;}
        .refill-error { color:var(--error-color,#ba2630); font-size:13px; }
        @media(max-width:500px) { .refill-head { align-items:start; flex-direction:column; } }
        button { border: none; border-radius: 12px; padding: 13px 20px; color: var(--text-primary-color, white);
          background: var(--primary-color); font: inherit; font-weight: 600; cursor: pointer; }
        button.secondary { background: var(--secondary-background-color); color: var(--primary-text-color); }
        button:disabled { opacity: .45; cursor: default; }
        .empty { padding: 24px; }
        @media(max-width:500px) { .wrap{padding:18px 12px 44px} .stove{padding:18px} .header{align-items:start;flex-direction:column} }
      </style>
      <main class="wrap">\n        ${modal}
        <div class="header">
          <div><span class="eyebrow">SMART HEATING</span><h1>WiNET Stove</h1></div>
          ${this._panel.config?.lovelace_available ? '<a class="small-link" href="/winnet-stove-dashboard">Lovelace dashboard</a>' : ""}
        </div>
        <nav class="tabs" aria-label="WiNET Stove sections">
          ${[
            ["control", "Control"], ["consumption", "Consumption"],
            ["refills", "Refills"], ["maintenance", "Maintenance"],
            ["settings", "Settings"],
          ].map(([id,label]) => `<button data-tab="${id}" class="${this._activeTab===id ? "selected" : ""}"
             aria-current="${this._activeTab===id ? "page" : "false"}">${label}</button>`).join("")}
        </nav>
        ${blocks || '<p class="empty">No active WiNET Stove devices found.</p>'}
      </main>`;
    if (html !== this._last) {
      // Home Assistant can push fresh state while a user is typing.
      // Preserve the open editor and its unsaved quantity across rerenders.
      const previous = this.shadowRoot.querySelector(".refill-dialog");
      const wasOpen = !!previous?.open;
      const typed = wasOpen ? previous.querySelector("#refill-qty")?.value : null;
      const unit = wasOpen ? previous.querySelector("#refill-unit")?.value : null;
      const full = wasOpen ? previous.querySelector("#refill-full")?.checked : null;
      this._last = html;
      this.shadowRoot.innerHTML = html;
      const restored = this.shadowRoot.querySelector(".refill-dialog");
      if (wasOpen && restored) {
        if (typed !== null) restored.querySelector("#refill-qty").value = typed;
        if (unit) restored.querySelector("#refill-unit").value = unit;
        if (full !== null) restored.querySelector("#refill-full").checked = full;
        restored.showModal();
      }
      this.shadowRoot.querySelectorAll("button[data-tab]").forEach(button => {
        button.addEventListener("click", () => {
          this._activeTab = button.dataset.tab;
          this._last = "";
          this.render();
        });
      });
      this.shadowRoot.querySelectorAll("button[data-reset-legacy]").forEach(button => {
        button.addEventListener("click", async () => {
          if (!window.confirm("Reset the old bag count? Detailed refill history is kept.")) return;
          try {
            await this._hass.callService("winnet_stove", "reset_legacy_bags", {
              entry_id: button.dataset.resetLegacy, confirm: true
            });
          } catch (error) { window.alert(String(error.message || error)); }
        });
      });
      this.shadowRoot.querySelectorAll("button[data-maint-kind]").forEach(button => {
        button.addEventListener("click", async () => {
          if (!window.confirm("Confirm this maintenance was completed?")) return;
          try {
            await this._hass.callService("winnet_stove", "complete_maintenance", {
              entry_id: button.dataset.entry, kind: button.dataset.maintKind,
              confirm: true
            });
          } catch (error) { window.alert(String(error.message || error)); }
        });
      });
      this.shadowRoot.querySelectorAll("button[data-refill-new]").forEach(button => {
        button.addEventListener("click", () => this.openRefillDialog({
          entry: button.dataset.refillNew,
          quantity: this._hass.states?.[
            stoves.find(s => s.entry_id === button.dataset.refillNew)?.entities?.pellet_setting_bag_weight_kg
          ]?.state || "15",
          weight: this._hass.states?.[
            stoves.find(s => s.entry_id === button.dataset.refillNew)?.entities?.pellet_setting_bag_weight_kg
          ]?.state || "15",
          unit: "kg",
          id: null,
          full: false
        }));
      });
      this.shadowRoot.querySelectorAll("button[data-refill-edit]").forEach(button => {
        button.addEventListener("click", () => this.openRefillDialog({
          entry: button.dataset.entry,
          id: button.dataset.refillEdit,
          full: button.dataset.full === "true",
          quantity: button.dataset.kg,
          weight: this._hass.states?.[
            stoves.find(s => s.entry_id === button.dataset.entry)?.entities?.pellet_setting_bag_weight_kg
          ]?.state || "15",
          unit: "kg"
        }));
      });
      this.shadowRoot.querySelectorAll("button[data-refill-delete]").forEach(button => {
        button.addEventListener("click", async () => {
          if (!window.confirm("Delete this refill? This cannot be undone.")) return;
          button.disabled = true;
          try {
            await this._hass.callService("winnet_stove", "remove_refill", {
              entry_id: button.dataset.entry,
              refill_id: button.dataset.refillDelete
            });
          } catch (error) {
            this._uiMessage = "Could not remove refill: " + String(error.message || error);
            this._last = "";
            this.render();
          } finally {
            button.disabled = false;
          }
        });
      });
      this.shadowRoot.querySelector("[data-refill-cancel]")?.addEventListener("click", () => {
        this._refillDraft = null;
        this._uiMessage = "";
        this._last = "";
        this.render();
      });
      this.shadowRoot.querySelector("[data-refill-save]")?.addEventListener("click", async (event) => {
        const button = event.currentTarget;
        const raw = Number(this.shadowRoot.querySelector("#refill-qty")?.value);
        const unit = this.shadowRoot.querySelector("#refill-unit")?.value;
        const kg = unit === "bags" ? raw * Number(this._refillDraft.weight) : raw;
        if (!Number.isFinite(kg) || kg <= 0 || kg > 500) {
          this._uiMessage = "Enter a quantity between 0 and 500 kg.";
          this.shadowRoot.querySelector(".refill-error").textContent = this._uiMessage;
          return;
        }
        button.disabled = true;
        try {
          const service = this._refillDraft.id ? "edit_refill" : "record_refill";
          const data = {
            entry_id: this._refillDraft.entry,
            quantity_kg: kg,
            full_hopper: this.shadowRoot.querySelector("#refill-full")?.checked === true
          };
          if (this._refillDraft.id) data.refill_id = this._refillDraft.id;
          await this._hass.callService("winnet_stove", service, data);
          this._refillDraft = null;
          this._uiMessage = "";
          this._last = "";
          this.render();
        } catch (error) {
          button.disabled = false;
          this._uiMessage = "Could not save refill: " + String(error.message || error);
          this.shadowRoot.querySelector(".refill-error").textContent = this._uiMessage;
        }
      });
      this.shadowRoot.querySelectorAll("button[data-info]").forEach(button => {
        button.addEventListener("click", () => {
          this.dispatchEvent(new CustomEvent("hass-more-info", {
            detail: { entityId: button.dataset.info },
            bubbles: true,
            composed: true,
          }));
        });
      });
      this.shadowRoot.querySelectorAll("button[data-button]").forEach(button => {
        button.addEventListener("click", async () => {
          if (button.disabled) return;
          button.disabled = true;
          try {
            await this._hass.callService("button", "press", {
              entity_id: button.dataset.button,
            });
          } catch (error) {
            this._hass?.showToast?.({ message: "Cannot log the pellet bag" });
          } finally {
            button.disabled = false;
          }
        });
      });
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
  openRefillDialog(draft) {
    this._refillDraft = draft;
    this._uiMessage = "";
    this._last = "";
    this.render();
    this.shadowRoot.querySelector(".refill-dialog")?.showModal();
  }
}
customElements.define("winnet-stove-panel", WinetStovePanel);
