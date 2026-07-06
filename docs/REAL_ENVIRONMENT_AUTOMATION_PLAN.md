# Real Environment Automation Plan

This document defines the next phase for turning the validated public CVSS dashboard into an operational workflow that can analyze real environments through the local watcher.

## Goal

Use the watcher as the execution layer and the chat as the reasoning layer. The watcher runs scanners, imports evidence, normalizes findings, and returns results. The chat reviews the output, decides the next safe action, and can ask the watcher to continue.

## Architecture

Scanner or inventory source -> raw scan JSON -> normalizer -> official_cvss layer -> contextual_environmental layer -> evidence layer -> dashboard, export, report, or ticket.

## Scanner order

1. Trivy for containers, repositories, filesystems, and dependencies. This is the first MVP scanner because it is local, simple, free, and emits JSON.
2. GitHub Dependabot or Snyk for code and dependency alerts. This requires local tokens and API integration.
3. OpenVAS or Nessus for network scans. This requires scan scope, credentials, and an asset inventory.

## Watcher role

The watcher should execute deterministic commands only. During the MVP it can run scanners, read files, write reports, run tests, call importers, and return stdout or generated artifacts.

Allowed MVP actions:

- run Trivy or import an existing Trivy JSON file
- generate normalized assessment JSON
- generate CSV or Markdown reports
- update docs and examples
- run local validation commands
- report changes back to the chat

Blocked by default:

- changing firewall rules
- applying dependency upgrades automatically
- deploying infrastructure changes automatically
- deleting production data
- running network scans outside an approved target scope

## MVP command

The first operational command is:

python tools/run_real_assessment.py --scanner trivy --target .

For testing without Trivy installed, import an existing Trivy JSON file:

python tools/run_real_assessment.py --scanner trivy --input examples/trivy.sample.json --output examples/sample_assessment.json

## Normalized contract

The normalized output must preserve three layers:

- official_cvss: official CVSS base score, base severity, vector, and source when present in scanner data
- contextual_environmental: local operational priority derived from asset context and evidence
- evidence: scanner name, target, package, installed version, fixed version, CVE, URLs, and source file

## Asset context

The contextual layer needs asset metadata such as environment, internet exposure, business criticality, and data sensitivity. The MVP starts with CLI flags and an example file under inputs/assets.example.yml.

## Context heuristic for MVP

The first heuristic is intentionally simple and auditable:

- internet exposed assets increase contextual priority
- production assets increase contextual priority
- high or critical business criticality increases contextual priority
- sensitive data increases contextual priority
- development assets that are not exposed can lower contextual priority
- the result is capped between 0.0 and 10.0
- every change includes rationale text

## Expected files

- tools/run_real_assessment.py
- inputs/assets.example.yml
- examples/trivy.sample.json
- examples/sample_assessment.json
- outputs/scans/.gitkeep
- outputs/assessments/.gitkeep

## Completion criteria

This phase is complete when the watcher can run a single command that imports a Trivy JSON file, produces normalized findings, calculates official and contextual layers, writes an assessment JSON, runs local validation, and commits the implementation.

## Next phases

After the Trivy MVP works, add GitHub Dependabot or Snyk import. After code dependency import works, add OpenVAS or Nessus with explicit scan scope and asset inventory.
