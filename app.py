import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Big Data Sales Analytics", page_icon="📊", layout="wide")

st.title("📊 Big Data Sales Analytics Dashboard")
st.caption("Explore sales performance, products, customers, and regional trends using an interactive dashboard.")

@st.cache_data
def load_default_data():
    data_path = Path(__file__).parent / "sales_data.csv"
    return pd.read_csv(data_path, parse_dates=["Order Date"])

def clean_data(df):
    df = df.copy()
    required = ["Order Date", "Region", "Category", "Product", "Sales", "Quantity", "Profit"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        st.error("Missing required columns: " + ", ".join(missing))
        st.info("Required columns: " + ", ".join(required))
        st.stop()
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    for col in ["Sales", "Quantity", "Profit"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["Order Date", "Region", "Category", "Product", "Sales", "Quantity", "Profit"])
    return df

with st.sidebar:
    st.header("Data")
    uploaded_file = st.file_uploader("Upload your own sales CSV (optional)", type=["csv"])
    st.caption("No upload? The included sample dataset loads automatically.")

try:
    raw_df = pd.read_csv(uploaded_file, parse_dates=["Order Date"]) if uploaded_file else load_default_data()
except Exception as exc:
    st.error(f"Could not read the CSV file: {exc}")
    st.stop()

df = clean_data(raw_df)

with st.sidebar:
    st.header("Filters")
    min_date = df["Order Date"].min().date()
    max_date = df["Order Date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    regions = sorted(df["Region"].dropna().unique().tolist())
    categories = sorted(df["Category"].dropna().unique().tolist())
    chosen_regions = st.multiselect("Region", regions, default=regions)
    chosen_categories = st.multiselect("Category", categories, default=categories)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = df[
    df["Order Date"].dt.date.between(start_date, end_date)
    & df["Region"].isin(chosen_regions)
    & df["Category"].isin(chosen_categories)
]

if filtered.empty:
    st.warning("No sales records match these filters. Adjust the filters in the sidebar.")
    st.stop()

total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
total_quantity = filtered["Quantity"].sum()
avg_order_sale = filtered["Sales"].mean()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Sales", f"${total_sales:,.2f}")
m2.metric("Total Profit", f"${total_profit:,.2f}")
m3.metric("Units Sold", f"{total_quantity:,.0f}")
m4.metric("Average Sale / Row", f"${avg_order_sale:,.2f}")

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("Sales over time")
    monthly = filtered.assign(Month=filtered["Order Date"].dt.to_period("M").astype(str)).groupby("Month", as_index=False)["Sales"].sum()
    fig = px.line(monthly, x="Month", y="Sales", markers=True, title="Monthly sales")
    fig.update_layout(xaxis_title="Month", yaxis_title="Sales ($)")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Sales by category")
    category_sales = filtered.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig = px.bar(category_sales, x="Category", y="Sales", color="Category", title="Sales by product category")
    fig.update_layout(showlegend=False, xaxis_title="Category", yaxis_title="Sales ($)")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Sales by region")
    region_sales = filtered.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig = px.pie(region_sales, names="Region", values="Sales", hole=0.35, title="Regional sales share")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Top 10 products")
    product_sales = filtered.groupby("Product", as_index=False)["Sales"].sum().nlargest(10, "Sales").sort_values("Sales")
    fig = px.bar(product_sales, x="Sales", y="Product", orientation="h", title="Top products by sales")
    fig.update_layout(xaxis_title="Sales ($)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Sales data")
st.dataframe(filtered.sort_values("Order Date", ascending=False), use_container_width=True, hide_index=True)
csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download filtered data as CSV", data=csv_bytes, file_name="filtered_sales_data.csv", mime="text/csv")

st.caption("Note: This project includes synthetic sample data for demonstration. Replace it with your own dataset for real business insights.")
