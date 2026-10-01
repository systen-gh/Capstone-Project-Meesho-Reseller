import os
import sqlite3
import pandas as pd

# Main project folder
base_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# SQLite database
db_path = os.path.join(base_folder, "meesho.db")

# SQL file location
sql_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Part3_Data_Masking.sql"
)

# Output folder
output_folder = os.path.join(
    base_folder, "Part3_Narrative", "output"
)

os.makedirs(output_folder, exist_ok=True)

# Connect to SQLite
conn = sqlite3.connect(db_path)

# Read SQL file
with open(sql_path, "r", encoding="utf-8") as file:
    sql_script = file.read()

# Execute SQL
conn.executescript(sql_script)
conn.commit()

print("SQL masking completed successfully.")

# Read masked data
masked_df = pd.read_sql_query(
    "SELECT * FROM masked_orders",
    conn
)

# Check that raw reseller name is not present
if "reseller_name" not in masked_df.columns:
    print("PASS: Raw reseller names are excluded.")
else:
    print("FAIL: Raw reseller names found.")

# Save masked data
output_path = os.path.join(
    output_folder,
    "Masked_Orders.csv"
)

masked_df.to_csv(output_path, index=False)

print("Masked data saved to:")
print(output_path)

# Show first 5 records
print("\nSample masked data:")
print(masked_df.head())

conn.close()
