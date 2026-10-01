import os
import random
import pandas as pd

from datetime import datetime, timedelta


# This is the main script to generate the reseller orders data for April, May, and June 2026. It creates a CSV file with the generated data and performs various analyses on it.
#Using Python and Pandas, we generate a dataset of reseller orders for the months of April, May, and June 2026. The dataset includes details such as order ID, order date, reseller information, product category, quantity, unit price, order amount, and order status. The script also performs analyses such as calculating monthly category revenue, region-wise revenue and order count, top resellers by total spend, and identifying zero-order resellers. The results are saved as CSV files for further use.
# ============================================================

# 1. FIXED RANDOM SEED

# ============================================================

# Using 42 means the same data will be generated every time

random.seed(42)



# ============================================================

# 2. MASTER DATA

# ============================================================


# 4 regions and 3 cities per region

regions_cities = {

    "North": ["Delhi", "Jaipur", "Lucknow"],

    "South": ["Chennai", "Bengaluru", "Hyderabad"],

    "East": ["Kolkata", "Bhubaneswar", "Guwahati"],

    "West": ["Mumbai", "Pune", "Ahmedabad"]

}



# 5 product categories

categories = [

    "Ethnic Wear",

    "Western Wear",

    "Kids Wear",

    "Home & Kitchen",

    "Beauty & Personal Care"

]



# Order statuses and their weights

statuses = [

    "Delivered",

    "Returned",

    "Cancelled",

    "Pending"

]


status_weights = [

    0.70,   # Delivered = 70%

    0.15,   # Returned = 15%

    0.10,   # Cancelled = 10%

    0.05    # Pending = 5%

]



# ============================================================

# 3. CREATE 24 RESELLERS

# ============================================================

# 4 regions × 6 resellers = 24 resellers


resellers = []


reseller_number = 1


for region, cities in regions_cities.items():


    for i in range(6):


        reseller = {

            "reseller_id": f"RES{reseller_number:03d}",

            "reseller_name": f"Reseller {reseller_number:02d}",

            "region": region,

            "city": cities[i % 3]

        }


        resellers.append(reseller)


        reseller_number += 1



# ============================================================

# 4. PRICE RANGE FOR EACH CATEGORY

# ============================================================


price_ranges = {


    "Ethnic Wear": (500, 5000),


    "Western Wear": (400, 4000),


    "Kids Wear": (200, 2500),


    "Home & Kitchen": (300, 6000),


    "Beauty & Personal Care": (100, 2500)

}



# ============================================================

# 5. GENERATE ORDERS

# ============================================================


orders = []


order_number = 1



# April, May and June 2026

months = [

    (2026, 4),

    (2026, 5),

    (2026, 6)
]
for year, month in months:
    # First day of current month
    start_date = datetime(year, month, 1)
    # First day of next month
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    # Number of days in current month
    days_in_month = (next_month - start_date).days
    # Exactly 300 orders per month

    for i in range(300):
        # Select random reseller
        reseller = random.choice(resellers)
        # Select random category
        category = random.choice(categories)
        # Select order status according to weights
        order_status = random.choices(
            statuses,
            weights=status_weights,
            k=1
        )[0]
        # Generate random date/time within the month

        order_date = start_date + timedelta(

            days=random.randrange(days_in_month),

            hours=random.randrange(24),

            minutes=random.randrange(60),

            seconds=random.randrange(60)
        )



        # Quantity between 1 and 5

        quantity = random.randint(1, 5)



        # Get price range for selected category

        minimum_price, maximum_price = price_ranges[category]



        # Generate unit price
        unit_price = round(

            random.uniform(

                minimum_price,

                maximum_price

            ),

            2
        )



        # Calculate total order amount
        order_amount = round(

            quantity * unit_price,

            2
        )



        # Create order record

        order = {


            "order_id":

                f"ORD{order_number:04d}",


            "order_date":

                order_date.strftime(

                    "%Y-%m-%d %H:%M:%S"

                ),


            "reseller_id":

                reseller["reseller_id"],


            "reseller_name":

                reseller["reseller_name"],


            "region":

                reseller["region"],


            "city":

                reseller["city"],


            "category":

                category,


            "quantity":

                quantity,


            "unit_price":

                unit_price,


            "order_amount":

                order_amount,


            "order_status":
                order_status

        }



        # Add order to list

        orders.append(order)



        # Increase order number

        order_number += 1



# ============================================================

# 6. CREATE DATAFRAME

# ============================================================

df = pd.DataFrame(orders)

# ============================================================

# 7. CREATE DATA FOLDER

# ============================================================

output_folder = "data"

os.makedirs(

    output_folder,

    exist_ok=True
)
# ============================================================

# 8. SAVE AS CSV

# ============================================================

output_file = os.path.join(

    output_folder,

    "reseller_orders_apr_may_jun_2026.csv"
)

df.to_csv(

    output_file,

    index=False
)

# ============================================================

# 9. DISPLAY RESULTS

# ============================================================

print()
print("==========================================")

print("DATA GENERATION COMPLETE")
print("==========================================")


print(f"Total Orders : {len(df)}")


print(f"CSV File     : {output_file}")


print()

print("Orders by Month:")

month_counts = (

    pd.to_datetime(df["order_date"])

    .dt.to_period("M")

    .value_counts()

    .sort_index()
)

print(month_counts)

print()

print("Orders by Status:")

print(

    df["order_status"]

    .value_counts()
)


print("\nChecking duplicate Order IDs...")  # checking for duplicate order IDs


duplicates = df["order_id"].duplicated().sum()


print("Duplicate Order IDs:", duplicates)

#------------------------------

# checking the number of unique order IDs or missing values in the order_id column

print("\nChecking for missing values...")


missing_values = df.isnull().sum()


print(missing_values)

#------------------------------

#Check the 24 Resellers and 4 Regions

print("\nChecking resellers and regions...")


unique_resellers = df["reseller_id"].nunique()

unique_regions = df["region"].nunique()


print("Unique Resellers:", unique_resellers)

print("Unique Regions:", unique_regions)

#----------------------------
print("===============================================================")

# Check Cities in Each Region

print("\nChecking cities in each region...")
print("===============================================================")

cities_per_region = df.groupby("region")["city"].nunique()


print(cities_per_region)


df.groupby("region")["city"].nunique() # group by region and count unique cities

print("\nChecking categories...")

print(df["category"].value_counts()) # check the number of orders per category

#------------------------------

# Check Orders Per Month

print("\nChecking orders per month...")


df["order_date"] = pd.to_datetime(df["order_date"])


monthly_orders = df.groupby(

    df["order_date"].dt.to_period("M")

).size()


print(monthly_orders)

#------------------------------
print("===============================================================")

#Check Product Category Distribution

print("\nChecking product category distribution...")
print("===============================================================")

category_count = df["category"].value_counts()


print(category_count)

#------------------------------

#Check Order Status Distribution

print("\nChecking order status distribution...")


status_count = df["order_status"].value_counts()

print(status_count)

#------------------------------


#------------------------------
print("===============================================================")

print("\nMonthly Category Revenue:")
print("===============================================================")

df["order_date"] = pd.to_datetime(df["order_date"])


df["month"] = df["order_date"].dt.strftime("%B")


df["revenue"] = df["quantity"] * df["unit_price"]


monthly_category_revenue = (

    df.groupby(["month", "category"])

    .agg(

        revenue=("revenue", "sum"),

        n_orders=("order_id", "count")
    )

    .reset_index()
)


monthly_category_revenue["revenue"] = (

    monthly_category_revenue["revenue"].round(2)
)


monthly_category_revenue = monthly_category_revenue[

    ["month", "category", "revenue", "n_orders"]

]

month_order = ["April", "May", "June"]  # define the desired order of months


monthly_category_revenue["month"] = pd.Categorical(

    monthly_category_revenue["month"],

    categories=month_order,

    ordered=True
)


monthly_category_revenue = monthly_category_revenue.sort_values(

    ["month", "category"]
)

print(monthly_category_revenue.to_string(index=False))
print("===============================================================")

#------------------------------

#Region-wise Revenue & Order Count

print("\nRegion-wise Revenue & Order Count:")
print("===============================================================")

df["revenue"] = df["quantity"] * df["unit_price"]


region_summary = (

    df.groupby("region")

    .agg(

        revenue=("revenue", "sum"),

        n_orders=("order_id", "count")
    )

    .reset_index()
)


# Round revenue to 2 decimal places

region_summary["revenue"] = region_summary["revenue"].round(2)


# Calculate Grand Total

grand_total = pd.DataFrame([{

    "region": "Grand Total",

    "revenue": round(region_summary["revenue"].sum(), 2),

    "n_orders": region_summary["n_orders"].sum()

}])


# Add Grand Total at the bottom

region_summary = pd.concat(

    [region_summary, grand_total],

    ignore_index=True
)




print(region_summary.to_string(index=False))
print("===============================================================")

#------------------------------

# Top 5 Resellers by Total Spend


print("\nTop 5 Resellers by Total Spend:")
print("===============================================================")

df["revenue"] = df["quantity"] * df["unit_price"]


top_5_resellers = (

    df.groupby(["reseller_id", "reseller_name"])

    .agg(

        total_spend=("revenue", "sum"),

        n_orders=("order_id", "count")
    )

    .reset_index()

    .sort_values("total_spend", ascending=False)

    .head(5)
)


top_5_resellers["total_spend"] = (

    top_5_resellers["total_spend"].round(2)
)


print(top_5_resellers.to_string(index=False))
print("===============================================================")

#------------------------------

#Find Zero-Order Resellers

print("\nFinding Zero-Order Resellers:")
print("===============================================================") 


#reseller_master = pd.DataFrame(resellers)  # to find the total number of resellers

#print("\nTotal Resellers:", len(reseller_master))  

#print(reseller_master.head())  

#print("---------------------------------------------------------------")


print("\nZero-Order Resellers:")

# Get all unique resellers from the master list

all_resellers = df[["reseller_id", "reseller_name"]].drop_duplicates()


# Count orders for each reseller

order_counts = df.groupby(

    ["reseller_id", "reseller_name"]

).size().reset_index(name="n_orders")


# Find resellers with zero orders

zero_order_resellers = all_resellers.merge(

    order_counts,

    on=["reseller_id", "reseller_name"],

    how="left"
)


zero_order_resellers["n_orders"] = (

    zero_order_resellers["n_orders"].fillna(0).astype(int)
)


zero_order_resellers = zero_order_resellers[

    zero_order_resellers["n_orders"] == 0

]


print(zero_order_resellers.to_string(index=False))
print("===============================================================")


#print("-------------------------------------------------------------")

# June AOV, Delivered Orders Only

print("\nJune AOV, Delivered Orders Only:")
print("===============================================================")

# df["order_date"] = pd.to_datetime(df["order_date"])


# df["month"] = df["order_date"].dt.strftime("%B")


# df["revenue"] = df["quantity"] * df["unit_price"]

# df["delivered_orders"] = df["order_status"] == "Delivered"  

# df["delivered_revenue"] = df["revenue"].where(df["delivered_orders"]& df["month"] == "June", 0)  # Revenue for delivered orders in June

# df["delivered_order_count"] = df["delivered_orders"].where(df["month"] == "June", 0).astype(int)  # Count of delivered orders in June   

# df["aov_june"] = df["delivered_revenue"] / df["delivered_order_count"].replace(0, pd.NA)  # Avoid division by zero

# import numpy as np

# df["aov_june"] = (
#     df["delivered_revenue"] /
#     df["delivered_order_count"].replace(0, np.nan)
# )

# print("June AOV, Delivered Orders Only: by Status:")

# print(

#     df["aov_june"].round(2)
# )

# df["aov_june"] = (
#     df["delivered_revenue"] /
#     df["delivered_order_count"].replace(0, pd.NA)
# )



# Convert order_date to datetime
df["order_date"] = pd.to_datetime(df["order_date"])

# Get month name
df["month"] = df["order_date"].dt.strftime("%B")

# Calculate revenue for each order
df["revenue"] = df["quantity"] * df["unit_price"]

# Identify delivered orders
df["delivered_orders"] = df["order_status"] == "Delivered"

# Filter only Delivered orders in June
june_delivered = df[
    (df["delivered_orders"]) &
    (df["month"] == "June")
]

# Calculate total delivered revenue for June
june_delivered_revenue = june_delivered["revenue"].sum()

# Count delivered orders in June
june_delivered_order_count = len(june_delivered)

# Calculate June AOV
if june_delivered_order_count > 0:
    aov_june = june_delivered_revenue / june_delivered_order_count
else:
    aov_june = 0

# Display results
#print("June AOV, Delivered Orders Only:")
print("Total Delivered Revenue:", round(june_delivered_revenue, 2))
print("Delivered Order Count:", june_delivered_order_count)
print("June AOV:", round(aov_june, 2))
print("===============================================================")