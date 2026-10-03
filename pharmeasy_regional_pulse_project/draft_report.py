"""Create data-grounded Context–Insight–Implication report blocks."""
import pandas as pd

def draft_report_v1(flagged_regions, metrics):
    """metrics is a DataFrame containing region, month sales, and MoM change columns."""
    if not isinstance(metrics, pd.DataFrame):
        metrics = pd.DataFrame(metrics)
    blocks = []
    for region in sorted(set(flagged_regions)):
        rows = metrics.loc[metrics["region"] == region]
        if rows.empty:
            continue
        row = rows.iloc[0].to_dict()
        changes = []
        for col, label in [("apr_may_change_pct","April→May"),("may_jun_change_pct","May→June")]:
            if col in row and abs(float(row[col])) > 8:
                changes.append(f"{label}: {float(row[col]):+.2f}%")
        blocks.append({
            "region":region,
            "Context":f"{region} regional sales are compared across April, May, and June 2026.",
            "Insight":f"SQL-derived month-on-month sales changes above the 8% operational threshold: {', '.join(changes) if changes else 'no change above threshold in supplied metrics'}.",
            "Implication":"Treat this as a prompt for human review, not proof of a cause; inspect order mix and source operations before taking action."
        })
    return blocks

if __name__ == "__main__":
    metrics = pd.read_csv("mom_changes.csv")
    flags = set(metrics.loc[metrics.apr_may_change_pct.abs()>8,"region"]) | set(metrics.loc[metrics.may_jun_change_pct.abs()>8,"region"])
    for block in draft_report_v1(flags, metrics):
        print(block)
    with open("cii_narrative.md","w",encoding="utf-8") as f:
        f.write("# CII insight narrative\n\n")
        for b in draft_report_v1(flags, metrics):
            f.write(f"## {b['region']}\n\n**Context:** {b['Context']}\n\n**Insight:** {b['Insight']}\n\n**Implication:** {b['Implication']}\n\n")
