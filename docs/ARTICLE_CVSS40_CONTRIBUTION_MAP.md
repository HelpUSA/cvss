---
status: active
last_updated: 2026-07-10
owner: "Wagner / CVSS project"
tags:
  - cvss-v4
  - contribution-map
  - environmental-metrics
  - ai-watcher
---

# CVSS v4.0 contribution map for the AI/watcher article

| Official CVSS v4.0 concept | Human difficulty | AI/watcher support | Artifact produced | Allowed claim | Claim to avoid |
|---|---|---|---|---|---|
| CVSS-B Base score | Analysts may treat severity as full organizational risk | Preserve official Base vector and score as separate baseline | `official_cvss_v4_vector`, `cvss_b_score` | The prototype preserves CVSS-B as the baseline | The prototype improves Base CVSS |
| Threat metric group | Threat context may change and evidence may be scattered | Collect threat notes, timestamps, and uncertainty flags | `threat_context`, evidence notes | The watcher supports evidence collection for time-sensitive context | The watcher has authoritative threat intelligence |
| Environmental Security Requirements | CR, IR, and AR require local business and asset judgment | Link asset criticality evidence to candidate CR/IR/AR rationale | `confidentiality_requirement`, `integrity_requirement`, `availability_requirement` | The workflow supports reviewable Environmental metric selection | AI decides the final Environmental score |
| Modified Base Metrics | Deployment, controls, privileges, and exposure are local | Map deployment evidence to candidate Modified metrics | `candidate_modified_metrics`, `trace_json` | The workflow makes Modified metric choices auditable | The workflow changes official CVSS semantics |
| Supplemental metrics | Optional context may be used inconsistently | Capture supplemental observations as contextual signals | `supplemental_context` | Supplemental signals can inform operational discussion | Supplemental metrics directly modify CVSS-BTE |
| CVSS-B / CVSS-BT / CVSS-BE / CVSS-BTE labels | Scores may be miscommunicated | Force explicit metric-group labels in outputs | labeled CSV/dashboard outputs | The output identifies the metric groups used | A score without vector or label is sufficient |
| Consumer responsibility | Local organizations must apply their own context | Assist consumer-side analyst and require review status | `human_review_status` | The watcher assists consumer-side Environmental assessment | Providers should apply one Environmental score for all consumers |
| Evidence and auditability | Decisions may be undocumented or inconsistent | Attach evidence, uncertainty, and trace artifacts to each recommendation | manifest, CSV, trace report | The workflow improves traceability and reproducibility | The workflow proves real-world effectiveness |
| Human review | Analysts need decision support, not replacement | Mark review as required/reviewed/not required | `human_review_status`, `review_required` | AI supports human review | AI replaces analysts |
| Evaluation | Broad real-world validation is not yet available | Evaluate curated scenarios with reproducible artifacts | result tables, trace completeness metrics | The evaluation demonstrates feasibility and traceability | The evaluation proves predictive superiority |
