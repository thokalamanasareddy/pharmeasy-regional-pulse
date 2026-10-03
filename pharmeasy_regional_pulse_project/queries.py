"""SQL-verified joins, data checks, and region/month sales metrics."""
import sqlite3
import pandas as pd

def run_queries(db_path="pharmeasy.db"):
    with sqlite3.connect(db_path) as con:
        left = con.execute("SELECT COUNT(*) FROM regions_master r LEFT JOIN orders_clean o ON r.region=o.region").fetchone()[0]
        inner = con.execute("SELECT COUNT(*) FROM regions_master r INNER JOIN orders_clean o ON r.region=o.region").fetchone()[0]
        print(f"LEFT JOIN rows: {left}; INNER JOIN rows: {inner}; delta: {left-inner}")
        duplicate_keys = pd.read_sql_query("SELECT order_id, COUNT(*) AS n FROM orders_clean GROUP BY order_id HAVING COUNT(*) > 1", con)
        print("Duplicate order_id rows (expected empty):")
        print(duplicate_keys.to_string(index=False) if not duplicate_keys.empty else "0 rows")
        counts = pd.read_sql_query("""SELECT r.region, COUNT(*) AS count_star, COUNT(o.order_id) AS count_order_id
            FROM regions_master r LEFT JOIN orders_clean o ON r.region=o.region
            GROUP BY r.region ORDER BY r.region""", con)
        print("LEFT JOIN null-count comparison:")
        print(counts.to_string(index=False))
        print("Disagreements:")
        print(counts[counts.count_star != counts.count_order_id].to_string(index=False))
        region_counts = pd.read_sql_query("""SELECT r.region, COUNT(o.order_id) AS order_count
            FROM regions_master r LEFT JOIN orders_clean o ON r.region=o.region
            GROUP BY r.region ORDER BY order_count ASC, r.region""", con)
        print("Per-region order counts:")
        print(region_counts.to_string(index=False))
        monthly = pd.read_sql_query("""SELECT r.region, substr(o.order_date,1,7) AS month,
            COALESCE(SUM(o.sales_inr),0) AS sales_inr, COALESCE(SUM(o.profit_inr),0) AS profit_inr,
            COUNT(o.order_id) AS order_count
            FROM regions_master r LEFT JOIN orders_clean o ON r.region=o.region
            GROUP BY r.region, substr(o.order_date,1,7)
            ORDER BY r.region, month""", con)
        # LEFT JOIN with a zero-order region has a NULL month; add all expected month combinations.
        active = pd.read_sql_query("SELECT region FROM regions_master", con)["region"].tolist()
        months = ["2026-04","2026-05","2026-06"]
        grid = pd.MultiIndex.from_product([active, months], names=["region","month"]).to_frame(index=False)
        monthly = grid.merge(monthly.dropna(subset=["month"]), on=["region","month"], how="left").fillna({"sales_inr":0,"profit_inr":0,"order_count":0})
        monthly["order_count"] = monthly["order_count"].astype(int)
        monthly.to_csv("region_month_metrics.csv", index=False)
        print("Saved region_month_metrics.csv")
        return monthly
if __name__ == "__main__": run_queries()
