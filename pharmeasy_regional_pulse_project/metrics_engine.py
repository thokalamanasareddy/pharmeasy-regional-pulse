"""Month-on-month changes, operational alert flags, and JSON state persistence."""
import json
from pathlib import Path

def compute_percentage_change_v1(current, previous):
    if previous == 0:
        return 0
    return round((current - previous) / previous * 100, 2)

def flag_significant_regions_v1(changes, threshold=8):
    """Return region names whose absolute change exceeds the fixed operational threshold."""
    if isinstance(changes, dict):
        return sorted(region for region, change in changes.items() if abs(float(change)) > threshold)
    flagged = []
    for row in changes:
        if abs(float(row["change_pct"])) > threshold:
            flagged.append(row["region"])
    return sorted(set(flagged))

def save_state_v1(month_summary, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(month_summary, f, indent=2, sort_keys=True)

def load_previous_state_v1(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def calculate_changes(metrics_path="region_month_metrics.csv"):
    import pandas as pd
    df = pd.read_csv(metrics_path)
    wide = df.pivot(index="region", columns="month", values="sales_inr").fillna(0)
    rows = []
    for region, row in wide.iterrows():
        apr, may, jun = (float(row.get(m, 0)) for m in ["2026-04","2026-05","2026-06"])
        rows.append({"region":region,"apr_sales":round(apr,2),"may_sales":round(may,2),"jun_sales":round(jun,2),
                     "apr_may_change_pct":compute_percentage_change_v1(may,apr),
                     "may_jun_change_pct":compute_percentage_change_v1(jun,may)})
    out = pd.DataFrame(rows)
    out.to_csv("mom_changes.csv", index=False)
    april_state = {"month":"2026-04","sales_by_region":{r:round(float(v),2) for r,v in wide["2026-04"].items()}}
    save_state_v1(april_state,"state_2026-04.json")
    assert load_previous_state_v1("state_2026-04.json") == april_state
    for previous, current, col in [("2026-04","2026-05","apr_may_change_pct"),("2026-05","2026-06","may_jun_change_pct")]:
        flags = out.loc[out[col].abs() > 8, "region"].tolist()
        print(f"Flags {previous} -> {current}: {', '.join(flags) if flags else 'None'}")
    print(out.to_string(index=False))
    return out
if __name__ == "__main__": calculate_changes()
