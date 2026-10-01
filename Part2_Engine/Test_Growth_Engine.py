
# Apply three-state flagging to May and June growth

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

#-------------------------------------------------- TESTING PURPOSES (VALIDATION)---------------------------------------------

def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
    """Validate the monthly category revenue CSV feed."""

    errors = []

    # 1. Check whether the file exists
    if not os.path.isfile(csv_path):
        return False, ["CSV file does not exist."]

    # 2. Read the CSV
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        return False, [f"Unable to read CSV file: {e}"]

    # 3. Check required columns
    required_columns = [
        "month",
        "category",
        "revenue",
        "n_orders"
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

    # 4. Check for empty file
    if df.empty:
        errors.append("CSV file contains no data rows.")
        return False, errors

    # 5. Check missing values
    for col in required_columns:
        if df[col].isna().any():
            errors.append(
                f"Column '{col}' contains missing values."
            )

    # 6. Check numeric values
    revenue = pd.to_numeric(
        df["revenue"], errors="coerce"
    )

    n_orders = pd.to_numeric(
        df["n_orders"], errors="coerce"
    )

    if revenue.isna().any():
        errors.append("Revenue must contain numeric values.")

    if n_orders.isna().any():
        errors.append("n_orders must contain numeric values.")

    # 7. Check negative values
    if (revenue.dropna() < 0).any():
        errors.append("Revenue cannot be negative.")

    if (n_orders.dropna() < 0).any():
        errors.append("n_orders cannot be negative.")

    # 8. Check order count is a whole number
    if (
        (n_orders.dropna() % 1) != 0
    ).any():
        errors.append("n_orders must be a whole number.")

    # Return validation result
    if errors:
        return False, errors

    return True, []  # TESTING PURPOSES

# --------------------------------------------------
# 1. Month-on-Month Growth Function
# --------------------------------------------------

def mom_growth(previous: float, current: float) -> float:
    """Calculate Month-on-Month growth percentage."""

    if previous == 0:
        return 0.0

    growth = ((current - previous) / previous) * 100

    return round(growth, 2)


# --------------------------------------------------
# 2. Three-State Flagging Function
# --------------------------------------------------

def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    """Return one of three flagging states."""

    if mom_pct == threshold:
        return "escalate_exact_boundary"

    elif mom_pct > threshold:
        return "flagged"

    else:
        return "not_flagged"

#-------------------------------    

# ==========================================
# MAY VS APRIL - FULL MOM RESULTS
# ==========================================

# Database path
base_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

db_path = os.path.join(base_folder, "meesho.db")

conn = sqlite3.connect(db_path)

# Get April and May revenue for all categories
query = """
SELECT
    category,
    strftime('%m', order_date) AS month_number,
    ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
WHERE order_date >= '2026-04-01'
  AND order_date < '2026-06-01'
GROUP BY category, strftime('%m', order_date)
ORDER BY category, month_number;
"""

df = pd.read_sql_query(query, conn)

conn.close()

# Convert rows into category-wise revenue columns
pivot_df = df.pivot(
    index="category",
    columns="month_number",
    values="revenue"
).fillna(0)

# Ensure April and May columns exist
for month in ["04", "05"]:
    if month not in pivot_df.columns:
        pivot_df[month] = 0

results = []

for category, row in pivot_df.iterrows():

    april_revenue = row["04"]
    may_revenue = row["05"]

    growth = mom_growth(april_revenue, may_revenue)

    flag = is_flagged(growth)

    results.append({
        "Category": category,
        "April_Revenue": april_revenue,
        "May_Revenue": may_revenue,
        "May_Growth_%": growth,
        "May_Flag": flag
    })

result_df = pd.DataFrame(results)

# Count flagged categories
flagged_count = (
    result_df["May_Flag"] == "flagged"
).sum()

boundary_count = (
    result_df["May_Flag"] == "escalate_exact_boundary"
).sum()

not_flagged_count = (
    result_df["May_Flag"] == "not_flagged"
).sum()

# Display results
print("\nMAY VS APRIL - FULL MOM RESULTS")
print("=" * 85)

print(result_df.to_string(index=False))

print("\nFLAG SUMMARY")
print("-" * 40)

print("Flagged:", flagged_count)
print("Exact Boundary Escalations:", boundary_count)
print("Not Flagged:", not_flagged_count)

# Save report
output_file = os.path.join(
    output_folder,
    "May_vs_April_Full_MoM_Results.csv"
)

result_df.to_csv(output_file, index=False)

print("\nReport saved as:", output_file)

#---------------------------------------

# ==========================================
# JUNE VS MAY - FULL MOM RESULTS
# ==========================================

# Database path
base_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

db_path = os.path.join(base_folder, "meesho.db")

conn = sqlite3.connect(db_path)

# Get May and June revenue for all categories
query = """
SELECT
    category,
    strftime('%m', order_date) AS month_number,
    ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
WHERE order_date >= '2026-05-01'
  AND order_date < '2026-07-01'
GROUP BY category, strftime('%m', order_date)
ORDER BY category, month_number;
"""

df = pd.read_sql_query(query, conn)

conn.close()

# Convert rows into category-wise revenue columns
pivot_df = df.pivot(
    index="category",
    columns="month_number",
    values="revenue"
).fillna(0)

# Ensure May and June columns exist
for month in ["05", "06"]:
    if month not in pivot_df.columns:
        pivot_df[month] = 0

results = []

for category, row in pivot_df.iterrows():

    may_revenue = row["05"]
    june_revenue = row["06"]

    growth = mom_growth(may_revenue, june_revenue)

    flag = is_flagged(growth)

    results.append({
        "Category": category,
        "May_Revenue": may_revenue,
        "June_Revenue": june_revenue,
        "June_Growth_%": growth,
        "June_Flag": flag
    })

result_df = pd.DataFrame(results)

# Count each flag state
flagged_count = (
    result_df["June_Flag"] == "flagged"
).sum()

boundary_count = (
    result_df["June_Flag"] == "escalate_exact_boundary"
).sum()

not_flagged_count = (
    result_df["June_Flag"] == "not_flagged"
).sum()

# Display results
print("\nJUNE VS MAY - FULL MOM RESULTS")
print("=" * 85)

print(result_df.to_string(index=False))

print("\nFLAG SUMMARY")
print("-" * 40)

print("Flagged:", flagged_count)
print("Exact Boundary Escalations:", boundary_count)
print("Not Flagged:", not_flagged_count)

# Save report
output_file = os.path.join(
    output_folder,
    "June_vs_May_Full_MoM_Results.csv"
)

result_df.to_csv(output_file, index=False)

print("\nReport saved as:", output_file)


# --------------------------------------------------
# 3. Connect to Existing Meesho Database
# --------------------------------------------------

# Database is in the main project folder
base_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

db_path = os.path.join(base_folder, "meesho.db")

conn = sqlite3.connect(db_path)


# --------------------------------------------------
# 4. Fetch Actual Category-wise Monthly Revenue
# --------------------------------------------------

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


# --------------------------------------------------
# 5. Create Category-wise Revenue Table
# --------------------------------------------------

pivot_df = df.pivot(
    index="category",
    columns="month_number",
    values="revenue"
).fillna(0)

# Ensure all three months exist
for month in ["04", "05", "06"]:
    if month not in pivot_df.columns:
        pivot_df[month] = 0

results = []

for category, row in pivot_df.iterrows():

    april = row["04"]
    may = row["05"]
    june = row["06"]

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


# Create the DataFrame
result_df = pd.DataFrame(results)


# --------------------------------------------------
# 6. Apply Three-State Flagging
# --------------------------------------------------

result_df["May_Flag"] = result_df[
    "May_Growth_%"
].apply(is_flagged)

result_df["June_Flag"] = result_df[
    "June_Growth_%"
].apply(is_flagged)


# --------------------------------------------------
# 7. Display Final Results
# --------------------------------------------------

print("\nCATEGORY-WISE MoM GROWTH ENGINE")
print("=" * 100)

print(result_df.to_string(index=False))


# --------------------------------------------------
# 8. Save Final CSV Report
# --------------------------------------------------

output_file = os.path.join(
    output_folder, 
    "Category_Wise_MoM_Growth_With_Flagging.csv"
)

result_df.to_csv(output_file, index=False)

print("\nReport saved as:", output_file)
    
#---------------Test the exact boundary------------

print("7.99%:", is_flagged(7.99))
print("8.00%:", is_flagged(8.00))
print("8.01%:", is_flagged(8.01))


#-------------------------------GIVEBN-WHEN-THEN TEST CASES-----------------------------

import tempfile

# ==========================================
# GIVEN-WHEN-THEN TEST CASES
# ==========================================

print("\nGIVEN-WHEN-THEN TESTING")
print("=" * 50)


# ------------------------------------------
# TEST 1: MoM Growth Calculation
# ------------------------------------------

# GIVEN: Previous revenue is 100000
# WHEN: Current revenue is 125000
# THEN: Growth should be 25%

result = mom_growth(100000, 125000)

assert result == 25.0

print("Test 1 PASSED: MoM Growth = 25%")


# ------------------------------------------
# TEST 2: Zero Previous Revenue
# ------------------------------------------

# GIVEN: Previous revenue is zero
# WHEN: Current revenue is 50000
# THEN: Function should return 0.0

result = mom_growth(0, 50000)

assert result == 0.0

print("Test 2 PASSED: Zero Previous Revenue")


# ------------------------------------------
# TEST 3: Growth Above 8%
# ------------------------------------------

# GIVEN: Growth is 12%
# WHEN: is_flagged() is executed
# THEN: Result should be flagged

result = is_flagged(12.0)

assert result == "flagged"

print("Test 3 PASSED: Growth Above Threshold")


# ------------------------------------------
# TEST 4: Growth Exactly 8%
# ------------------------------------------

# GIVEN: Growth is exactly 8%
# WHEN: is_flagged() is executed
# THEN: Result should be escalated

result = is_flagged(8.0)

assert result == "escalate_exact_boundary"

print("Test 4 PASSED: Exact Boundary")


# ------------------------------------------
# TEST 5: Growth Below 8%
# ------------------------------------------

# GIVEN: Growth is 5%
# WHEN: is_flagged() is executed
# THEN: Result should not be flagged

result = is_flagged(5.0)

assert result == "not_flagged"

print("Test 5 PASSED: Growth Below Threshold")


# ------------------------------------------
# TEST 6: Valid CSV Feed
# ------------------------------------------

# GIVEN: CSV has all required columns
# WHEN: validate_feed() is executed
# THEN: Validation should pass

valid_csv = """month,category,revenue,n_orders
April,Ethnic Wear,100000,50
May,Ethnic Wear,125000,60
"""

with tempfile.NamedTemporaryFile(
    mode="w",
    suffix=".csv",
    delete=False,
    encoding="utf-8"
) as temp_file:

    temp_file.write(valid_csv)
    valid_path = temp_file.name

try:
    is_valid, errors = validate_feed(valid_path)

    assert is_valid is True
    assert errors == []

    print("Test 6 PASSED: Valid CSV Feed")

finally:
    os.remove(valid_path)


# ------------------------------------------
# TEST 7: Missing Required Column
# ------------------------------------------

# GIVEN: CSV is missing n_orders
# WHEN: validate_feed() is executed
# THEN: Validation should fail

invalid_csv = """month,category,revenue
April,Ethnic Wear,100000
"""

with tempfile.NamedTemporaryFile(
    mode="w",
    suffix=".csv",
    delete=False,
    encoding="utf-8"
) as temp_file:

    temp_file.write(invalid_csv)
    invalid_path = temp_file.name

try:
    is_valid, errors = validate_feed(invalid_path)

    assert is_valid is False
    assert any(
        "n_orders" in error for error in errors
    )

    print("Test 7 PASSED: Missing Column Detected")

finally:
    os.remove(invalid_path)


# ------------------------------------------
# TEST 8: Non-Existing CSV File
# ------------------------------------------

# GIVEN: CSV file does not exist
# WHEN: validate_feed() is executed
# THEN: Validation should fail

is_valid, errors = validate_feed(
    "missing_test_file.csv"
)

assert is_valid is False
assert "CSV file does not exist." in errors

print("Test 8 PASSED: Missing File Detected")


print("\nALL 8 TEST CASES COMPLETED SUCCESSFULLY!")

#-------------------------------CORRUPTED FEED - EXACT ERRORS--------------------------


# ==========================================
# TEST 9: CORRUPTED FEED - EXACT ERRORS
# ==========================================

import tempfile

print("\nTEST 9: CORRUPTED FEED")
print("=" * 50)

# GIVEN: A CSV containing multiple data errors
# corrupted_csv = """month,category,revenue,n_orders
# ,Ethnic Wear,abc,1.5
# May,, -100,-2
# June,Kids Wear,200,10
# """


corrupted_csv = """month,category,revenue,n_orders
,Ethnic Wear,abc,invalid
May,, -100,-2
June,Kids Wear,200,1.5
"""

with tempfile.NamedTemporaryFile(
    mode="w",
    suffix=".csv",
    delete=False,
    encoding="utf-8"
) as temp_file:

    temp_file.write(corrupted_csv)
    corrupted_path = temp_file.name


try:
    # WHEN: Validate the corrupted feed
    is_valid, errors = validate_feed(corrupted_path)

    # THEN: Validation must fail
    assert is_valid is False

    # Expected errors in exact order
    expected_errors = [
        "Column 'month' contains missing values.",
        "Column 'category' contains missing values.",
        "Revenue must contain numeric values.",
        "n_orders must contain numeric values.",
        "Revenue cannot be negative.",
        "n_orders cannot be negative.",
        "n_orders must be a whole number."
    ]

    # Compare exact errors and exact order
    assert errors == expected_errors, (
        f"\nExpected:\n{expected_errors}"
        f"\n\nActual:\n{errors}"
    )

    print("Test 9 PASSED: Exact errors and order verified")

    print("\nErrors returned:")
    for error in errors:
        print("-", error)

finally:
    os.remove(corrupted_path)