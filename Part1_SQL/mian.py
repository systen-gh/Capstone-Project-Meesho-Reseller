from asyncio.windows_events import NULL
import sqlite3   # SQl connection checking 

# # Connect to the database

import pandas as pd
#import sqlite3
conn = sqlite3.connect("meesho.db")

#----------------------------- OUTPUT FILE SAVING LOCATION ----------------------------
import os
# Get the main project folder
base_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Set the Part 1 output folder
output_folder = os.path.join(
    base_folder, "Part1_SQL", "Output"
)

# Create the folder if it does not exist
os.makedirs(output_folder, exist_ok=True)

print("Output folder:", output_folder)


print("Connected database:")
print(conn.execute("PRAGMA database_list;").fetchall())

print("\nAvailable tables:")
print(conn.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table';
""").fetchall())

# # Create a cursor
cursor = conn.cursor()

print("Database connected successfully!")

# Close the connection
conn.close()

#------------------- Table Creation -------------------
# Connect to the database
conn = sqlite3.connect("meesho.db")

# Create a cursor
cursor = conn.cursor()

# Create orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT,
    order_date TEXT,
    product_name TEXT,
    quantity INTEGER,
    unit_price REAL,
    order_status TEXT,
    revenue REAL
)
""")

# Save changes
conn.commit()

print("Orders table created successfully!")

# Close connection
conn.close()

#------------------- Data Insertion -------------------
# Read the CSV file
df = pd.read_csv("data/reseller_orders_apr_may_jun_2026.csv")

# Calculate revenue
df["revenue"] = df["quantity"] * df["unit_price"]

# Connect to SQLite database
conn = sqlite3.connect("meesho.db")

# Import CSV data into the orders table
df.to_sql("orders", conn, if_exists="replace", index=False)

print("CSV data imported successfully!")

# Check number of records
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM orders")

print("Total orders:", cursor.fetchone()[0])

conn.close()
#------------------- Query Execution -------------------

conn = sqlite3.connect("meesho.db")

query = """
SELECT region,
       SUM(order_amount) AS total_sales
FROM orders
GROUP BY region
ORDER BY total_sales DESC;
"""

cursor = conn.cursor()

cursor.execute(query)

results = cursor.fetchall()

for row in results:
    print(row)

conn.close()

# List all tables in the database
conn = sqlite3.connect("meesho.db")
cursor = conn.cursor()
cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table';
""")

tables = cursor.fetchall()

print("Tables available in database:")

for table in tables:
    print(table[0])

conn.close()


# Check the columns in orders table
conn = sqlite3.connect("meesho.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(orders);")

columns = cursor.fetchall()

print("Columns in orders table:")

for column in columns:
    print(column[1])

conn.close()

#---------------------------- Monthly Revenue Query ----------------------------
conn = sqlite3.connect("meesho.db")
cursor = conn.cursor()

query = """
SELECT
    strftime('%Y-%m', order_date) AS month,
    SUM(revenue) AS total_revenue
FROM orders
WHERE order_date >= '2026-04-01'
  AND order_date < '2026-07-01'
GROUP BY month
ORDER BY month;
"""

cursor.execute(query)

results = cursor.fetchall()

print("Monthly Revenue - 2026")
print("-----------------------")

for row in results:
    print(row[0], ":", round(row[1], 2))

conn.close()
print("----------------------")

#---------------------------- Monthly Revenue Query ----------------------------


conn = sqlite3.connect("meesho.db")
cursor = conn.cursor()

query = """
SELECT
    strftime('%Y-%m', order_date) AS month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
WHERE order_date >= '2026-04-01'
  AND order_date < '2026-07-01'
GROUP BY
    month,
    category
ORDER BY
    month,
    category;
"""

cursor.execute(query)

results = cursor.fetchall()

print("month       | category             | revenue   | n_orders")

for row in results:
    print(row)

print("Total rows:", len(results))

conn.close()
#----------------------------------------------------------------------

# Connect to the database
conn = sqlite3.connect("meesho.db")

query = """
SELECT
    strftime('%Y-%m', order_date) AS month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
WHERE order_date >= '2026-04-01'
  AND order_date < '2026-07-01'
GROUP BY
    month,
    category
ORDER BY
    month,
    category;
"""

# Execute query and store results in a DataFrame
df = pd.read_sql_query(query, conn)

# Display results
print(df)

# Save output in Part1_SQL / output folder
output_file = os.path.join(
    output_folder,
     "Monthly_Category_Revenue.csv"
)

df.to_csv(output_file, index=False)

print("\nCSV file saved successfully!")
print("File location:", output_file)

conn.close()

#----------------------------- Region wise revenue Query ----------------------------  


# Connect to the database
conn = sqlite3.connect("meesho.db")

# Region-wise Revenue & Order Count
query = """
SELECT
    region,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY region
ORDER BY revenue DESC;
"""

# Execute SQL query
df = pd.read_sql_query(query, conn)

# Display results
print("\nRegion-wise Revenue & Order Count")
print(df)

# Save results as CSV in Part1_SQL / output folder
output_file = os.path.join(
    output_folder,
    "Region_Wise_Revenue_Order_Count.csv"
)

df.to_csv(output_file, index=False)

print("\nCSV file saved successfully!")
print("File location:", output_file)

conn.close()

#----------------------------- Top 5 Resellers by Total Spend ----------------------------
# Connect to the database
conn = sqlite3.connect("meesho.db")

# Top 5 Resellers by Total Spend
query = """
SELECT
    reseller_id,
    reseller_name,
    ROUND(SUM(quantity * unit_price), 2) AS total_spend
FROM orders
GROUP BY
    reseller_id,
    reseller_name
HAVING SUM(quantity * unit_price) > 50000
ORDER BY total_spend DESC
LIMIT 5;
"""

# Execute SQL query
df = pd.read_sql_query(query, conn)

# Display results
print("\nTop 5 Resellers by Total Spend")
print(df)

# Save output to CSV in Part1_SQL / output folder
output_file = os.path.join(
    output_folder,
    "Top_5_Resellers_By_Spend.csv"
)

df.to_csv(output_file, index=False)

print("\nCSV file saved successfully!")
print("File location:", output_file)

conn.close()


#----------------------------- Reseller List ----------------------------


conn = sqlite3.connect("meesho.db")
cursor = conn.cursor()

# Create the resellers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS resellers (
    reseller_id TEXT PRIMARY KEY,
    reseller_name TEXT
)
""")

# Insert unique resellers from orders table
cursor.execute("""
INSERT OR IGNORE INTO resellers (reseller_id, reseller_name)
SELECT DISTINCT reseller_id, reseller_name
FROM orders
WHERE reseller_id IS NOT NULL
""")

conn.commit()

print("Reseller list inserted successfully!")

# Display reseller list
cursor.execute("""
SELECT * FROM resellers
ORDER BY reseller_id
""")

for row in cursor.fetchall():
    print(row)

conn.close()


#----------------------------- zero order resellers ---------------------------- 
# in my database, I have a table named "resellers" that contains information about resellers, including their IDs and names. 
# I also have a table named "orders" that contains information about orders placed by resellers, including the reseller ID associated with each order. 
# I want to find all resellers who have not placed any orders. To do this, I can use a LEFT JOIN between the "resellers" table and the "orders" table, 
# and then filter for resellers where the order ID is NULL.


conn = sqlite3.connect("meesho.db")

query = """
SELECT
    r.reseller_id,
    r.reseller_name
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE o.reseller_id IS NULL;
"""

df = pd.read_sql_query(query, conn)

output_file = os.path.join(
    output_folder,
    "Zero_Order_Resellers.csv"
)

df.to_csv(output_file, index=False)

print(df)
print("CSV saved:", output_file)

conn.close()

#----------------------------- AOV for June ----------------------------

conn = sqlite3.connect("meesho.db")

query = """
SELECT
    ROUND(AVG(order_amount), 2) AS June_AOV
FROM orders
WHERE order_status = 'Delivered'
  AND order_date >= '2026-06-01'
  AND order_date < '2026-07-01';
"""

df = pd.read_sql_query(query, conn)

output_file = os.path.join(
    output_folder,
    "June_AOV_Delivered_Only.csv"
)

df.to_csv(output_file, index=False)

print(df)
print("CSV saved:", output_file)

conn.close()

