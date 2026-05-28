# CVSS v3.1 official base-score compatibility

core/cvss31.py implements a self-contained CVSS v3.x vector parser and base-score calculator.

Verified examples:

- CVSS 3.1 vector example produces 9.8 Critical
- CVSS 3.1 vector example produces 8.8 High
- CVSS 3.1 vector example produces 6.1 Medium

Boundary: temporal and official environmental metrics are not yet implemented. The contextual layer must remain separate from official CVSS outputs.
