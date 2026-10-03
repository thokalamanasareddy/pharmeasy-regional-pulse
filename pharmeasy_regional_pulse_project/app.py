"""Local Streamlit dashboard for PharmEasy Regional Pulse."""
import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="PharmEasy Regional Pulse", layout="wide")
st.title("PharmEasy Regional Pulse")
st.caption("Regional performance intelligence · April–June 2026 · Local-only dashboard")

@st.cache_data
def load_data():
    with sqlite3.connect("pharmeasy.db") as con:
        orders = pd.read_sql_query("SELECT * FROM orders_clean", con)
        regions = pd.read_sql_query("SELECT * FROM regions_master", con)
    orders["month"] = orders["order_date"].astype(str).str[:7]
    orders["sales_inr"] = pd.to_numeric(orders["sales_inr"], errors="coerce").fillna(0)
    orders["profit_inr"] = pd.to_numeric(orders["profit_inr"], errors="coerce").fillna(0)
    return orders, regions

try:
    orders, regions = load_data()
except Exception:
    st.error("Database not found. From the repository root, run `python3 generate_dataset.py`, `python3 clean_data.py`, and `python3 build_db.py`, then run `python3 queries.py` and `python3 metrics_engine.py`.")
    st.stop()

month_options = sorted(orders["month"].unique())
selected_month = st.selectbox("Reporting month", month_options, index=len(month_options)-1)
region_options = ["All regions"] + sorted(regions["region"].tolist())
selected_region = st.selectbox("Region filter (updates all views)", region_options)
filtered = orders[orders["month"] == selected_month].copy()
if selected_region != "All regions":
    filtered = filtered[filtered["region"] == selected_region]
total_sales = filtered["sales_inr"].sum()
total_profit = filtered["profit_inr"].sum()
order_count = filtered["order_id"].nunique()

st.subheader("Executive summary")
if selected_region == "All regions":
    summary = f"In {selected_month}, the selected dataset contains {order_count:,} distinct orders, INR {total_sales:,.2f} in sales, and INR {total_profit:,.2f} in estimated/recorded profit. The view is filtered to {selected_month}; use the trend chart to compare regional sales across the three available months. Category totals show how sales are distributed across the six categories, while the region comparison highlights differences in scale. Changes over the 8% operational threshold are review prompts rather than proof of cause. Use the region filter and detail table below to investigate the records behind a pattern."
else:
    summary = f"In {selected_month}, {selected_region} has {order_count:,} distinct orders, INR {total_sales:,.2f} in sales, and INR {total_profit:,.2f} in estimated/recorded profit. The trend chart places this region in the April–June context. Category totals show the distribution of this region's sales across categories. Any month-on-month movement should be reviewed alongside order counts and category mix before assigning a cause. Use the detail table to inspect the underlying orders."
st.write(summary)

c1,c2,c3 = st.columns(3)
c1.metric("Total sales (INR)", f"₹{total_sales:,.2f}")
c2.metric("Total profit (INR)", f"₹{total_profit:,.2f}")
c3.metric("Distinct order count", f"{order_count:,}")

st.subheader("Trend: How did monthly sales change by region?")
trend = orders.copy()
if selected_region != "All regions":
    trend = trend[trend.region == selected_region]
trend = trend.groupby(["month","region"],as_index=False).sales_inr.sum()
fig_line = px.line(trend,x="month",y="sales_inr",color="region",markers=True,title="Monthly sales by region (INR)")
fig_line.update_yaxes(rangemode="tozero",title="Sales (INR)")
fig_line.update_xaxes(title="Month")
st.plotly_chart(fig_line,use_container_width=True)

st.subheader("Comparison: Which regions generated the most sales?")
comparison = orders[orders.month == selected_month]
if selected_region != "All regions":
    comparison = comparison[comparison.region == selected_region]
comparison = comparison.groupby("region",as_index=False).sales_inr.sum().sort_values("sales_inr",ascending=False)
fig_bar = px.bar(comparison,x="region",y="sales_inr",title=f"Regional sales comparison — {selected_month}")
fig_bar.update_yaxes(rangemode="tozero",title="Sales (INR)")
fig_bar.update_xaxes(title="Region")
st.plotly_chart(fig_bar,use_container_width=True)

st.subheader("Category: What share of sales comes from each category?")
category = filtered.groupby("category",as_index=False).sales_inr.sum()
fig_pie = px.pie(category,names="category",values="sales_inr",hole=.38,title=f"Sales share by category — {selected_month}")
st.plotly_chart(fig_pie,use_container_width=True)

st.subheader("Detail: Regional and monthly metrics")
detail = orders.copy()
if selected_region != "All regions":
    detail = detail[detail.region == selected_region]
detail = detail.groupby(["region","month"],as_index=False).agg(sales_inr=("sales_inr","sum"),profit_inr=("profit_inr","sum"),order_count=("order_id","nunique"))
st.dataframe(detail.sort_values(["region","month"]),use_container_width=True)

st.subheader("Order-level detail")
st.dataframe(filtered.sort_values(["region","order_date","order_id"]),use_container_width=True)
st.caption("Profit values with missing source data were imputed using the observed category-level mean profit margin. All results are local and require no API key.")
