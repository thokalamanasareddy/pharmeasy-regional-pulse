# Presentation storyline

## 1. Executive audience — Situation–Complication–Resolution

### Situation
The regional desk has a repeatable pipeline that cleans the April–June 2026 order export, validates its schema, and calculates regional sales totals through SQLite. [LOW]

### Complication
Guntur's April-to-May sales movement is reported as +122.19%, making it the flagship case for a human review. [HIGH] This is a change in observed sales, not evidence by itself of the cause or of a statistically significant underlying shift. [LOW]

### Resolution
Ask the regional manager to verify the April and May totals, compare category mix and order counts, and document a review decision before any external action. [MEDIUM] Revisit the recommendation after those checks are completed and recorded. [MEDIUM]

## 2. Regional manager audience — Overview–Category–Detail

### Overview
The headline finding is Guntur's reported +122.19% sales change from April to May 2026. [HIGH]

### Category
Use the dashboard's category breakdown to determine whether the change is spread across categories or concentrated in one; the narrative should not name a driving category until the computed category totals support it. [MEDIUM]

### Detail
The calculation uses cleaned order data and SQL-aggregated monthly sales: `(May sales − April sales) / April sales × 100`. [LOW] Exact April and May totals should be checked in `region_month_metrics.csv` and `mom_changes.csv` before sign-off. [HIGH]

## Anticipated pushback Q&A

### Q1 — Why should I believe this number?
1. **Acknowledge:** It is reasonable to ask whether the percentage can be reproduced and whether the underlying rows are clean.
2. **Verified vs. not verified:** The pipeline removes exact duplicate rows, normalizes region text, imputes missing fields, and aggregates sales by region/month in SQLite; the result still depends on the source export being representative.
3. **Resolution and timing:** Before the next regional review, independently rerun the pipeline and compare Guntur's April and May sales totals and percentage with the generated CSV metrics.

### Q2 — What if an alternative explanation is driving this?
1. **Acknowledge:** The sales change alone does not establish why it happened.
2. **Verified vs. not verified:** The pipeline can verify observed order counts, sales, and category mix; it does not verify promotions, stock availability, local events, competitor activity, or changes in data capture.
3. **Resolution and timing:** Within five business days, review category-level totals and operational records for both months, then update the memo's Assumptions field with any evidence-backed explanation.
