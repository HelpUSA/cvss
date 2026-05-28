# Official CVSS integration design

## Goal

Provide an official-CVSS-compatible scoring layer before claiming practical real-world CVSS scoring.

## Design principle

The implementation must return two separate outputs:

1. official_cvss: score and severity derived from the selected CVSS standard and vector.
2. contextual_environmental: additional environment-aware prioritization layer derived from infrastructure context.

## Required output structure

json
{
 "official_cvss": {
 "version": "3.1 or 4.0",
 "vector": "...",
 "base_score": 0.0,
 "base_severity": "...",
 "temporal_score": null,
 "environmental_score": null
 },
 "contextual_environmental": {
 "score": 0.0,
 "severity": "...",
 "delta_from_official": 0.0,
 "trace": []
 }
}


## Implementation options

- Implement official formulas directly with tests.
- Or vendor a well-maintained scoring library only if licensing and reproducibility are acceptable.

## Rule

Do not mix official CVSS formula components and project-specific context adjustments into one opaque score.
