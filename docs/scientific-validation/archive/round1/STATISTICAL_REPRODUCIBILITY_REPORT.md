# Statistical Reproducibility Report

The historical flat-versus-segmented contingency analysis is now reproduced by
`scripts/reproduce_historical_fisher.py` rather than relying on manually typed values.
The machine-readable output is `generated/historical_fisher.json`.

The script records both:
- the simple sample cross-product odds ratio; and
- Fisher-style conditional maximum-likelihood odds ratio with its exact conditional 95% confidence interval.

The LaTeX manuscript uses the conditional estimate/interval when it labels the interval as exact conditional. This avoids pairing a Wald formula with a conditional interval.
