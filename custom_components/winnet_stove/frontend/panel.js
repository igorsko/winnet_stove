/* SPDX-License-Identifier: GPL-3.0-only */
/** WiNET Stove — independent Home Assistant side panel. No external UI libraries. */

// Panel translations are separate from Home Assistant's backend entity names.
// English is the fallback for every language other than Italian.
const WINET_LABELS = {
  "en": {
    "subtitle": "SMART HEATING",
    "control": "Control",
    "consumption": "Consumption",
    "refills": "Refills",
    "maintenance": "Maintenance",
    "settings": "Settings",
    "lovelace": "Lovelace dashboard",
    "notAvailable": "Unavailable",
    "notConfigured": "Not configured",
    "working": "Running",
    "off": "Off",
    "starting": "Starting",
    "stopping": "Stopping",
    "unavailable": "Offline",
    "heating": "Heating active",
    "roomTemp": "Room temperature",
    "state": "Stove status",
    "power": "Power",
    "fan": "Fan",
    "wifi": "Wi-Fi signal",
    "alarm": "Alarms",
    "schedule": "Schedule",
    "on": "Turn on stove",
    "offButton": "Turn off stove",
    "confirmOn": "Confirm starting the stove?",
    "confirmOff": "Confirm turning off the stove?",
    "commandError": "Could not send command to stove",
    "noDevice": "No WiNET Stove device available",
    "technical": "Technical details",
    "todayHours": "Burning today",
    "allHours": "Total stove hours",
    "bagsLoaded": "Recorded bags",
    "estimatedUsed": "Estimated pellet used",
    "estimatedBags": "Estimated bags used",
    "autoRefill": "Automatic refill",
    "bagsHour": "Estimated bags/hour",
    "hoursBag": "Estimated hours/bag",
    "todayKg": "Estimated pellet today",
    "todayCost": "Estimated cost today",
    "monthCost": "Estimated cost this month",
    "rate": "Estimated average rate",
    "costsTitle": "Consumption and costs",
    "dataNote": "Pellet consumption and costs are estimates, not direct measurements.",
    "setupTitle": "Configure pellet consumption",
    "setupHelp": "To estimate consumption, enter an average kg/h rate or record two refills returning the hopper to the same full level.",
    "setupCta": "Configure consumption",
    "lastDays": "Last 10 days",
    "powerHours": "Burning hours per power level",
    "noDaily": "Burning history will appear after valid measurements.",
    "noPower": "No power samples available",
    "level": "Level",
    "h": "h",
    "refillTitle": "Your refills",
    "refillHelp": "Record how much pellet you place in the hopper. Automatically inferred refills can be corrected.",
    "recordRefill": "Record refill",
    "recorded": "Pellet recorded",
    "recent": "recent entries",
    "noneRefill": "No refills recorded.",
    "manual": "Manual",
    "autoInferred": "Automatic · inferred",
    "full": "Hopper full",
    "edit": "Edit",
    "delete": "Delete",
    "deleteConfirm": "Delete this refill? This cannot be undone.",
    "deleteError": "Could not delete refill",
    "editRefill": "Correct refill",
    "amount": "Quantity",
    "bags": "Bags",
    "fullOption": "Hopper returned to the same full level",
    "fullHelp": "Check only when the hopper is actually at the same full level; this helps calibrate consumption.",
    "bagEq": "One bag equals",
    "save": "Save",
    "cancel": "Cancel",
    "invalidQty": "Enter a valid quantity between 0.001 and 500 kg.",
    "saveError": "Could not save refill",
    "maintTitle": "Maintenance",
    "maintHelp": "Reminders based on observed burning hours. Always follow the manufacturer's instructions.",
    "burner": "Burner cleaning",
    "deep": "Deep cleaning",
    "annual": "Periodic servicing",
    "dueIn": "Due in",
    "overdue": "Overdue by",
    "hours": "hours",
    "completed": "Mark as completed",
    "completeConfirm": "Confirm this maintenance was completed?",
    "settingsTitle": "Settings",
    "settingsHelp": "Tap a value to edit it. Consumption settings do not change the stove's physical operation.",
    "pelletGroup": "Pellet and prices",
    "calibrationGroup": "Consumption calibration",
    "maintGroup": "Maintenance intervals",
    "diagnosticsGroup": "Diagnostics and historical data",
    "initialHours": "Initial stove hours",
    "bagWeight": "Bag weight",
    "avgRate": "Average consumption",
    "stock": "Bags in stock",
    "bagPrice": "Price per bag",
    "burnerInterval": "Burner cleaning interval",
    "deepInterval": "Deep cleaning interval",
    "annualInterval": "Periodic service interval",
    "powerRate": "Consumption at level",
    "resetBags": "Reset historical bag counter",
    "resetHelp": "Does not delete detailed refill history.",
    "resetConfirm": "Reset historical bag counter? Detailed refills will be kept.",
    "connection": "Connection",
    "connected": "Connected",
    "connectionDetails": "Connection details",
    "unknown": "Unknown",
    "configured": "Configured",
    "unconfigured": "Unconfigured",
    "sourceManual": "User-defined average",
    "sourceFull": "Calibrated from refills",
    "sourcePower": "Calibrated per power level",
    "estimated": "Estimated",
    "measured": "Observed",
    "legacy": "Historical"
  },
  "it": {
    "subtitle": "RISCALDAMENTO INTELLIGENTE",
    "control": "Controllo",
    "consumption": "Consumi",
    "refills": "Rifornimenti",
    "maintenance": "Manutenzione",
    "settings": "Impostazioni",
    "lovelace": "Dashboard Lovelace",
    "notAvailable": "Non disponibile",
    "notConfigured": "Da configurare",
    "working": "In funzione",
    "off": "Spenta",
    "starting": "In avvio",
    "stopping": "In spegnimento",
    "unavailable": "Non raggiungibile",
    "heating": "Riscaldamento attivo",
    "roomTemp": "Temperatura ambiente",
    "state": "Stato",
    "power": "Potenza",
    "fan": "Ventola",
    "wifi": "Segnale Wi-Fi",
    "alarm": "Allarmi",
    "schedule": "Programmazione",
    "on": "Accendi stufa",
    "offButton": "Spegni stufa",
    "confirmOn": "Confermi l'accensione della stufa?",
    "confirmOff": "Confermi lo spegnimento della stufa?",
    "commandError": "Impossibile inviare il comando alla stufa",
    "noDevice": "Nessuna stufa WiNET disponibile",
    "technical": "Dettagli tecnici",
    "todayHours": "Combustione oggi",
    "allHours": "Ore totali",
    "bagsLoaded": "Sacchi registrati",
    "estimatedUsed": "Pellet consumato (stima)",
    "estimatedBags": "Sacchi consumati (stima)",
    "autoRefill": "Rifornimento automatico",
    "bagsHour": "Sacchi/ora stimati",
    "hoursBag": "Ore per sacco stimate",
    "todayKg": "Pellet oggi (stima)",
    "todayCost": "Costo oggi (stima)",
    "monthCost": "Costo del mese (stima)",
    "rate": "Consumo medio stimato",
    "costsTitle": "Consumi e costi",
    "dataNote": "I consumi e i costi sono stime, non misurazioni dirette.",
    "setupTitle": "Configura il consumo del pellet",
    "setupHelp": "Per calcolare il consumo, inserisci un valore medio in kg/ora oppure registra due rifornimenti allo stesso livello di pieno.",
    "setupCta": "Configura i consumi",
    "lastDays": "Ultimi 10 giorni",
    "powerHours": "Ore per livello di potenza",
    "noDaily": "Le ore saranno disponibili dopo la prima combustione rilevata.",
    "noPower": "Nessun campione di potenza disponibile",
    "level": "Livello",
    "h": "h",
    "refillTitle": "I tuoi rifornimenti",
    "refillHelp": "Registra il pellet versato nel serbatoio. I rifornimenti automatici sono presunti e possono essere corretti.",
    "recordRefill": "Registra rifornimento",
    "recorded": "Pellet registrato",
    "recent": "registrazioni recenti",
    "noneRefill": "Nessun rifornimento registrato.",
    "manual": "Manuale",
    "autoInferred": "Automatico · presunto",
    "full": "Serbatoio pieno",
    "edit": "Modifica",
    "delete": "Elimina",
    "deleteConfirm": "Eliminare questo rifornimento? L'operazione non può essere annullata.",
    "deleteError": "Impossibile eliminare il rifornimento",
    "editRefill": "Correggi rifornimento",
    "amount": "Quantità",
    "bags": "Sacchi",
    "fullOption": "Serbatoio riportato allo stesso livello di pieno",
    "fullHelp": "Seleziona solo se il serbatoio è stato davvero riportato allo stesso livello: aiuta a calibrare i consumi.",
    "bagEq": "Un sacco equivale a",
    "save": "Salva",
    "cancel": "Annulla",
    "invalidQty": "Inserisci una quantità valida tra 0,001 e 500 kg.",
    "saveError": "Impossibile salvare il rifornimento",
    "maintTitle": "Manutenzione",
    "maintHelp": "Promemoria calcolati sulle ore rilevate. Segui sempre le istruzioni del produttore.",
    "burner": "Pulizia braciere",
    "deep": "Pulizia approfondita",
    "annual": "Manutenzione periodica",
    "dueIn": "Tra",
    "overdue": "In ritardo di",
    "hours": "ore",
    "completed": "Segna come eseguita",
    "completeConfirm": "Confermi di aver eseguito questa manutenzione?",
    "settingsTitle": "Impostazioni",
    "settingsHelp": "Tocca un valore per modificarlo. I parametri di consumo non cambiano il funzionamento della stufa.",
    "pelletGroup": "Pellet e prezzi",
    "calibrationGroup": "Calibrazione consumi",
    "maintGroup": "Intervalli di manutenzione",
    "diagnosticsGroup": "Diagnostica e dati storici",
    "initialHours": "Ore iniziali stufa",
    "bagWeight": "Peso del sacco",
    "avgRate": "Consumo medio",
    "stock": "Sacchi in magazzino",
    "bagPrice": "Prezzo per sacco",
    "burnerInterval": "Intervallo pulizia braciere",
    "deepInterval": "Intervallo pulizia approfondita",
    "annualInterval": "Intervallo manutenzione periodica",
    "powerRate": "Consumo al livello",
    "resetBags": "Azzera contatore storico sacchi",
    "resetHelp": "Non elimina le registrazioni dettagliate dei rifornimenti.",
    "resetConfirm": "Azzerare il contatore storico dei sacchi? I rifornimenti dettagliati saranno conservati.",
    "connection": "Connessione",
    "connected": "Connessa",
    "connectionDetails": "Dettagli connessione",
    "unknown": "Sconosciuto",
    "configured": "Configurato",
    "unconfigured": "Non configurato",
    "sourceManual": "Media impostata",
    "sourceFull": "Calibrato tramite rifornimenti",
    "sourcePower": "Calibrato per livello di potenza",
    "estimated": "Stimato",
    "measured": "Rilevato",
    "legacy": "Storico"
  }
};

class WinetStovePanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._last = "";
    this._activeTab = "control";
    this._refillDraft = null;
    this._uiMessage = "";
    this._advancedOpen = false;
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

  get locale() {
    const locale = this._hass?.locale?.language || this._hass?.language || "en";
    return locale.toLowerCase().startsWith("it") ? "it" : "en";
  }

  tr(key) {
    return WINET_LABELS[this.locale][key] || WINET_LABELS.en[key] || key;
  }

  displayName(title, index) {
    // Avoid presenting network addresses as the main device name.
    const clean = String(title || "").replace(/\\s*\\([^)]*(?:\\d{1,3}\\.){3}\\d{1,3}[^)]*\\)/g, "").trim();
    return clean || "WiNET Stove " + (index + 1);
  }

  duration(hours) {
    if (hours === null || hours === undefined || !Number.isFinite(Number(hours))) return "—";
    const minutes = Math.max(0, Math.round(Number(hours) * 60));
    return `${Math.floor(minutes / 60)} h ${String(minutes % 60).padStart(2, "0")} min`;
  }

  stateLabel(state) {
    const label = ({heat:"heating", off:"off", unavailable:"unavailable",
      unknown:"unknown"})[state];
    return label ? this.tr(label) : state;
  }

  sourceLabel(source) {
    return ({
      full_hopper_calibration: this.tr("sourceFull"),
      user_average: this.tr("sourceManual"),
      configured_power_profile: this.tr("sourcePower"),
      unconfigured: this.tr("unconfigured"),
    })[source] || this.tr("unconfigured");
  }

  format(entityId) {
    const entity = this._hass?.states?.[entityId];
    if (!entity) return "—";
    if (entity.state === "unavailable" || entity.state === "unknown") return this.tr("notAvailable");
    const units = entity.attributes?.unit_of_measurement;
    const translations = this.locale === "it"
      ? {"In Funzione":"In funzione", "Spento":"Spenta", "Avvio":"In avvio",
         "Arresto":"In spegnimento", "Nessun Allarme":"Nessun allarme",
         "Disattivo":"Disattivato", "Connected":"Connessa"}
      : {"In Funzione":"Running", "Spento":"Off", "Avvio":"Starting",
         "Arresto":"Stopping", "Nessun Allarme":"No alarms",
         "Disattivo":"Disabled", "Connected":"Connected"};
    if (Object.hasOwn(translations, entity.state)) return translations[entity.state];
    if (entity.state === "on" && entityId?.startsWith("switch.")) return this.tr("configured");
    if (entity.state === "off" && entityId?.startsWith("switch.")) return this.tr("off");
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
        [this.tr("state"), m.state], [this.tr("power"), m.power],
        [this.tr("fan"), m.fan], [this.tr("wifi"), m.rssi],
        [this.tr("alarm"), m.alarm], [this.tr("schedule"), m.crono]
      ];
      const rows = keys.filter(([_, id]) => id).map(([label, id]) =>
        `<div class="metric"><span>${this.escape(label)}</span><strong>${this.format(id)}</strong></div>`
      ).join("");
      const primaryKeys = keys.filter(([label]) =>
        [this.tr("state"), this.tr("power"), this.tr("fan"), this.tr("alarm"), this.tr("schedule")].includes(label)
      );
      const primaryRows = primaryKeys.filter(([_, id]) => id).map(([label,id]) =>
        `<div class="metric"><span>${this.escape(label)}</span><strong>${this.format(id)}</strong></div>`
      ).join("");
      const todayRunning = m.insights_today_hours
        ? this.duration(this._hass.states?.[m.insights_today_hours]?.state)
        : "—";
      const buttons = climate && mode !== "unavailable" && mode !== "unknown" ? `
        <div class="controls main-action">
          <button data-climate="${this.escape(climate)}" data-mode="${isOn ? "off" : "heat"}"
            class="${isOn ? "secondary" : ""}">
            ${isOn ? this.tr("offButton") : this.tr("on")}
          </button>
        </div>` : "";
      const pelletMetrics = [
        [this.tr("allHours"), m.pellet_total_hours],
        [this.tr("bagsLoaded"), m.pellet_bags_loaded],
        [this.tr("estimatedUsed"), m.pellet_pellet_used],
        [this.tr("estimatedBags"), m.pellet_estimated_bags],
        [this.tr("autoRefill"), m.pellet_auto_refill],
        [this.tr("bagsHour"), m.pellet_bags_per_hour],
        [this.tr("hoursBag"), m.pellet_hours_per_bag],
        [this.tr("todayKg"), m.insights_today_pellet],
        [this.tr("todayCost"), m.insights_today_cost],
        [this.tr("monthCost"), m.insights_month_cost],
        [this.tr("rate"), m.insights_effective_rate]
      ];
      const pelletNumbers = [
        [this.tr("initialHours"), m.pellet_setting_initial_hours],
        [this.tr("bagWeight"), m.pellet_setting_bag_weight_kg],
        [this.tr("avgRate"), m.pellet_setting_rate_kg_h],
        [this.tr("stock"), m.pellet_setting_bags_in_stock],
        [this.tr("bagPrice"), m.pellet_setting_price_per_bag],
        [this.tr("burnerInterval"), m.maintenance_interval_burner],
        [this.tr("deepInterval"), m.maintenance_interval_deep_clean],
        [this.tr("annualInterval"), m.maintenance_interval_annual_service],
        [`${this.tr("powerRate")} 1 (kg/h)`, m.power_rate_1],
        [`${this.tr("powerRate")} 2 (kg/h)`, m.power_rate_2],
        [`${this.tr("powerRate")} 3 (kg/h)`, m.power_rate_3],
        [`${this.tr("powerRate")} 4 (kg/h)`, m.power_rate_4],
        [`${this.tr("powerRate")} 5 (kg/h)`, m.power_rate_5]
      ];
      const pelletReadings = pelletMetrics.filter(([_, id]) => id).map(([label, id]) =>
        `<div class="metric"><span>${this.escape(label)}</span><strong>${this.format(id)}</strong></div>`
      ).join("");
      const makeSettings = (items) => items.filter(([_, id]) => id).map(([label, id]) => {
        const entity = this._hass.states?.[id];
        const unsetRate = (label === this.tr("avgRate") || label.startsWith(this.tr("powerRate")))
          && entity && Number(entity.state) === 0;
        return `<button class="setting" data-info="${this.escape(id)}">
          <span>${this.escape(label)}</span>
          <strong>${unsetRate ? this.tr("notConfigured") : this.format(id)}</strong>
        </button>`;
      }).join("");
      const pelletSettings = makeSettings(pelletNumbers);
      const ledger = m.pellet_refill_log
        ? this._hass.states?.[m.pellet_refill_log]?.attributes || {}
        : {};
      const refills = Array.isArray(ledger.events) ? ledger.events : [];
      const refillRows = refills.map(event => {
        const label = event.source === "auto" ? this.tr("autoInferred") : this.tr("manual");
        const date = new Date(event.at);
        const when = Number.isNaN(date.valueOf())
          ? "—" : date.toLocaleString(this.locale === "it" ? "it-IT" : "en-GB");
        return `<div class="refill-row">
          <div><strong>${this.escape(event.kg)} kg</strong>
            <small>${this.escape(label)} · ${this.escape(when)}</small></div>
          <div class="row-actions">
            <button class="secondary mini" data-refill-edit="${this.escape(event.id)}"
              data-entry="${this.escape(stove.entry_id)}"
              data-kg="${this.escape(event.kg)}"
            data-full="${event.full_hopper ? "true" : "false"}">${this.tr("edit")}</button>
            <button class="secondary mini" data-refill-delete="${this.escape(event.id)}"
              data-entry="${this.escape(stove.entry_id)}">${this.tr("delete")}</button>
          </div>
        </div>`;
      }).join("");
      const refillCard = stove.entry_id ? `
        <div class="refill-manager">
          <div class="refill-head"><div><h4>${this.tr("refillTitle")}</h4>
          <p class="hint">${this.tr("refillHelp")}</p></div>
          <button data-refill-new="${this.escape(stove.entry_id)}">${this.tr("recordRefill")}</button></div>
          <p class="refill-error" role="alert">${this.escape(this._refillDraft ? "" : this._uiMessage)}</p>
          <div class="refill-summary">
            ${this.tr("recorded")}: <strong>${this.escape(ledger.total_kg ?? "0")} kg</strong>
            · ${this.escape(refills.length)} ${this.tr("recent")}
          </div>
          ${refillRows || `<p class="hint">${this.tr("noneRefill")}</p>`}
        </div>` : "";
      const maintenance = [
        [this.tr("burner"), "burner", m.insights_maintenance_burner],
        [this.tr("deep"), "deep_clean", m.insights_maintenance_deep_clean],
        [this.tr("annual"), "annual_service", m.insights_maintenance_annual_service]
      ].map(([title, key, id]) => {
        const obj = this._hass.states?.[id];
        const remaining = Number(obj?.state);
        const threshold = Number(obj?.attributes?.interval_hours);
        const valid = obj && Number.isFinite(remaining) && Number.isFinite(threshold) && threshold > 0
          && obj.state !== "unavailable" && obj.state !== "unknown";
        const percent = valid ? Math.min(100, Math.max(0, 100 * (threshold - remaining) / threshold)) : 0;
        const label = !valid ? this.tr("notAvailable") : remaining < 0
          ? this.tr("overdue") + " " + this.duration(Math.abs(remaining))
          : this.tr("dueIn") + " " + this.duration(remaining);
        return `<div class="maintenance-item">
          <div class="maintenance-main">
            <strong>${this.escape(title)}</strong>
            <small>${this.escape(label)}</small>
            ${valid ? `<div class="progress"><div style="width:${percent.toFixed(2)}%"></div></div>` : ""}
          </div>
          <button class="secondary" data-maint-kind="${this.escape(key)}"
            data-entry="${this.escape(stove.entry_id)}">${this.tr("completed")}</button>
        </div>`;
      }).join("");
      const fullRateId = m.insights_effective_rate;
      const rateSource = fullRateId
        ? this._hass.states?.[fullRateId]?.attributes?.source
        : null;
      const dailyHistory = m.insights_month_cost
        ? this._hass.states?.[m.insights_month_cost]?.attributes?.daily_history || []
        : [];
      const dailyRows = dailyHistory.slice(-10).reverse().map(day =>
        `<div class="refill-row"><span>${this.escape(day.date)}</span>
          <strong>${this.duration(day.working_h)} ·
          ${day.estimated_kg == null ? "—" : this.escape(day.estimated_kg) + " kg"} ·
          ${day.estimated_cost == null ? "—" : this.escape(day.estimated_cost) + " €"}</strong>
        </div>`).join("");
      const powerData = m.insights_power_profile
        ? this._hass.states?.[m.insights_power_profile]?.attributes?.power_hours || {}
        : {};
      const powerRows = Object.entries(powerData).map(([key, hours]) =>
        `<div class="metric"><span>${this.tr("level")} ${this.escape(key)}</span>
        <strong>${this.duration(hours)}</strong></div>`).join("");
      const temp = current?.attributes?.current_temperature;
      return `
        <section class="stove">
          <div class="top">
            <div><h2>${this.escape(this.displayName(stove.title, index))}</h2></div>
            <span class="status ${isOn ? "on" : ""}">${this.escape(this.stateLabel(mode))}</span>
          </div>
          <section class="tab-content" ${this._activeTab !== "control" ? "hidden" : ""}>
            <div class="control-hero">
              <div class="temperature">
                <span>${this.tr("roomTemp")}</span>
                <strong>${temp == null ? "—" : this.escape(temp) + " °C"}</strong>
                <small>${this.tr("todayHours")}: ${todayRunning}</small>
              </div>
              <div class="primary-control">${buttons}</div>
            </div>
            <div class="metrics key-metrics">${primaryRows}</div>
            <details class="more-info"><summary>${this.tr("technical")}</summary>
              <div class="metrics">${rows}</div>
            </details>
          </section>
          <section class="tab-content" ${this._activeTab !== "consumption" ? "hidden" : ""}>
            <div class="section-intro">
              <h3>${this.tr("costsTitle")}</h3>
              <p class="hint">${this.tr("dataNote")}</p>
            </div>
            <div class="metrics overview">
              ${[
                [this.tr("todayHours"), m.insights_today_hours, true],
                [this.tr("allHours"), m.pellet_total_hours, true],
                [this.tr("todayKg"), m.insights_today_pellet],
                [this.tr("todayCost"), m.insights_today_cost],
              ].filter(([_, id]) => id).map(([name,id,time]) =>
                `<div class="metric">
                  <span>${this.escape(name)}</span>
                  <strong>${time ? this.duration(this._hass.states?.[id]?.state) : this.format(id)}</strong>
                </div>`).join("")}
            </div>
            ${(!rateSource || rateSource === "unconfigured") ? `
              <div class="setup-callout">
                <strong>${this.tr("setupTitle")}</strong>
                <p>${this.tr("setupHelp")}</p>
                <button data-go-settings>${this.tr("setupCta")}</button>
              </div>` : `
              <p class="hint">${this.tr("rate")}: ${this.format(m.insights_effective_rate)}
                · ${this.sourceLabel(rateSource)}</p>`}
            <h4>${this.tr("lastDays")}</h4>
            ${dailyRows || `<p class="hint">${this.tr("noDaily")}</p>`}
            <details class="more-info"><summary>${this.tr("technical")}</summary>
              <div class="metrics">${pelletReadings}</div>
              <h4>${this.tr("powerHours")}</h4>
              <div class="metrics">${powerRows || `<p class="hint">${this.tr("noPower")}</p>`}</div>
            </details>
          </section>
          <section class="tab-content" ${this._activeTab !== "refills" ? "hidden" : ""}>
            ${refillCard}
          </section>
          <section class="tab-content" ${this._activeTab !== "maintenance" ? "hidden" : ""}>
            <h3>${this.tr("maintTitle")}</h3>
            <p class="hint">${this.tr("maintHelp")}</p>
            ${maintenance}
          </section>
          <section class="tab-content" ${this._activeTab !== "settings" ? "hidden" : ""}>
            <h3>${this.tr("settingsTitle")}</h3>
            <p class="hint">${this.tr("settingsHelp")}</p>
            <div class="setting-section"><h4>${this.tr("pelletGroup")}</h4>
              <div class="settings">${makeSettings(pelletNumbers.slice(0,5))}</div>
            </div>
            <details class="more-info"><summary>${this.tr("calibrationGroup")}</summary>
              <p class="hint">${this.tr("fullHelp")}</p>
              <div class="settings">${makeSettings(pelletNumbers.slice(8))}</div>
            </details>
            <details class="more-info"><summary>${this.tr("maintGroup")}</summary>
              <div class="settings">${makeSettings(pelletNumbers.slice(5,8))}</div>
            </details>
            <details class="more-info"><summary>${this.tr("diagnosticsGroup")}</summary>
              <div class="controls">
                <button class="secondary" data-info="${this.escape(m.diagnostics_connection || "")}">
                  ${this.tr("connectionDetails")}: ${m.diagnostics_connection ? this.format(m.diagnostics_connection) : "—"}
                </button>
                <button class="secondary" data-reset-legacy="${this.escape(stove.entry_id)}">
                  ${this.tr("resetBags")}
                </button>
              </div>
              <p class="hint">${this.tr("resetHelp")}</p>
            </details>
          </section>
        </section>`;
    }).join("");
    const draft = this._refillDraft;
    const modal = draft ? `
      <dialog class="refill-dialog" aria-label="Refill editor">
        <h3>${draft.id ? this.tr("editRefill") : this.tr("recordRefill")}</h3>
        <p class="hint">${this.tr("refillHelp")}</p>
        <label for="refill-qty">${this.tr("amount")}</label>
        <div class="refill-input">
          <input id="refill-qty" type="number" min="0.001" step="any"
            value="${this.escape(draft.quantity)}" required>
          <select id="refill-unit">
            <option value="kg" ${draft.unit === "kg" ? "selected" : ""}>kg</option>
            <option value="bags" ${draft.unit === "bags" ? "selected" : ""}>${this.tr("bags")}</option>
          </select>
        </div>
        <label class="full-check"><input type="checkbox" id="refill-full" ${draft.full ? "checked" : ""}> ${this.tr("fullOption")}</label>
        <p class="hint">${this.tr("bagEq")} ${this.escape(draft.weight)} kg. ${this.tr("fullHelp")}</p>
        <p class="refill-error" role="alert">${this.escape(this._uiMessage)}</p>
        <div class="controls">
          <button data-refill-save>${this.tr("save")}</button>
          <button class="secondary" data-refill-cancel>${this.tr("cancel")}</button>
        </div>
      </dialog>` : "";
    const html = `
      <style>
        :host { display: block; color: var(--primary-text-color); background: var(--primary-background-color); min-height: 100%; }
        * { box-sizing: border-box; }
        .wrap { max-width: 1120px; margin: 0 auto; padding: 24px 20px 64px; font-family: var(--paper-font-body1_-_font-family, sans-serif); }
        .tab-content[hidden] { display:none !important; }
        .control-hero {display:flex;align-items:center;justify-content:space-between;gap:20px;
          padding:18px 0 24px;flex-wrap:wrap;}
        .control-hero .temperature {padding:0;}
        .control-hero .temperature strong {font-size:clamp(38px,7vw,62px);}
        .control-hero .temperature small {font-size:13px;color:var(--secondary-text-color);}
        .primary-control .controls {margin:0;}
        .primary-control button {min-height:48px;}
        .section-intro h3 {font-size:21px;margin:0 0 7px;}
        .overview {grid-template-columns:repeat(2,minmax(0,1fr));margin:18px 0 22px;}
        .overview .metric {min-height:105px;justify-content:center;}
        .overview .metric strong {font-size:clamp(18px,3vw,26px);font-variant-numeric:tabular-nums;}
        .more-info {margin-top:20px;border:1px solid var(--divider-color);border-radius:12px;padding:14px;}
        .more-info summary {cursor:pointer;font-weight:600;list-style-position:inside;}
        .more-info[open] summary {margin-bottom:16px;}
        .more-info summary:focus-visible,button:focus-visible,a:focus-visible {
          outline:2px solid var(--primary-color);outline-offset:3px;}
        .setup-callout {border:1px solid var(--divider-color);border-radius:13px;padding:20px;
          margin:16px 0 24px;display:flex;flex-direction:column;align-items:flex-start;gap:10px;}
        .setup-callout p {margin:0;color:var(--secondary-text-color);font-size:14px;line-height:1.6;}
        .setting-section {margin:23px 0;}
        .setting-section h4 {margin:0 0 8px;}
        .maintenance-main {flex:1;display:flex;flex-direction:column;gap:8px;min-width:0;}
        .progress {height:5px;background:var(--secondary-background-color);border-radius:999px;
          overflow:hidden;width:100%;}
        .progress>div {height:100%;background:var(--primary-color);border-radius:999px;}
        .maintenance-item small {font-size:13px;}
        .stove .top h2 {margin:0;font-size:18px;}
        .stove .top {margin-bottom:15px;}
        .hint {font-size:13px;}
        .tabs button {min-height:42px;}
        button {min-height:40px;}
        .key-metrics {margin:4px 0;}
        .refill-manager {border:0;margin:0;padding:0;}
        .refill-row strong {font-variant-numeric:tabular-nums;}
        @media(max-width:600px) {
          .overview {grid-template-columns:repeat(2,minmax(0,1fr));}
          .control-hero {align-items:flex-start;}
          .maintenance-item {flex-wrap:wrap;}
          .maintenance-item button {width:100%;}
          .refill-row {align-items:flex-start;}
        }
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
          <div><span class="eyebrow">${this.tr("subtitle")}</span><h1>WiNET Stove</h1></div>
          ${this._panel.config?.lovelace_available ?
            `<a class="small-link" href="/winnet-stove-dashboard">${this.tr("lovelace")}</a>` : ""}
        </div>
        <nav class="tabs" aria-label="WiNET Stove">
          ${[
            ["control", this.tr("control")], ["consumption", this.tr("consumption")],
            ["refills", this.tr("refills")], ["maintenance", this.tr("maintenance")],
            ["settings", this.tr("settings")],
          ].map(([id,label]) => `<button data-tab="${id}" class="${this._activeTab===id ? "selected" : ""}"
             aria-current="${this._activeTab===id ? "page" : "false"}">${label}</button>`).join("")}
        </nav>
        ${blocks || `<p class="empty">${this.tr("noDevice")}</p>`}
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
      this.shadowRoot.querySelectorAll("button[data-go-settings]").forEach(button => {
        button.addEventListener("click", () => {
          this._activeTab = "settings";
          this._last = "";
          this.render();
        });
      });
      this.shadowRoot.querySelectorAll("button[data-tab]").forEach(button => {
        button.addEventListener("click", () => {
          this._activeTab = button.dataset.tab;
          this._last = "";
          this.render();
        });
      });
      this.shadowRoot.querySelectorAll("button[data-reset-legacy]").forEach(button => {
        button.addEventListener("click", async () => {
          if (!window.confirm(this.tr("resetConfirm"))) return;
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
            this._uiMessage = this.tr("deleteError") + ": " + String(error.message || error);
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
          this._uiMessage = this.tr("invalidQty");
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
          this._uiMessage = this.tr("saveError") + ": " + String(error.message || error);
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
          if (!window.confirm(this.tr(button.dataset.mode === "off" ? "confirmOff" : "confirmOn"))) return;
          button.disabled = true;
          try {
            await this._hass.callService("climate", "set_hvac_mode", {
              entity_id: button.dataset.climate,
              hvac_mode: button.dataset.mode
            });
          } catch (error) {
            this._hass?.showToast?.({message: this.tr("commandError")});
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
