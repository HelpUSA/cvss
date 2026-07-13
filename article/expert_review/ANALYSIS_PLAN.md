# Expert-review analysis plan

## Sample

- Scenarios: 30
- Planned reviewers: 3
- Planned assessments: 90
- Two counterbalanced packet orders

## Primary measures

### Metric-level exact agreement

For each CVSS Environmental metric:

- watcher-versus-reviewer exact agreement;
- pairwise reviewer exact agreement;
- majority-reviewer agreement with watcher;
- missing or deferred response rate.

### Multi-reviewer agreement

Where metric values are categorical, calculate:

- Fleiss' kappa when all reviewers assess every scenario;
- Krippendorff's alpha when missing values require a more flexible measure.

Report raw agreement alongside chance-corrected statistics.

### Operational-priority agreement

For ordered categories, calculate:

- exact agreement;
- adjacent-category agreement;
- weighted Cohen's kappa for pairwise comparisons;
- weighted multi-reviewer agreement where supported.

The priority category remains a prototype operational measure and is not an
official CVSS score.

## Secondary measures

- median review time per scenario;
- interquartile range of review time;
- median confidence;
- median evidence-sufficiency rating;
- defer rate;
- missing-evidence rate;
- ambiguity rate;
- watcher override rate after adjudication.

## Stratified analysis

Report measures separately for:

- real NVD/CVSS v4.0 records with curated consumer context;
- controlled synthetic scenarios;
- Base severity category;
- upward, downward, and unchanged watcher priority transitions;
- high-confidence versus low-confidence reviewer responses.

## Adjudication outcomes

Classify each disagreement as one of:

- insufficient evidence;
- ambiguous scenario language;
- reviewer interpretation difference;
- reviewer data-entry error;
- watcher recommendation error;
- CVSS specification interpretation issue;
- operational-priority framework issue.

## Interpretation boundary

The study can support claims about reviewer agreement, review effort, and
evidence sufficiency. It cannot by itself prove improved remediation outcomes,
exploit prediction, or production effectiveness.
