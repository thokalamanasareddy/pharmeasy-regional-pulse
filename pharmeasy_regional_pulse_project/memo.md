# Regional sales review: Guntur April–May movement

## Title
Guntur sales increased by 122.19% from April to May 2026. [HIGH]

## Context
The pipeline compares cleaned order-level records from April, May, and June 2026 after removing exact duplicate rows and imputing missing fields. [LOW] Sales values are aggregated by region and month using SQLite `SUM(sales_inr)`. [LOW]

## Key Insight
Guntur's April-to-May sales change is +122.19%, the largest-magnitude flagged case specified for this review. [HIGH] The 8% threshold is an operational review trigger, not a statistical-significance test. [LOW]

## Evidence
The reported +122.19% change is calculated as `(May sales − April sales) / April sales × 100` from the region/month metrics. [HIGH] Before external use, the reviewer should verify the April and May Guntur sales totals and the calculated percentage against `region_month_metrics.csv` and `mom_changes.csv`. [LOW]

## Recommendation
Have the regional manager review Guntur's order counts, category mix, and order-level records for April and May before deciding whether an operational intervention is needed. [MEDIUM] Do not attribute the increase to an external event or competitor action without additional evidence. [LOW]

## Next Check
Within five business days of review, compare Guntur's April and May category-level sales and order counts, then record whether the movement is supported across multiple categories or concentrated in one. [MEDIUM]

## Assumptions
The unverified assumption is that the cleaned export represents comparable and complete regional order activity in both months; the dataset alone cannot establish that source capture and business conditions were unchanged. [MEDIUM]
