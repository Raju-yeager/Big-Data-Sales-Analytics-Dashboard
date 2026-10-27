# Big Data Sales Analytics Dashboard

A beginner-friendly Big Data subject project built with Python, Pandas, Plotly, and Streamlit. It lets users explore sales data through interactive charts and filters.

## Features
- Total sales, profit, units sold, and average sale metrics
- Filter by order date, region, and product category
- Monthly sales trend chart
- Sales by category and region
- Top 10 products by sales
- View and download filtered data as CSV
- Upload your own sales CSV file

## Files
- `app.py` — Streamlit dashboard source code
- `sales_data.csv` — sample demonstration dataset (synthetic data)
- `requirements.txt` — Python dependencies

## Run on your computer
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the app:
   ```bash
   streamlit run app.py
   ```
5. Your browser should open the dashboard. If it does not, open the local URL printed in the terminal.

## Deploy on Streamlit Community Cloud
1. Create or sign in to a GitHub account.
2. Create a new repository, for example `big-data-sales-analytics`.
3. Upload `app.py`, `sales_data.csv`, `requirements.txt`, and `README.md` to the repository root.
4. Open https://share.streamlit.io/ and connect your GitHub account.
5. Choose **Create app**, select your repository and branch (usually `main`), and set the main file path to `app.py`.
6. Click **Deploy**. Wait for the build to finish; Streamlit will provide a public app URL.

## CSV format for uploading your own data
The uploaded file should contain these columns:
- `Order Date` — date such as `2025-01-31`
- `Region` — sales region
- `Category` — product category
- `Product` — product name
- `Sales` — numeric sales amount
- `Quantity` — numeric quantity sold
- `Profit` — numeric profit amount

An `Order ID` column is optional.

## Important note
The included CSV contains randomly generated synthetic records for learning and demonstration. It is not real company data.
