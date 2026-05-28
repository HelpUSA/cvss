# Scenario input schema

Each curated scenario must use a stable input package so the research pipeline, article tables, dashboard, and future interactive site all consume the same structure.

## Required files

- case_description.md
- topology.yaml
- firewall_rules.yaml
- business_impact.yaml
- pci_scope.yaml
- vulnerabilities.csv
- expected_expert_labels.yaml

## vulnerabilities.csv required columns

- finding_id
- asset_id
- cve
- vulnerability_type
- base_score
- base_severity
- base_vector
- internet_exposed
- network_segmented
- pci_in_scope
- firewall_restricted
- compensating_controls
- business_criticality
- notes

## Context fields

internet_exposed, network_segmented, pci_in_scope, firewall_restricted, and compensating_controls should use yes/no values. business_criticality should use low, medium, or high.

## Research rule

The interactive site must eventually export this same structure rather than inventing a separate product-only schema.
