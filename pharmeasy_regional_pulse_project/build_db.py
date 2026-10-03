"""Load the cleaned orders and region master into SQLite."""
import sqlite3
import pandas as pd

def build_db(clean_path="orders_clean.csv", master_path="regions_master.csv", db_path="pharmeasy.db"):
    orders = pd.read_csv(clean_path)
    regions = pd.read_csv(master_path)
    with sqlite3.connect(db_path) as con:
        regions.to_sql("regions_master", con, if_exists="replace", index=False)
        orders.to_sql("orders_clean", con, if_exists="replace", index=False)
        con.execute("CREATE INDEX IF NOT EXISTS idx_orders_region ON orders_clean(region)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_orders_date ON orders_clean(order_date)")
    print(f"Built {db_path}: {len(regions)} regions, {len(orders)} orders.")
if __name__ == "__main__": build_db()
