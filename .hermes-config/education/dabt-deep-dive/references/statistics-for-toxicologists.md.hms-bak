# Statistics for Toxicologists — DABT Exam Reference

## Core Exam Traps (appear across multiple question types)

| Trap | Why it catches people | Correct framing |
|------|---------------------|-----------------|
| **SD vs SE** | Both describe spread; SE is *always* smaller (SE = SD/√n). Reporters switch them to make data look tighter. | SD = individual animal variability. SE = precision of mean estimate. If a table says "mean ± SE, n=10", SD = SE × √10. |
| **"Not significant" = no effect** | The single most dangerous misinterpretation in toxicology. P > 0.05 means "failed to reject H₀ at α = 0.05," not "no effect" — especially in an underpowered study. | "No statistically significant differences were detected. The confidence interval for the effect includes zero." |
| **Bonferroni vs Dunnett** | Bonferroni is too conservative for dose-response studies. Treats all 4 comparisons as independent when they all share the same control. | Dunnett's accounts for shared-control correlation. Less conservative → more power to detect real effects. Default for toxicology post-hoc. |
| **Parametric vs non-parametric** | Running ANOVA on non-normal data violates the normality-of-residuals assumption → F-statistic unreliable. | Shapiro-Wilk test first. If normality fails, use Kruskal-Wallis + Dunn's. |
| **One-tailed vs two-tailed** | Toxicologists default to two-tailed. A chemical could increase OR decrease an endpoint. | One-tailed requires strong prior directional hypothesis (rare in general tox). |
| **Paired vs unpaired t-test** | Paired t-test is more powerful *only* when same subjects are measured twice. Using it on different animals (even weight-matched) is a protocol violation. | Independent groups → 2-sample t-test. Same subjects pre/post → paired t-test. |

## Test Selection Decision Tree

```
Q1: Data type?
├── Continuous (numbers) → Q2
└── Categorical (proportions) → Q5

Q2: How many groups?
├── 2 groups → Q3
└── ≥3 groups → Q4

Q3: Independent or paired?
├── Different animals (treated vs control) → 2-sample t-test
└── Same animals pre/post → Paired t-test

Q4: Normal or non-normal?
├── Normal → ANOVA + Dunnett (vs control) or Tukey (all pairs)
└── Non-normal → Kruskal-Wallis + Dunn's

Q5: Association or trend?
├── Association between two categorical vars → χ² test (or Fisher's exact if any expected cell < 5)
└── Trend in proportions across ordered doses → Cochran-Armitage test
```

## Multiple Comparisons Hierarchy

| Correction | When | Power | Notes |
|-----------|------|-------|-------|
| **Dunnett's** | Multiple doses vs single control | Best for this design | **Default for tox** — shares control group correlation |
| **Bonferroni** | Any set of independent comparisons | Most conservative | Use only when comparisons don't share a reference group |
| **Tukey HSD** | All pairwise comparisons | Moderate | When you need every group vs every other group |
| **Williams' test** | Monotonic dose-response trend | Most powerful if monotonic | OECD-recommended primary trend test for continuous endpoints |

## Trend Tests

| Test | Data type | Use case |
|------|-----------|----------|
| **Williams'** | Continuous, parametric | Dose-related trend, assumes monotonicity. Standard for repeated-dose studies. |
| **Cochran-Armitage** | Proportions | Monotonic trend in incidence (tumors, mortality). Standard for 2-year bioassays. |
| **Jonckheere-Terpstra** | Continuous, non-parametric | Trend test when normality fails. |

## Power Analysis — The Four Parameters

```  
Sample Size (n)     ← control this in study design
Effect Size         ← estimate from prior data or literature
α (Type I error)    ← set at 0.05 by convention
Power (1 − β)       ← conventionally target 80%
```

**The tradeoff:** Fix any three, the fourth is determined. Small n + small effect = very low power. A "not significant" result from 5 rats/group is meaningless for any endpoint with moderate variability.

## OECD Guideline Group Sizes (Power-Driven)

| Guideline | Duration | Minimum/sex/group | Power implication |
|-----------|----------|------------------|-------------------|
| TG 407 | 28-day | 5 | Can detect only large effects (>1.8 SD) |
| TG 408 | 90-day | 10 | Moderate power for clinical path endpoints |
| TG 453 | 2-year chronic | 20 | Adequate for tumor incidence detection |

## What "Not Statistically Significant" Means (Exact Language)

| ❌ Incorrect | ✅ Correct |
|-------------|-----------|
| "The chemical has no effect" | "We failed to reject the null hypothesis at α = 0.05" |
| "The effect is biologically irrelevant" | "The confidence interval for the effect includes zero" |
| "The chemical is safe at this dose" | "This study had insufficient power to detect the observed effect as significant" |

## Questions from DB for Practice

- **DABT-2072**: χ² test for case-control association (cigarette smoking + bladder cancer)
- **DABT-2073**: ANOVA for 3+ dose groups vs placebo (antihypertensive)
- **DABT-2074**: 2-sample t-test for two independent groups (RA vs control on urinary excretion)
