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
    "cronoTitle": "Weekly schedule (Crono)",
    "cronoOn": "Enabled",
    "cronoOff": "Disabled",
    "cronoEnable": "Enable Crono",
    "cronoDisable": "Disable Crono",
    "cronoConfirmOn": "Enable the stove’s saved weekly program?",
    "cronoConfirmOff": "Disable the stove’s weekly program?",
    "cronoError": "Could not change the Crono schedule",
    "pilotTarget": "Target temperature",
    "pilotPower": "Burner power",
    "pilotFan": "Air fan",
    "pilotError": "The stove did not accept the setting",
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
    "cronoTitle": "Programmazione oraria (Crono)",
    "cronoOn": "Attiva",
    "cronoOff": "Disattivata",
    "cronoEnable": "Attiva Crono",
    "cronoDisable": "Disattiva Crono",
    "cronoConfirmOn": "Attivare il programma settimanale già salvato sulla stufa?",
    "cronoConfirmOff": "Disattivare la programmazione oraria della stufa?",
    "cronoError": "Impossibile modificare la programmazione Crono",
    "pilotTarget": "Temperatura obiettivo",
    "pilotPower": "Potenza della stufa",
    "pilotFan": "Ventola aria",
    "pilotError": "La stufa non ha accettato la regolazione",
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

const WINET_ICONS = {"power":"<path d=\"M12 2v10M6.5 5.5a9 9 0 1 0 11 0\"/>","flame":"<path d=\"M12 22c5 0 8-3 8-7.5 0-3.4-2-6.4-5.3-9.5 0 3.1-1.2 4.7-2.6 5.5C12 6.8 10.7 3.8 8 2c.7 4-1.1 6.2-2.8 8.7C2.3 15.3 6 22 12 22Z\"/>","temperature":"<path d=\"M14 14.6V5a3 3 0 0 0-6 0v9.6a5 5 0 1 0 6 0ZM11 10v8\"/>","bars":"<rect x=\"3\" y=\"14\" width=\"4\" height=\"7\" rx=\"1\"/><rect x=\"10\" y=\"9\" width=\"4\" height=\"12\" rx=\"1\"/><rect x=\"17\" y=\"3\" width=\"4\" height=\"18\" rx=\"1\"/>","fan":"<circle cx=\"12\" cy=\"12\" r=\"2\"/><path d=\"M12 10c-1.5-6-7-6-8-2-1 4 3 6 6 4M14 12c6-1 7 5 3 7-3 2-6-1-5-5M11 14c-4 4-9 2-8-2 1-4 5-5 7-2\"/>","clock":"<circle cx=\"12\" cy=\"12\" r=\"9\"/><path d=\"M12 7v5l3 2\"/>","shield":"<path d=\"M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Zm-3-10 2 2 4-4\"/>","alert":"<path d=\"m12 3 10 18H2L12 3ZM12 9v4m0 4v.2\"/>","wifi":"<path d=\"M2 8a16 16 0 0 1 20 0M5 12a11 11 0 0 1 14 0m-10.5 4a6 6 0 0 1 7 0M12 20h.01\"/>","package":"<path d=\"m12 2 9 5v10l-9 5-9-5V7l9-5Zm-9 5 9 5 9-5m-9 5v10\"/>","chart":"<path d=\"M3 3v18h18m-15-5 4-5 4 2 5-7\"/>","wrench":"<path d=\"M14 6a6 6 0 0 0-8 8L2 18l4 4 4-4a6 6 0 0 0 8-8l-4 4-4-4 4-4Z\"/>","settings":"<path d=\"M10 2h4l.7 2.3 2 1.2 2.3-.5 2 3.5-1.6 1.7v2.4l1.6 1.8-2 3.5-2.3-.5-2 1.2L14 21h-4l-.7-2.4-2-1.2-2.3.5-2-3.5 1.6-1.8v-2.4L3 8.5 5 5l2.3.5 2-1.2L10 2Z\"/><circle cx=\"12\" cy=\"11.5\" r=\"3\"/>","sliders":"<path d=\"M4 7h16M4 17h16\"/><circle cx=\"9\" cy=\"7\" r=\"2\" fill=\"none\"/><circle cx=\"16\" cy=\"17\" r=\"2\" fill=\"none\"/>","plus":"<path d=\"M12 5v14M5 12h14\"/>","check":"<path d=\"m5 12 4 4 10-10\"/>","pencil":"<path d=\"m3 17 11-11 4 4L7 21H3v-4ZM13 7l4 4\"/>","trash":"<path d=\"M4 7h16M10 4h4M6 7l1 14h10l1-14M10 11v6m4-6v6\"/>","info":"<circle cx=\"12\" cy=\"12\" r=\"10\"/><path d=\"M12 10v7M12 7v.01\"/>"};

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

  icon(name) {
    const path = WINET_ICONS[name] || WINET_ICONS.info;
    // Static allowlisted SVG geometry, never sourced from an HA entity.
    return `<svg class="ico" aria-hidden="true" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" stroke-width="1.9" stroke-linecap="round"
      stroke-linejoin="round">${path}</svg>`;
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
      const powerValue = m.power ? this.format(m.power) : "—";
      const powerLevel = Number(this._hass.states?.[m.power]?.state);
      const powerBars = Array.from({length:5}, (_,n) =>
        `<span class="${Number.isInteger(powerLevel) && powerLevel >= n + 1 ? "active" : ""}"></span>`
      ).join("");
      const fanValue = m.fan ? this.format(m.fan) : "—";
      const alarmRaw = this._hass.states?.[m.alarm]?.state?.toLowerCase() || "";
      const alarmOk = ["nessun allarme","no alarms","none","0","ok"].includes(alarmRaw);
      const alarmText = m.alarm ? this.format(m.alarm) : "—";
      const rssiValue = m.rssi ? this.format(m.rssi) : "—";
      const todayRunning = m.insights_today_hours
        ? this.duration(this._hass.states?.[m.insights_today_hours]?.state)
        : "—";
      const cronoId = m.crono_switch;
      const cronoState = cronoId ? this._hass.states?.[cronoId]?.state : null;
      const cronoAvailable = cronoState === "on" || cronoState === "off";
      const cronoEnabled = cronoState === "on";
      // Prefer dedicated writable entities while displaying actual sensor values.
      const powerControlId = m.pilot_power;
      const fanControlId = m.pilot_fan;
      const targetValue = Number(current?.attributes?.temperature);
      const controlStepper = (entityId, label, reading, min, max) => {
        const state = entityId ? this._hass.states?.[entityId]?.state : null;
        const value = Number(state);
        const ready = state != null && !["unknown", "unavailable"].includes(state)
          && Number.isInteger(value) && value >= min && value <= max;
        if (!entityId || !ready) return `<strong>${this.escape(reading)}</strong>`;
        return `<div class="inline-stepper" role="group" aria-label="${this.escape(label)}">
          <button type="button" class="secondary" data-pilot-step="${this.escape(entityId)}"
            data-pilot-value="${value - 1}" aria-label="${this.escape(label)}: −"
            ${value <= min ? "disabled" : ""}>−</button>
          <output aria-live="polite">${value}</output>
          <button type="button" class="secondary" data-pilot-step="${this.escape(entityId)}"
            data-pilot-value="${value + 1}" aria-label="${this.escape(label)}: +"
            ${value >= max ? "disabled" : ""}>+</button>
        </div>`;
      };
      const powerControl = controlStepper(powerControlId, this.tr("power"), powerValue, 1, 5);
      const fanControl = controlStepper(fanControlId, this.tr("fan"), fanValue, 1, 5);
      const targetValid = climate && current && Number.isFinite(targetValue)
        && targetValue >= 15 && targetValue <= 30 && Number.isInteger(targetValue * 2);
      const targetControl = targetValid
        ? `<div class="target-control"><span class="subtle">${this.tr("pilotTarget")}</span>
          <div class="inline-stepper" role="group" aria-label="${this.tr("pilotTarget")}">
            <button type="button" class="secondary" data-pilot-temp="${targetValue - 0.5}"
              data-pilot-climate="${this.escape(climate)}" aria-label="${this.tr("pilotTarget")}: −"
              ${targetValue <= 15 ? "disabled" : ""}>−</button>
            <output aria-live="polite">${this.escape(targetValue)} °C</output>
            <button type="button" class="secondary" data-pilot-temp="${targetValue + 0.5}"
              data-pilot-climate="${this.escape(climate)}" aria-label="${this.tr("pilotTarget")}: +"
              ${targetValue >= 30 ? "disabled" : ""}>+</button>
          </div></div>`
        : "";
      const canCommand = Boolean(climate) && ["heat","off"].includes(mode);
      const buttons = climate ? `
        <button class="power-action ${isOn ? "power-stop" : "power-start"}"
          data-climate="${this.escape(climate)}" data-mode="${isOn ? "off" : "heat"}"
          ${canCommand ? "" : "disabled"}>
          ${this.icon("power")}<span>${isOn ? this.tr("offButton") : this.tr("on")}</span>
        </button>` : "";
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
            data-full="${event.full_hopper ? "true" : "false"}">${this.icon("pencil")}${this.tr("edit")}</button>
            <button class="secondary mini" data-refill-delete="${this.escape(event.id)}"
              data-entry="${this.escape(stove.entry_id)}">${this.icon("trash")}${this.tr("delete")}</button>
          </div>
        </div>`;
      }).join("");
      const refillCard = stove.entry_id ? `
        <div class="refill-manager">
          <div class="refill-head"><div><h4 class="section-title">${this.icon("package")}${this.tr("refillTitle")}</h4>
          <p class="hint">${this.tr("refillHelp")}</p></div>
          <button data-refill-new="${this.escape(stove.entry_id)}">${this.icon("plus")}${this.tr("recordRefill")}</button></div>
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
            <strong class="maintenance-label">${this.icon(key === "burner" ? "flame" : "wrench")}${this.escape(title)}</strong>
            <small>${this.escape(label)}</small>
            ${valid ? `<div class="progress"><div style="width:${percent.toFixed(2)}%"></div></div>` : ""}
          </div>
          <button class="secondary" data-maint-kind="${this.escape(key)}"
            data-entry="${this.escape(stove.entry_id)}">${this.icon("check")}${this.tr("completed")}</button>
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
            <div class="device-heading">
              <span class="device-mark">${this.icon("flame")}</span>
              <div><h2>${this.escape(this.displayName(stove.title, index))}</h2>
                <span class="status ${isOn ? "on" : ""}">
                  ${this.icon(isOn ? "flame" : "info")}${this.escape(this.stateLabel(mode))}
                </span>
              </div>
            </div>
            ${this._activeTab === "control" ? `<div class="top-actions">${buttons}</div>` : ""}
          </div>
          <section class="tab-content" ${this._activeTab !== "control" ? "hidden" : ""}>
            <div class="control-summary">
              <div class="hero-reading"><span class="hero-symbol">${this.icon("temperature")}</span>
                <div><span class="subtle">${this.tr("roomTemp")}</span>
                <strong>${temp == null ? "—" : this.escape(temp) + " °C"}</strong>
                ${targetControl}</div>
              </div>
              <div class="hero-reading"><span class="hero-symbol blue">${this.icon("bars")}</span>
                <div><span class="subtle">${this.tr("power")}</span>
                ${powerControl}
                <div class="power-bars" aria-hidden="true">${powerBars}</div></div>
              </div>
            </div>
            <div class="support-grid">
              <div class="support-reading"><span class="support-symbol blue">${this.icon("fan")}</span>
                <div><span>${this.tr("fan")}</span>${fanControl}</div>
              </div>
              <div class="support-reading"><span class="support-symbol">${this.icon("clock")}</span>
                <div><strong>${todayRunning}</strong><span>${this.tr("todayHours")}</span></div>
              </div>
            </div>
            ${cronoId ? `<div class="crono-control">
              <div class="crono-description">${this.icon("clock")}
                <div><strong>${this.tr("cronoTitle")}</strong>
                  <span>${cronoAvailable ? this.tr(cronoEnabled ? "cronoOn" : "cronoOff") : this.tr("notAvailable")}</span>
                </div>
              </div>
              <button class="secondary crono-button" type="button"
                data-crono="${this.escape(cronoId)}" data-crono-action="${cronoEnabled ? "turn_off" : "turn_on"}"
                ${cronoAvailable ? "" : "disabled"}>
                ${this.tr(cronoEnabled ? "cronoDisable" : "cronoEnable")}
              </button>
            </div>` : ""}
            <div class="health-strip">
              <div class="${alarmOk ? "ok" : "attention"}">
                ${this.icon(alarmOk ? "shield" : "alert")}<span>${alarmText}</span>
              </div>
              <div>${this.icon("wifi")}${rssiValue}</div>
            </div>
          </section>
          <section class="tab-content" ${this._activeTab !== "consumption" ? "hidden" : ""}>
            <div class="section-intro">
              <h3 class="section-title">${this.icon("chart")}${this.tr("costsTitle")}</h3>
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
            <details class="more-info"><summary>${this.icon("sliders")}${this.tr("technical")}</summary>
              <div class="metrics">${pelletReadings}</div>
              <h4>${this.tr("powerHours")}</h4>
              <div class="metrics">${powerRows || `<p class="hint">${this.tr("noPower")}</p>`}</div>
            </details>
          </section>
          <section class="tab-content" ${this._activeTab !== "refills" ? "hidden" : ""}>
            ${refillCard}
          </section>
          <section class="tab-content" ${this._activeTab !== "maintenance" ? "hidden" : ""}>
            <h3 class="section-title">${this.icon("wrench")}${this.tr("maintTitle")}</h3>
            <p class="hint">${this.tr("maintHelp")}</p>
            ${maintenance}
          </section>
          <section class="tab-content" ${this._activeTab !== "settings" ? "hidden" : ""}>
            <h3 class="section-title">${this.icon("settings")}${this.tr("settingsTitle")}</h3>
            <p class="hint">${this.tr("settingsHelp")}</p>
            <div class="setting-section"><h4 class="section-title">${this.icon("package")}${this.tr("pelletGroup")}</h4>
              <div class="settings">${makeSettings(pelletNumbers.slice(0,5))}</div>
            </div>
            <details class="more-info"><summary>${this.icon("bars")}${this.tr("calibrationGroup")}</summary>
              <p class="hint">${this.tr("fullHelp")}</p>
              <div class="settings">${makeSettings(pelletNumbers.slice(8))}</div>
            </details>
            <details class="more-info"><summary>${this.icon("wrench")}${this.tr("maintGroup")}</summary>
              <div class="settings">${makeSettings(pelletNumbers.slice(5,8))}</div>
            </details>
            <details class="more-info"><summary>${this.icon("settings")}${this.tr("diagnosticsGroup")}</summary>
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

        /* One design system for light and dark Home Assistant themes. */
        .ico { width:20px;height:20px;display:inline-block;flex-shrink:0;vertical-align:middle; }
        .device-heading {display:flex;align-items:center;gap:14px;min-width:0;}
        .device-mark {display:grid;place-items:center;color:var(--warning-color,#f47b20);}
        .device-mark .ico {width:38px;height:38px;}
        .device-heading h2 {font-size:clamp(19px,2.4vw,24px);margin:0 0 7px;}
        .device-heading .status {display:inline-flex;align-items:center;gap:6px;padding:5px 10px;}
        .status .ico {width:14px;height:14px;}
        .top-actions {flex-shrink:0;}
        .power-action {min-height:76px;min-width:145px;display:flex;align-items:center;
          justify-content:center;gap:10px;border:1px solid transparent;padding:13px 18px;
          font-size:16px;box-shadow:0 2px 7px #0001;}
        .power-action .ico {width:30px;height:30px;}
        .power-action.power-stop {background:var(--error-color,#c34c3f);color:white;}
        .power-action.power-start {background:var(--primary-color,#159bca);color:var(--text-primary-color,white);}
        .power-action:disabled {opacity:.5;}
        .control-summary {display:grid;grid-template-columns:repeat(2,minmax(0,1fr));
          gap:12px;margin:20px 0 12px;}
        .hero-reading {min-height:154px;padding:24px 22px;border-radius:18px;
          background:var(--secondary-background-color);display:flex;align-items:center;gap:18px;}
        .hero-reading > div {min-width:0;}
        .hero-reading .subtle {color:var(--secondary-text-color);font-size:13px;display:block;}
        .hero-reading strong {display:block;font-size:clamp(31px,4.5vw,46px);font-weight:700;
          line-height:1.15;margin-top:8px;font-variant-numeric:tabular-nums;}
        .hero-symbol {color:var(--warning-color,#f47b20);}
        .hero-symbol .ico {width:37px;height:37px;}
        .blue {color:var(--primary-color,#159bca);}
        .power-bars {display:flex;align-items:end;gap:5px;height:19px;margin-top:9px;}
        .power-bars span {height:28%;width:12px;background:var(--divider-color);border-radius:2px;}
        .power-bars span:nth-child(2){height:43%;}
        .power-bars span:nth-child(3){height:58%;}
        .power-bars span:nth-child(4){height:78%;}
        .power-bars span:nth-child(5){height:100%;}
        .power-bars span.active {background:var(--primary-color,#159bca);}
        .support-grid {display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;}
        .support-reading {background:var(--secondary-background-color);border-radius:16px;
          padding:18px 20px;display:flex;align-items:center;gap:16px;}
        .support-symbol .ico {width:29px;height:29px;}
        .support-reading div {min-width:0;display:flex;flex-direction:column;gap:3px;}
        .support-reading strong {font-size:23px;font-variant-numeric:tabular-nums;}
        .support-reading span:last-child {color:var(--secondary-text-color);font-size:13px;}
        .hero-reading {align-items:flex-start;}
        .hero-reading > div {flex:1;min-width:0;}
        .target-control {display:flex;flex-direction:column;align-items:flex-start;gap:7px;
          padding-top:12px;margin-top:12px;border-top:1px solid var(--divider-color);}
        .inline-stepper {display:flex;flex-direction:row;align-items:center;gap:7px;
          min-width:0;max-width:100%;}
        .inline-stepper output {display:inline-block;min-width:52px;text-align:center;
          font-size:21px;font-weight:700;font-variant-numeric:tabular-nums;
          color:var(--primary-text-color);white-space:nowrap;}
        .target-control .inline-stepper output {min-width:80px;}
        .inline-stepper button {display:inline-flex;align-items:center;justify-content:center;
          flex:0 0 auto;width:42px;height:42px;min-width:42px;min-height:42px;
          border:1px solid var(--divider-color);border-radius:11px;padding:0;
          font-size:22px;font-weight:600;line-height:1;
          background:var(--secondary-background-color);color:var(--primary-text-color);
          cursor:pointer;transition:background .15s ease,border-color .15s ease;}
        .inline-stepper button:hover:not(:disabled) {
          border-color:var(--primary-color);background:var(--card-background-color);}
        .inline-stepper button:focus-visible {
          outline:2px solid var(--primary-color);outline-offset:2px;}
        .inline-stepper button:disabled {opacity:.4;cursor:not-allowed;}
        .support-reading .inline-stepper {flex-direction:row;gap:6px;}
        .support-reading .inline-stepper output {font-size:21px;min-width:30px;}
        .support-reading .inline-stepper button {width:42px;height:42px;min-width:42px;min-height:42px;}
        @media(max-width:680px) {
          .hero-reading {padding:18px 14px;gap:9px;flex-wrap:wrap;}
          .hero-reading .hero-symbol .ico {width:28px;height:28px;}
          .support-reading {flex-wrap:wrap;gap:9px;}
          .inline-stepper {gap:4px;}
          .inline-stepper button {width:42px;height:42px;min-width:42px;min-height:42px;}
          .target-control .inline-stepper output {min-width:69px;font-size:17px;}
        }
        .crono-control {display:flex;align-items:center;justify-content:space-between;gap:16px;
          border:1px solid var(--divider-color);border-radius:14px;padding:14px 16px;margin-top:16px;}
        .crono-description {display:flex;align-items:center;gap:12px;}
        .crono-description>.ico {color:var(--primary-color);width:24px;height:24px;}
        .crono-description>div {display:flex;flex-direction:column;gap:4px;}
        .crono-description strong {font-size:14px;}
        .crono-description span {color:var(--secondary-text-color);font-size:12px;}
        .crono-button {white-space:nowrap;}
        @media(max-width:480px){.crono-control{flex-wrap:wrap;}
          .crono-control button {width:100%;}}
        .health-strip {display:flex;align-items:center;justify-content:space-between;
          gap:15px;flex-wrap:wrap;padding:18px 4px 0;color:var(--secondary-text-color);}
        .health-strip>div {display:flex;align-items:center;gap:8px;font-size:13px;}
        .health-strip .ok {color:var(--success-color,#279452);}
        .health-strip .attention {color:var(--error-color,#c34c3f);}
        .section-title {display:flex;align-items:center;gap:10px;}
        .section-title .ico {color:var(--primary-color);width:24px;height:24px;}
        .more-info summary {display:flex;align-items:center;gap:10px;}
        .more-info summary .ico {color:var(--primary-color);width:18px;height:18px;}
        .technical-rows {display:grid;gap:12px;padding:2px 0 4px;}
        .technical-rows>div {display:flex;justify-content:space-between;gap:12px;
          align-items:center;border-bottom:1px solid var(--divider-color);padding:6px 0;}
        .technical-rows span {color:var(--secondary-text-color);}
        .maintenance-label {display:inline-flex;align-items:center;gap:10px;}
        .maintenance-label .ico {color:var(--primary-color);}
        button .ico {width:18px;height:18px;margin-right:7px;}
        button.power-action .ico {margin-right:0;}
        .tabs button {display:inline-flex;align-items:center;gap:7px;}
        .tabs button .ico {width:17px;height:17px;margin:0;}
        .refill-head button {display:inline-flex;align-items:center;justify-content:center;}
        .refill-manager .row-actions button {display:inline-flex;align-items:center;}
        @media(max-width:680px) {
          .stove .top {align-items:flex-start;flex-wrap:wrap;}
          .top-actions {width:100%;}
          .power-action {min-height:59px;width:100%;}
          .control-summary {grid-template-columns:1fr 1fr;}
          .hero-reading {padding:15px;min-height:126px;gap:8px;flex-direction:column;align-items:flex-start;}
          .hero-symbol .ico {width:27px;height:27px;}
          .hero-reading strong {font-size:clamp(27px,6.4vw,38px);}
          .support-reading {padding:12px;gap:10px;}
          .support-reading strong {font-size:18px;}
          .support-symbol .ico {width:22px;height:22px;}
          .tabs button {padding:9px 12px;}
        }
        @media(max-width:380px) {
          .support-grid {grid-template-columns:1fr;}
          .hero-reading strong {font-size:27px;}
          .device-mark .ico {width:30px;height:30px;}
        }

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
            ["control", this.tr("control"), "temperature"], ["consumption", this.tr("consumption"), "chart"],
            ["refills", this.tr("refills"), "package"], ["maintenance", this.tr("maintenance"), "wrench"],
            ["settings", this.tr("settings"), "settings"],
          ].map(([id,label,ico]) => `<button data-tab="${id}" class="${this._activeTab===id ? "selected" : ""}"
             aria-current="${this._activeTab===id ? "page" : "false"}">${this.icon(ico)}${label}</button>`).join("")}
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
      this.shadowRoot.querySelectorAll("button[data-pilot-temp]").forEach(button => {
        button.addEventListener("click", async () => {
          if (button.disabled) return;
          const value = Number(button.dataset.pilotTemp);
          if (!Number.isFinite(value) || value < 15 || value > 30 || !Number.isInteger(value * 2)) return;
          button.disabled = true;
          try {
            await this._hass.callService("climate", "set_temperature", {
              entity_id: button.dataset.pilotClimate, temperature: value,
            });
          } catch (_) {
            this._hass?.showToast?.({message: this.tr("pilotError")});
            button.disabled = false;
          }
        });
      });
      this.shadowRoot.querySelectorAll("button[data-pilot-step]").forEach(button => {
        button.addEventListener("click", async () => {
          if (button.disabled) return;
          const level = Number(button.dataset.pilotValue);
          if (!Number.isInteger(level) || level < 1 || level > 5) return;
          const id = button.dataset.pilotStep;
          const group = button.closest(".pilot-stepper");
          group?.querySelectorAll("button").forEach(b => { b.disabled = true; });
          try {
            await this._hass.callService("select", "select_option", {
              entity_id: id, option: String(level),
            });
          } catch (_) {
            this._hass?.showToast?.({message: this.tr("pilotError")});
            group?.querySelectorAll("button").forEach(b => { b.disabled = false; });
          }
        });
      });
      this.shadowRoot.querySelectorAll("button[data-crono]").forEach(button => {
        button.addEventListener("click", async () => {
          if (button.disabled) return;
          const action = button.dataset.cronoAction;
          if (action !== "turn_on" && action !== "turn_off") return;
          if (!window.confirm(this.tr(action === "turn_on" ? "cronoConfirmOn" : "cronoConfirmOff"))) return;
          button.disabled = true;
          try {
            await this._hass.callService("switch", action, {
              entity_id: button.dataset.crono,
            });
          } catch (error) {
            this._hass?.showToast?.({message: this.tr("cronoError")});
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
