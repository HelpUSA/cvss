# CVSS v4.0 Phase 1 reading queue

This queue turns the official FIRST CVSS v4.0 documentation into article work items.

## Primary reading order

1. Main CVSS v4.0 page.
2. Specification Document.
3. User Guide.
4. Implementation Guide.
5. Examples.
6. FAQ.
7. Calculator notes.
8. Data representations.

## Extract for the article

For each official source, extract only short article-safe notes and cite the official URL in the manuscript. Do not copy large sections into the repository.

### Required concepts

- Four metric groups: Base, Threat, Environmental, Supplemental.
- CVSS-B, CVSS-BT, CVSS-BE, CVSS-BTE naming.
- Base metrics as intrinsic vulnerability characteristics.
- Threat metrics as time-dependent characteristics.
- Environmental metrics as consumer-environment-specific characteristics.
- Environmental Security Requirements.
- Modified Base Metrics.
- Supplemental metrics and how they relate to scoring.
- Consumer responsibility for applying Threat and Environmental context.
- Correct communication of vector string, metric groups, and score.

## Article mapping questions

1. Which CVSS v4.0 concepts does the watcher assist?
2. Which decisions remain human-reviewed?
3. Which outputs are evidence-backed recommendations rather than official scores?
4. Which artifacts prove traceability?
5. Which claims must be avoided because they imply modifying CVSS?

## Immediate next deliverables

- `docs/CVSS40_OFFICIAL_READING_NOTES.md` should be expanded with verified official definitions.
- `docs/ARTICLE_CVSS40_CONTRIBUTION_MAP.md` should map each project capability to a CVSS v4.0 concept.
- `docs/ARTICLE_DATASET_SCHEMA.md` should become the schema for the 30 to 50 scenario dataset.
