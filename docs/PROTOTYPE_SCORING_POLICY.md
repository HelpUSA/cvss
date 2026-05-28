# Prototype environmental scoring policy

This document defines the current deterministic environmental scoring policy used by the research prototype.

## Current adjustment constants

| Field | Condition | Adjustment | Interpretation |
| --- | --- | ---: | --- |
| internet_exposed | yes | +0.4 | Increases environmental exposure. |
| internet_exposed | no | -0.3 | Reduces reachable attack surface. |
| network_segmented | yes | -0.7 | Reduces reachable attack surface. |
| firewall_restricted | yes | -0.5 | Reduces exposure. |
| compensating_controls | yes | -0.4 | Reduces expected impact. |
| pci_in_scope | yes | +0.3 | Increases business/compliance relevance. |
| business_criticality | high | +0.4 | Increases business relevance. |
| business_criticality | low | -0.2 | Reduces business relevance. |

## Evidence boundary

This is a prototype deterministic scoring policy. It is not claimed to be the official FIRST CVSS environmental formula. The policy is useful because it is explicit, auditable, reproducible, trace-enabled, and suitable for synthetic curated scenario evaluation.

## Future option

A future branch may implement the official CVSS environmental equation and compare it against this prototype policy.
