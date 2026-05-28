# CVSS interactive site plan

This document defines where the fully usable website fits in the project. The current public dashboard is a static deploy and proof of reproducibility. It is not yet the full user-facing calculator.

## Current dashboard purpose

The current index.html proves that cvss.helpusbr.com can serve a clean static dashboard without Next.js, npm build, Python serverless, or custom root-directory behavior. It is also a public marker for the research artifacts.

## Future usable site objective

The usable site should let a user enter scenario and vulnerability data, calculate environmental CVSS results, view explanations, and export artifacts compatible with the research pipeline.

## Required user inputs

- Scenario name.
- Asset or system.
- CVE or vulnerability identifier.
- Base CVSS vector and score.
- Internet exposure.
- Network segmentation.
- PCI scope.
- Firewall restrictions.
- Compensating controls.
- Business criticality.
- Confidentiality, integrity, and availability context.

## Required outputs

- Base score and severity.
- Environmental score and severity.
- Score delta.
- Decision: downgraded, unchanged, or upgraded.
- Explanation of context factors.
- Recommended actions.
- Exportable JSON.
- Exportable CSV.
- Pipeline-compatible scenario package.

## Recommended MVP architecture

Use static HTML, CSS, and JavaScript only. Avoid Next.js and npm build requirements for the MVP. The calculation engine should be reusable and should not depend on the UI.

Suggested files:
- index.html
- app.js
- styles.css
- examples/pci_segmented_lab_20260517_143146.json

## Relationship to the article

The site is a demonstrator and artifact generator. It should not be presented as a validated enterprise product in the current article. Human expert comparison remains future work.

## Interactive MVP checkpoint

Added app.js, styles.css, example JSON, and an interactive calculator section in index.html. The MVP calculates deterministic environmental CVSS values in the browser and exports JSON. Next checkpoint: convert exported JSON to standardized scenario input package.

