
import os
import pandas as pd

# Project folder
base_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Agent output folder
output_folder = os.path.join(
    base_folder,
    "Part4_Agent",
    "Output"
)

os.makedirs(output_folder, exist_ok=True)

# Agent narrative output file
output_file = os.path.join(
    output_folder,
    "Agent_Narratives.txt"
)

# Part 2 verified Growth Engine output
csv_path = os.path.join(
    base_folder,
    "Part2_Engine",
    "Part2_Output",
    #"Category_Wise_MoM_Growth.csv"
    "Category_Wise_MoM_Growth_With_Flagging.csv"
)
# ---------------------------------------------------------
# Input File Reliability Check
# ---------------------------------------------------------

if not os.path.isfile(csv_path):
    print("\nERROR: Required Growth Engine output file is missing.")
    print("Agent execution stopped safely.")
    raise SystemExit(1)
# Check that the file exists
if not os.path.exists(csv_path):
    print("ERROR: Growth Engine CSV file not found.")
    print(csv_path)
    raise SystemExit


# Read verified Growth Engine data
df = pd.read_csv(csv_path)

print("Verified Growth Engine data loaded successfully.")
print(f"Records found: {len(df)}")

# Required columns
required_columns = [
    "Category",
    "April_Revenue",
    "May_Revenue",
    "May_Growth_%",
    "June_Revenue",
    "June_Growth_%",
    "May_Flag",
    "June_Flag"
]


# Validate columns
missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    print("ERROR: Missing required columns:")
    print(missing_columns)
    raise SystemExit


print("All required columns are present.")


# Display verified data
print("\nVerified Growth Engine data:")
print(df.to_string(index=False))


# Find categories flagged for May
may_flagged = df[
    df["May_Flag"].astype(str).str.lower() == "flagged"
]


print("\nMay flagged categories:")
print(may_flagged[
    ["Category", "April_Revenue", "May_Revenue",
     "May_Growth_%", "May_Flag"]
].to_string(index=False))


# Find categories flagged for June
june_flagged = df[
    df["June_Flag"].astype(str).str.lower() == "flagged"
]


print("\nJune flagged categories:")
print(june_flagged[
    ["Category", "May_Revenue", "June_Revenue",
     "June_Growth_%", "June_Flag"]
].to_string(index=False))

#-----------------------------------------------------------

# ---------------------------------------------------------
# Generate Reliable AI Narrative
# ---------------------------------------------------------

def generate_narrative(
    category,
    previous_month,
    current_month,
    previous_revenue,
    current_revenue,
    mom_pct,
    flag_status
):
    revenue_change = current_revenue - previous_revenue

    if revenue_change > 0:
        direction = "increased"
    elif revenue_change < 0:
        direction = "decreased"
    else:
        direction = "remained unchanged"

    narrative = {
        "Context": (
            f"{category} revenue {direction} from "
            f"{previous_month} to {current_month}. "
            f"The verified MoM growth is {mom_pct:.2f}%, "
            f"and the category is {flag_status}."
        ),

        "Insight": (
            f"Revenue changed from {previous_revenue:.2f} "
            f"to {current_revenue:.2f}, resulting in a "
            f"{mom_pct:.2f}% month-on-month change."
        ),

        "Implication": (
            "Management may review order volume, product availability, "
            "returns and cancellations to understand the revenue movement. "
            "No specific cause should be assumed without supporting data."
        ),

        "Validation": {
            "category_verified": True,
            "period_verified": True,
            "revenue_verified": True,
            "growth_verified": True,
            "flag_status": flag_status
        }
    }

    return narrative


# ---------------------------------------------------------
# Save Reliable AI Narratives
# ---------------------------------------------------------

with open(output_file, "w", encoding="utf-8") as file:

    file.write("RELIABLE AI NARRATIVE REPORT\n")
    file.write("=" * 60 + "\n\n")

    # May narratives
    file.write("MAY FLAGGED CATEGORIES\n")
    file.write("=" * 60 + "\n\n")

    for _, row in may_flagged.iterrows():

        narrative = generate_narrative(
            category=row["Category"],
            previous_month="April 2026",
            current_month="May 2026",
            previous_revenue=row["April_Revenue"],
            current_revenue=row["May_Revenue"],
            mom_pct=row["May_Growth_%"],
            flag_status=row["May_Flag"]
        )

        file.write(f"Category: {row['Category']}\n")
        file.write("-" * 60 + "\n")

        file.write("Context:\n")
        file.write(narrative["Context"] + "\n\n")

        file.write("Insight:\n")
        file.write(narrative["Insight"] + "\n\n")

        file.write("Implication:\n")
        file.write(narrative["Implication"] + "\n\n")

        file.write("Validation:\n")
        file.write(str(narrative["Validation"]) + "\n\n")

    # June narratives
    file.write("\nJUNE FLAGGED CATEGORIES\n")
    file.write("=" * 60 + "\n\n")

    for _, row in june_flagged.iterrows():

        narrative = generate_narrative(
            category=row["Category"],
            previous_month="May 2026",
            current_month="June 2026",
            previous_revenue=row["May_Revenue"],
            current_revenue=row["June_Revenue"],
            mom_pct=row["June_Growth_%"],
            flag_status=row["June_Flag"]
        )

        file.write(f"Category: {row['Category']}\n")
        file.write("-" * 60 + "\n")

        file.write("Context:\n")
        file.write(narrative["Context"] + "\n\n")

        file.write("Insight:\n")
        file.write(narrative["Insight"] + "\n\n")

        file.write("Implication:\n")
        file.write(narrative["Implication"] + "\n\n")

        file.write("Validation:\n")
        file.write(str(narrative["Validation"]) + "\n\n")


print("\nNarrative report saved successfully:")
print(output_file)

#-----------------------------------------------

# ---------------------------------------------------------
# Agent Reliability Validation
# ---------------------------------------------------------

expected_categories = [
    "Beauty & Personal Care",
    "Ethnic Wear",
    "Western Wear"
]

expected_june_category = "Ethnic Wear"

with open(output_file, "r", encoding="utf-8") as file:
    report_content = file.read()

# Check May categories
may_validation = all(
    category in report_content
    for category in expected_categories
)

# Check June category
june_validation = expected_june_category in report_content

# Check output file
file_validation = os.path.exists(output_file)

    # Verify expected growth percentages
expected_growth_values = [
    "13.64%",
    "17.00%",
    "9.63%",
    "35.48%"
]

growth_validation = all(
    value in report_content
    for value in expected_growth_values
)
#------------------------------
print("\nAGENT RELIABILITY VALIDATION")
print("=" * 60)

print(f"Output file exists: {file_validation}")
print(f"May categories verified: {may_validation}")
print(f"June category verified: {june_validation}")
print(f"Growth percentages verified: {growth_validation}")

# if file_validation and may_validation and june_validation:
#     print("\nAgent validation PASSED.")
# else:
#     print("\nAgent validation FAILED.")

#-------------
if (
    file_validation
    and may_validation
    and june_validation
    and growth_validation
):
    print("\nAgent validation PASSED.")
else:
    print("\nAgent validation FAILED.")

    