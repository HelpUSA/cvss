function val(id) {
  var el = document.getElementById(id);
  return el ? el.value : "";
}

function sev(score) {
  var s = Number(score);
  if (s >= 9) return "Critical";
  if (s >= 7) return "High";
  if (s >= 4) return "Medium";
  if (s > 0) return "Low";
  return "None";
}

function yes(id) {
  return val(id) === "yes";
}

function esc(value) {
  return String(value == null ? "" : value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function fmtNum(value, digits) {
  var n = Number(value);
  if (!isFinite(n)) return "";
  return n.toFixed(digits === undefined ? 1 : digits);
}

function quoteCsv(value) {
  return "\"" + String(value == null ? "" : value).replace(/"/g, "\"\"") + "\"";
}

function getExportContract() {
  var r = window.lastCvssResult || {};
  return {
    official_cvss: r.official_cvss || {},
    contextual_environmental: r.contextual_environmental || {},
    evidence: r.evidence || {}
  };
}

function calc() {
  var base = Number(String(val("base_score") || "0").replace(",", "."));
  if (!isFinite(base)) base = 0;

  var contextual = base;
  var rationale = [];

  if (yes("internet_exposed")) {
    contextual += 0.4;
    rationale.push("internet exposure increased contextual priority");
  } else {
    contextual -= 0.3;
    rationale.push("absence of internet exposure reduced contextual priority");
  }

  if (yes("network_segmented")) {
    contextual -= 0.7;
    rationale.push("network segmentation reduced reachable attack surface");
  }

  if (yes("firewall_restricted")) {
    contextual -= 0.5;
    rationale.push("firewall restrictions reduced exposure");
  }

  if (yes("compensating_controls")) {
    contextual -= 0.4;
    rationale.push("compensating controls reduced expected impact");
  }

  if (yes("pci_in_scope")) {
    contextual += 0.3;
    rationale.push("PCI scope increased business and compliance relevance");
  }

  var criticality = val("business_criticality");
  if (criticality === "high") {
    contextual += 0.4;
    rationale.push("high business criticality increased contextual relevance");
  }

  if (criticality === "low") {
    contextual -= 0.2;
    rationale.push("low business criticality reduced contextual relevance");
  }

  var contextualScore = Number(Math.max(0, Math.min(10, contextual)).toFixed(1));
  var delta = Number((contextualScore - base).toFixed(1));
  var decision = delta < 0 ? "downgraded" : (delta > 0 ? "upgraded" : "unchanged");

  var officialCvss = {
    base_score: fmtNum(base, 1),
    base_severity: sev(base)
  };

  var contextualEnvironmental = {
    contextual_score: fmtNum(contextualScore, 1),
    contextual_severity: sev(contextualScore),
    decision: decision,
    delta_from_official_base: fmtNum(delta, 1),
    rationale: rationale.join("; ")
  };

  var evidence = {
    scenario: val("scenario"),
    asset_id: val("asset_id"),
    cve: val("cve"),
    internet_exposed: val("internet_exposed"),
    network_segmented: val("network_segmented"),
    pci_in_scope: val("pci_in_scope"),
    firewall_restricted: val("firewall_restricted"),
    compensating_controls: val("compensating_controls"),
    business_criticality: criticality
  };

  var out = {
    official_cvss: officialCvss,
    contextual_environmental: contextualEnvironmental,
    evidence: evidence,

    // Legacy flat fields remain for the static MVP UI and older snippets.
    scenario: evidence.scenario,
    asset_id: evidence.asset_id,
    cve: evidence.cve,
    base_score: officialCvss.base_score,
    base_severity: officialCvss.base_severity,
    environmental_score: contextualEnvironmental.contextual_score,
    environmental_severity: contextualEnvironmental.contextual_severity,
    delta: contextualEnvironmental.delta_from_official_base,
    decision: contextualEnvironmental.decision,
    rationale: contextualEnvironmental.rationale,
    internet_exposed: evidence.internet_exposed,
    network_segmented: evidence.network_segmented,
    pci_in_scope: evidence.pci_in_scope,
    firewall_restricted: evidence.firewall_restricted,
    compensating_controls: evidence.compensating_controls,
    business_criticality: evidence.business_criticality
  };

  window.lastCvssResult = out;

  var exportPreview = JSON.stringify(getExportContract(), null, 2);
  document.getElementById("result").innerHTML =
    "<h3>Result</h3>" +
    "<div class=grid>" +
    "<div class=card><div>Official CVSS base</div><div class=metric>" + esc(officialCvss.base_score) + "</div><div>" + esc(officialCvss.base_severity) + "</div></div>" +
    "<div class=card><div>Contextual prioritization</div><div class=metric>" + esc(contextualEnvironmental.contextual_score) + "</div><div>" + esc(contextualEnvironmental.contextual_severity) + "</div></div>" +
    "<div class=card><div>Delta from official base</div><div class=metric>" + esc(contextualEnvironmental.delta_from_official_base) + "</div><div>" + esc(contextualEnvironmental.decision) + "</div></div>" +
    "</div>" +
    "<p><strong>Caveat:</strong> Contextual prioritization is not official CVSS and must remain separate from the official_cvss layer.</p>" +
    "<p class=note>" + esc(contextualEnvironmental.rationale) + "</p>" +
    "<textarea rows=10 id=exportBox>" + esc(exportPreview) + "</textarea>";
}

function loadExample() {
  document.getElementById("scenario").value = "pci_segmented_lab_20260517_143146";
  document.getElementById("asset_id").value = "payment-api";
  document.getElementById("cve").value = "CVE-2025-0001";
  document.getElementById("base_score").value = "9.8";
  document.getElementById("internet_exposed").value = "no";
  document.getElementById("network_segmented").value = "yes";
  document.getElementById("pci_in_scope").value = "yes";
  document.getElementById("firewall_restricted").value = "yes";
  document.getElementById("compensating_controls").value = "yes";
  document.getElementById("business_criticality").value = "high";
  calc();
}

function downloadJson() {
  var data = JSON.stringify(getExportContract(), null, 2);
  var blob = new Blob([data], {type: "application/json"});
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "cvss_official_contextual_result.json";
  a.click();
}

function downloadCsv() {
  var r = window.lastCvssResult || {};
  var o = r.official_cvss || {};
  var c = r.contextual_environmental || {};
  var e = r.evidence || {};
  var header = [
    "scenario",
    "asset_id",
    "cve",
    "official_cvss_base_score",
    "official_cvss_base_severity",
    "contextual_score",
    "contextual_severity",
    "contextual_decision",
    "contextual_delta_from_official_base",
    "rationale"
  ];
  var values = [
    e.scenario,
    e.asset_id,
    e.cve,
    o.base_score,
    o.base_severity,
    c.contextual_score,
    c.contextual_severity,
    c.decision,
    c.delta_from_official_base,
    c.rationale
  ];
  var csv = header.join(",") + "\n" + values.map(quoteCsv).join(",");
  var blob = new Blob([csv], {type: "text/csv"});
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "cvss_official_contextual_result.csv";
  a.click();
}

function copyPipelineJson() {
  var r = window.lastCvssResult || {};
  var e = r.evidence || {};
  var o = r.official_cvss || {};
  var pkg = {
    case_description: {
      scenario: e.scenario,
      source: "interactive_static_mvp"
    },
    vulnerabilities: [{
      finding_id: "interactive-001",
      asset_id: e.asset_id,
      cve: e.cve,
      vulnerability_type: "user_entered",
      official_cvss_base_score: o.base_score,
      official_cvss_base_severity: o.base_severity
    }],
    context: e,
    export_layers: getExportContract()
  };
  navigator.clipboard.writeText(JSON.stringify(pkg, null, 2));
  alert("Pipeline JSON copied with official_cvss, contextual_environmental, and evidence.");
}

function copyMarkdownReport() {
  var r = window.lastCvssResult || {};
  var o = r.official_cvss || {};
  var c = r.contextual_environmental || {};
  var e = r.evidence || {};
  var text = "# CVSS assessment report\n\n";
  text += "## Official CVSS\n";
  text += "- official_cvss_base_score: " + (o.base_score || "") + "\n";
  text += "- official_cvss_base_severity: " + (o.base_severity || "") + "\n\n";

  text += "## Contextual Prioritization\n";
  text += "- contextual_score: " + (c.contextual_score || "") + "\n";
  text += "- contextual_severity: " + (c.contextual_severity || "") + "\n";
  text += "- contextual_decision: " + (c.decision || "") + "\n";
  text += "- contextual_delta_from_official_base: " + (c.delta_from_official_base || "") + "\n";
  text += "- rationale: " + (c.rationale || "") + "\n\n";

  text += "## Evidence\n";
  text += "- scenario: " + (e.scenario || "") + "\n";
  text += "- asset_id: " + (e.asset_id || "") + "\n";
  text += "- cve: " + (e.cve || "") + "\n";
  text += "- internet_exposed: " + (e.internet_exposed || "") + "\n";
  text += "- network_segmented: " + (e.network_segmented || "") + "\n";
  text += "- pci_in_scope: " + (e.pci_in_scope || "") + "\n";
  text += "- firewall_restricted: " + (e.firewall_restricted || "") + "\n";
  text += "- compensating_controls: " + (e.compensating_controls || "") + "\n";
  text += "- business_criticality: " + (e.business_criticality || "") + "\n\n";

  text += "## Caveat\n";
  text += "Contextual prioritization is not official CVSS. The official CVSS layer must remain separate from the contextual_environmental layer.\n";

  navigator.clipboard.writeText(text);
  alert("Markdown report copied with separate Official CVSS, Contextual Prioritization, Evidence, and Caveat sections.");
}

window.addEventListener("DOMContentLoaded", loadExample);
