# CVSS v3.1 official base-score compatibility checkpoint

This branch includes core/cvss31.py, a self-contained CVSS v3.x vector parser and base-score calculator.

## Supported now

- CVSS:3.1 and CVSS:3.0 vector prefix parsing.
- Base metrics AV, AC, PR, UI, S, C, I, A.
- CVSS v3.x base score rounding behavior.
- Severity mapping.
- Impact and exploitability subscores.
- Separate official_cvss output object.

## Known test vectors

- CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H -> 9.8 Critical.
- CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H -> 8.8 High.
- CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N -> 6.1 Medium.

## Boundary

Temporal and official environmental metrics are not yet implemented. The project contextual layer must remain separate from official CVSS scoring outputs.
