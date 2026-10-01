
import os
import sqlite3
import pandas as pd


def mom_growth(previous: float, current: float) -> float:
    """Calculate Month-on-Month growth percentage. CATEGORY WISE."""

    if previous == 0:
        return 0.0

    growth = ((current - previous) / previous) * 100

    return round(growth, 2)


# Connect to the Meesho database
conn = sqlite3.connect("meesho.db")

# Get category-wise monthly revenue from actual data
query = """
SELECT
    category,
    strftime('%m', order_date) AS month_number,
    ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
WHERE order_date >= '2026-04-01'
  AND order_date < '2026-07-01'
GROUP BY category, strftime('%m', order_date)
ORDER BY category, month_number;
"""

df = pd.read_sql_query(query, conn)

conn.close()

# Convert monthly data into separate columns
pivot_df = df.pivot(
    index="category",
    columns="month_number",
    values="revenue"
).fillna(0)

# Calculate MoM growth for each category
results = []

for category, row in pivot_df.iterrows():

    april = row.get("04", 0)
    may = row.get("05", 0)
    june = row.get("06", 0)

    may_growth = mom_growth(april, may)
    june_growth = mom_growth(may, june)

    results.append({
        "Category": category,
        "April_Revenue": april,
        "May_Revenue": may,
        "May_Growth_%": may_growth,
        "June_Revenue": june,
        "June_Growth_%": june_growth
    })

# Create final report
result_df = pd.DataFrame(results)

# Print results
print("\nCATEGORY-WISE MONTH-ON-MONTH REVENUE GROWTH")
print("=" * 75)

print(result_df.to_string(index=False))

# Save report
#output_file = "Category_Wise_MoM_Growth.csv"

# Get the main project folder
base_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Set the Part 2 output folder
output_folder = os.path.join(
    base_folder, "Part2_Engine", "Part2_Output"
)

# Create the folder if it does not exist
os.makedirs(output_folder, exist_ok=True)

result_df.to_csv(os.path.join(output_folder,"Category_Wise_MoM_Growth.csv"), index=False)

print("\nReport saved as:", "Category_Wise_MoM_Growth.csv")

#----------------------------------

