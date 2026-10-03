"""Cleaning, imputation, schema validation, and quality reporting."""
import pandas as pd

REQUIRED_COLUMNS = ["order_id","order_date","region","category","product","quantity","sales_inr","profit_inr"]

def validate_schema(df, required_columns):
    missing = [c for c in required_columns if c not in df.columns]
    return {"status":"blocked_schema" if missing else "validated","row_count":int(len(df)),"missing_columns":missing}

def clean_orders(raw_path="pharmeasy_orders_raw.csv", output_path="orders_clean.csv"):
    df = pd.read_csv(raw_path, dtype={"order_id":"string","region":"string","category":"string","product":"string"})
    raw_count = len(df)
    df = df.drop_duplicates(keep="first").copy()
    duplicates_removed = raw_count - len(df)
    df["region"] = df["region"].astype("string").str.strip().str.title()
    # Build deterministic product-to-category mapping from known non-missing rows.
    lookup = df.dropna(subset=["category"]).drop_duplicates("product").set_index("product")["category"].to_dict()
    missing_category_before = int(df["category"].isna().sum())
    df["category"] = df["category"].fillna(df["product"].map(lookup))
    if df["category"].isna().any():
        raise ValueError("Category imputation failed: product has no known category mapping.")
    df["sales_inr"] = pd.to_numeric(df["sales_inr"], errors="raise")
    df["profit_inr"] = pd.to_numeric(df["profit_inr"], errors="coerce")
    missing_profit_before = int(df["profit_inr"].isna().sum())
    observed = df[df["profit_inr"].notna()].copy()
    observed["profit_margin"] = observed["profit_inr"] / observed["sales_inr"]
    margins = observed.groupby("category")["profit_margin"].mean().to_dict()
    missing = df["profit_inr"].isna()
    df.loc[missing, "profit_inr"] = (df.loc[missing, "sales_inr"] * df.loc[missing, "category"].map(margins)).round(2)
    df["quantity"] = pd.to_numeric(df["quantity"], errors="raise").astype(int)
    df["profit_inr"] = df["profit_inr"].round(2)
    result = validate_schema(df, REQUIRED_COLUMNS)
    broken = df.drop(columns=[REQUIRED_COLUMNS[-1]])
    broken_result = validate_schema(broken, REQUIRED_COLUMNS)
    df.to_csv(output_path, index=False)
    report = f"""# Data quality report

- **Raw rows:** {raw_count}
- **Exact duplicate rows removed:** {duplicates_removed}
- **Clean rows:** {len(df)}
- **Missing categories imputed:** {missing_category_before}
- **Missing profit values imputed:** {missing_profit_before}
- **Schema validation (clean data):** `{result}`
- **Schema validation (deliberately broken copy):** `{broken_result}`

## Quality dimensions and implemented fixes

- **Uniqueness:** removed exact duplicate rows across all columns.
- **Consistency:** stripped whitespace and title-cased region names.
- **Completeness:** imputed missing category values using product-to-category lookup and missing profit values using category mean profit margins.
- **Accuracy:** recalculated missing profit values from sales and the observed category-level mean profit margin; this is an estimate, not recovered source truth.
- **Validity:** checked that all required columns exist and demonstrated the blocked-schema path when `profit_inr` is removed.
- **Relevance:** retained the order-level fields needed for region/month sales and profit metrics.
- **Timeliness:** the dataset covers April, May, and June 2026; this pipeline does not independently validate source freshness.
"""
    with open("data_quality_report.md","w",encoding="utf-8") as f: f.write(report)
    print("Cleaning complete:", {"raw_rows":raw_count,"duplicates_removed":duplicates_removed,"clean_rows":len(df),"schema":result,"broken_schema":broken_result})
    return df

if __name__ == "__main__":
    clean_orders()
