#---------------------------------- Month-on-Month Growth Calculation ----------------------------------

import sqlite3
import pandas as pd
import os


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

print("Output folder:", output_folder)


# Month-on-Month growth function
def mom_growth(previous: float, current: float) -> float:
    """Calculate Month-on-Month growth percentage."""

    if previous == 0:
        return 0.0

    growth = ((current - previous) / previous) * 100

    return round(growth, 2)


# Connect to our Meesho database
conn = sqlite3.connect("meesho.db")

# Calculate monthly revenue from actual order data
query = """
SELECT
    strftime('%m', order_date) AS month_number,
    CASE strftime('%m', order_date)
        WHEN '04' THEN 'April'
        WHEN '05' THEN 'May'
        WHEN '06' THEN 'June'
    END AS month,
    ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
WHERE order_date >= '2026-04-01'
  AND order_date < '2026-07-01'
GROUP BY strftime('%m', order_date)
ORDER BY month_number;
"""

df = pd.read_sql_query(query, conn)

conn.close()

# Calculate MoM growth
df["mom_growth_percent"] = None

for i in range(len(df)):

    if i == 0:
        df.loc[i, "mom_growth_percent"] = None

    else:
        previous = df.loc[i - 1, "revenue"]
        current = df.loc[i, "revenue"]

        df.loc[i, "mom_growth_percent"] = mom_growth(
            previous, current
        )

# Display the results
print("\nMONTH-ON-MONTH REVENUE GROWTH")
print("--------------------------------")

print(df.to_string(index=False))

# Save the results
#output_file = "Monthly_MoM_Growth.csv"

output_file = os.path.join(
    output_folder,
    "Monthly_MoM_Growth.csv"
)

df.to_csv(output_file, index=False)

print("\nReport saved as:", output_file)

#------------------------------------- Flagging Function ---------------------------------- 


def validate_mom_feed(csv_path: str) -> tuple[bool, list[str]]:
    """Validate the Monthly MoM Growth CSV file."""

    errors = []

    if not os.path.isfile(csv_path):
        return False, ["CSV file does not exist."]

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        return False, [f"Unable to read CSV file: {e}"]

    # Required columns for MoM report
    required_columns = [
        "month_number",
        "month",
        "revenue",
        "mom_growth_percent"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        errors.append(
            f"Missing required columns: {missing_columns}"
        )
        return False, errors

    if df.empty:
        errors.append("CSV file contains no data rows.")
        return False, errors

    # Check revenue values
    revenue = pd.to_numeric(
        df["revenue"], errors="coerce"
    )

    if revenue.isna().any():
        errors.append("Revenue must contain numeric values.")

    elif (revenue < 0).any():
        errors.append("Revenue cannot be negative.")

    # Check MoM growth values
    growth = pd.to_numeric(
        df["mom_growth_percent"], errors="coerce"
    )

    # April growth can be blank because it is the first month
    invalid_growth = (
        df["mom_growth_percent"].notna()
        & growth.isna()
    )

    if invalid_growth.any():
        errors.append(
            "MoM growth must contain numeric values or blanks."
        )

    if errors:
        return False, errors

    return True, []

#-----------------------  FOLDER PATH FOR VALIDATION PURPOSES -----------------------------------
        
# Get the folder where this Python script is located
base_folder = os.path.dirname(os.path.abspath(__file__))

# Use your actual CSV filename
csv_path = os.path.join(
    output_folder,
    "Monthly_MoM_Growth.csv"
)

is_valid, errors = validate_mom_feed(csv_path)

if is_valid:
    print("Feed Validation: PASSED")
else:
    print("Feed Validation: FAILED")

    for error in errors:
        print("-", error)

#----------------------------
