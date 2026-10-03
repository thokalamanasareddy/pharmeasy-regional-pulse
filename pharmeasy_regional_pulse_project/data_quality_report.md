# Data quality report

- **Raw rows:** 2159
- **Exact duplicate rows removed:** 59
- **Clean rows:** 2100
- **Missing categories imputed:** 48
- **Missing profit values imputed:** 94
- **Schema validation (clean data):** `{'status': 'validated', 'row_count': 2100, 'missing_columns': []}`
- **Schema validation (deliberately broken copy):** `{'status': 'blocked_schema', 'row_count': 2100, 'missing_columns': ['profit_inr']}`

## Quality dimensions and implemented fixes

- **Uniqueness:** removed exact duplicate rows across all columns.
- **Consistency:** stripped whitespace and title-cased region names.
- **Completeness:** imputed missing category values using product-to-category lookup and missing profit values using category mean profit margins.
- **Accuracy:** recalculated missing profit values from sales and the observed category-level mean profit margin; this is an estimate, not recovered source truth.
- **Validity:** checked that all required columns exist and demonstrated the blocked-schema path when `profit_inr` is removed.
- **Relevance:** retained the order-level fields needed for region/month sales and profit metrics.
- **Timeliness:** the dataset covers April, May, and June 2026; this pipeline does not independently validate source freshness.
