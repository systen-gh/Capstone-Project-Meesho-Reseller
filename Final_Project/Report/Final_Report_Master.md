# MEESHO RESELLER REVENUE ANALYTICS
## Reliable Data Analysis, Growth Monitoring and AI-Assisted Business Narrative

### Capstone Project Report

**Project:** Meesho Reseller Revenue Analytics  
**Project Type:** Data Analytics / Reliable AI Analytics  
**Technology:** Python, SQLite, SQL, Pandas  
**Analysis Period:** April 2026 – June 2026  

---

# 1. Executive Summary

The Meesho Reseller Revenue Analytics project demonstrates an end-to-end data analytics workflow for analyzing reseller order and revenue information.

The project was designed to transform raw reseller order data into verified business insights through SQL analysis, Month-on-Month growth monitoring, reliable narrative generation, data masking, and a local revenue analysis agent.

The project uses a simulated dataset containing 900 orders covering April, May, and June 2026. The dataset includes 24 resellers distributed across four regions, with three cities represented in each region.

The analytical pipeline consists of four major parts:

1. SQL-based revenue analysis
2. A Month-on-Month Growth Engine
3. Reliable AI narrative preparation with data masking
4. A reliable revenue analysis agent

A threshold of more than 8% Month-on-Month growth is used to identify categories requiring attention.

The verified results show that:

- Beauty & Personal Care grew by 13.64% from April to May.
- Ethnic Wear grew by 17.00% from April to May.
- Western Wear grew by 9.63% from April to May.
- Ethnic Wear grew by 35.48% from May to June.

The project also demonstrates reliability controls, including validation of source data, verification of growth calculations, masking of reseller identifiers, negative testing, and safe failure when required input files are unavailable.

The complete workflow operates locally and does not require an external API key.

---

# 2. Business Problem

Reseller businesses generate large volumes of transactional information through orders, products, quantities, prices, revenue, returns, cancellations, and reseller activity.

Raw transactional data alone does not provide management with immediate answers to questions such as:

- Which categories are growing?
- Which categories require attention?
- How is revenue changing month over month?
- Which regions generate higher revenue?
- Which resellers contribute significant spending?
- How can revenue changes be communicated clearly?
- How can sensitive reseller information be protected?
- How can automated analysis avoid unsupported assumptions?

The objective of this project is to build a structured analytics workflow that converts transactional data into reliable and understandable business information.

The project focuses not only on calculating results, but also on ensuring that the reported insights remain connected to verified source data.

---

# 3. Project Objectives

The main objectives are:

1. Generate a structured reseller order dataset.
2. Store and analyze the data using SQLite.
3. Calculate category-wise and region-wise revenue.
4. Calculate Month-on-Month revenue growth.
5. Identify categories exceeding the defined 8% growth threshold.
6. Generate concise evidence-based business narratives.
7. Mask reseller identifiers before narrative processing.
8. Build a local revenue analysis agent.
9. Validate calculations and outputs.
10. Demonstrate safe failure when required inputs are missing.
11. Maintain a complete and reproducible project workflow.
12. Produce professional documentation suitable for a capstone project.

---

# 4. Dataset Description

The project uses a simulated reseller order dataset.

## 4.1 Dataset Summary

| Item | Value |
|---|---:|
| Total Orders | 900 |
| Analysis Period | April–June 2026 |
| Orders per Month | 300 |
| Total Resellers | 24 |
| Regions | 4 |
| Cities per Region | 3 |
| Product Categories | 5 |
| Duplicate Order IDs | 0 |

## 4.2 Product Categories

The dataset contains the following categories:

- Ethnic Wear
- Western Wear
- Kids Wear
- Home & Kitchen
- Beauty & Personal Care

## 4.3 Order Status

The generated dataset uses the following status distribution:

- Delivered — 70%
- Returned — 15%
- Cancelled — 10%
- Pending — 5%

## 4.4 Dataset Generation

The dataset is generated using Python and a fixed random seed.

The fixed seed ensures that the generated dataset is deterministic and reproducible.

The project therefore allows the dataset to be regenerated using the same generation logic.

---

# 5. Technology Stack

The project uses the following technologies:

| Technology | Purpose |
|---|---|
| Python | Data generation and analytical processing |
| Pandas | Data handling and CSV processing |
| SQLite | Local database storage and SQL analysis |
| SQL | Revenue and business analysis |
| VS Code | Development environment |
| Markdown | Project documentation |
| CSV | Analytical data exchange |
| Git-style project structure | Organized project workflow |

The project does not require an external AI API key.

---

# 6. Project Architecture

The project follows a sequential analytical pipeline.

```text
Raw / Generated Dataset
        |
        v
   Part 1 — SQL
        |
        | Verified Revenue Results
        v
   Part 2 — Growth Engine
        |
        | Verified MoM Growth + Flags
        v
   Part 3 — Reliable Narrative
        |
        | Masked Data + Evidence-Based Narrative
        v
   Part 4 — Revenue Analysis Agent
        |
        v
   Final Reports / Business Insights

   The workflow separates data preparation, analysis, growth detection, narrative generation, and agent validation.

This separation improves traceability and makes it easier to identify where an error occurs.

7. Part 1 — SQL Analysis

Part 1 establishes the verified analytical foundation of the project.

The SQLite database contains the orders table with the following fields:

order_id
order_date
reseller_id
reseller_name
region
city
category
quantity
unit_price
order_amount
order_status
revenue

SQL queries were used to produce several business reports.

7.1 Monthly Category Revenue

Revenue was calculated using:

quantity × unit_price

The analysis produces category-level revenue for April, May, and June 2026.

The report also includes the number of orders for each category and month.

7.2 Region-Wise Revenue and Order Count

Revenue and order counts were aggregated by region.

A grand total row was included to provide a complete summary.

7.3 Top Resellers by Total Spend

The project identifies the top five resellers based on total spend.

The analysis applies a minimum spend condition of:

total_spend > 50,000

The results are sorted by total spend in descending order.

7.4 June Average Order Value

June Average Order Value was calculated using delivered orders only.

This provides a more focused measure of completed order value.

7.5 Data Quality Check

Duplicate Order IDs were checked.

Verified result:

Duplicate Order IDs = 0

This provides a basic integrity check for the transactional dataset.

8. Part 2 — Growth Engine

The Growth Engine calculates Month-on-Month revenue growth.

The calculation is:

MoM Growth % =
((Current Revenue - Previous Revenue) / Previous Revenue) × 100

The calculated value is rounded to two decimal places.

8.1 Growth Threshold

The project uses an 8% threshold.

The flagging logic is:

MoM Growth > 8%
        → flagged

MoM Growth = 8%
        → escalate_exact_boundary

MoM Growth < 8%
        → not_flagged

Negative growth is not automatically classified as flagged because the defined rule specifically identifies growth above the 8% threshold.

8.2 Verified Category Results
May 2026 compared with April 2026
Category	April Revenue	May Revenue	Growth	Flag
Beauty & Personal Care	207,421.46	235,710.83	13.64%	Flagged
Ethnic Wear	421,858.43	493,572.34	17.00%	Flagged
Home & Kitchen	619,987.73	494,285.21	-20.28%	Not Flagged
Kids Wear	241,899.28	243,977.89	0.86%	Not Flagged
Western Wear	391,501.83	429,203.55	9.63%	Flagged
June 2026 compared with May 2026
Category	May Revenue	June Revenue	Growth	Flag
Beauty & Personal Care	235,710.83	238,323.37	1.11%	Not Flagged
Ethnic Wear	493,572.34	668,716.09	35.48%	Flagged
Home & Kitchen	494,285.21	479,068.32	-3.08%	Not Flagged
Kids Wear	243,977.89	186,472.78	-23.57%	Not Flagged
Western Wear	429,203.55	382,377.37	-10.91%	Not Flagged

The Growth Engine therefore provides a clearly defined and reproducible method for identifying threshold-exceeding category growth.

9. Part 3 — Reliable AI Narrative and Data Masking

Part 3 focuses on communicating verified numbers safely.

The narrative framework uses three sections:

Context

Describes what happened using verified figures.

Insight

Explains what the numbers show.

Implication

Provides a practical management consideration without assuming an unsupported cause.

The narrative rules explicitly prohibit inventing:

Causes
Trends
Sustainability
Missing values
Business facts not present in the supplied data

If the available information is insufficient, the narrative should state that further investigation is required.

10. Data Masking

Before narrative processing, reseller identifiers are masked.

A mapping table is used to convert actual reseller IDs into identifiers such as:

Reseller_001
Reseller_002
Reseller_003

A masked view is then created for analytical processing.

The masked dataset excludes the raw reseller name.

This reduces direct exposure of reseller identifiers during downstream narrative processing.

However, the masking approach is pseudonymization rather than complete anonymization because the private mapping table can reconnect the masked identifier to the original reseller.

11. Chart Selection

The project documents chart selection based on the business question rather than visual preference.

Examples include:

Monthly Revenue Comparison

A bar chart is appropriate when comparing revenue values across discrete months.

Category Share of Revenue

A pie chart can be used when showing a category's proportion of a meaningful total.

For example, Ethnic Wear represented 24.92% of April total revenue.

Regional Revenue Comparison

A bar chart provides a direct comparison of revenue across the four regions.

The project follows basic visualization principles such as avoiding unnecessary 3D effects and using clear axes.

12. Part 4 — Reliable Revenue Analysis Agent

Part 4 implements a local/mock revenue analysis agent.

The agent receives verified analytical information from the Growth Engine.

Possible inputs include:

Month
Previous month
Category
Previous revenue
Current revenue
MoM growth percentage
Flag status
Region
Total revenue

The agent produces three primary narrative sections:

Context
Insight
Implication

It also produces validation information.

The agent does not connect to an external AI service.

Therefore, the current implementation demonstrates the architecture and reliability workflow without requiring an API key.

13. Agent Reliability Validation

The agent performs validation before completing the workflow.

The following checks were successfully verified:

Output file exists: True
May categories verified: True
June category verified: True
Growth percentages verified: True

Agent validation PASSED.

The validation confirms that the expected categories and growth percentages are consistent with the Growth Engine output.

14. Negative Testing

A negative test was performed by temporarily changing the required Growth Engine output filename.

The agent then produced:

ERROR: Required Growth Engine output file is missing.
Agent execution stopped safely.

This demonstrates that the agent does not continue processing when its required input is unavailable.

The original filename was subsequently restored and the normal functional test passed.

This provides evidence of safe failure behavior.

15. Key Verified Findings

The following findings were verified from the project outputs.

May 2026

Three categories exceeded the 8% growth threshold:

Beauty & Personal Care — 13.64%
Ethnic Wear — 17.00%
Western Wear — 9.63%
June 2026

One category exceeded the 8% growth threshold:

Ethnic Wear — 35.48%

Other June category movements included:

Beauty & Personal Care — 1.11%
Home & Kitchen — -3.08%
Kids Wear — -23.57%
Western Wear — -10.91%

The flagging result should be interpreted strictly according to the project's rule: a category is flagged when its positive MoM growth exceeds 8%.

A flag does not establish why the revenue changed.

16. Data Privacy and Reliability

Reliability is implemented at several stages of the project.

Data Validation

The project checks data integrity before analysis.

Calculation Validation

Growth calculations are independently checked against expected results.

Input Validation

The agent verifies that required input files exist.

Output Validation

The project verifies that expected output files are generated.

Data Masking

Reseller identifiers are masked before narrative processing.

Negative Testing

The project tests missing-input behavior.

Safe Failure

The agent stops rather than generating unsupported results when required input is unavailable.

Evidence-Based Narratives

The narrative generation rules prevent unsupported causes or explanations from being presented as facts.

17. Reliability Principles

The project follows these principles:

Use verified source data.
Preserve numerical accuracy.
Separate facts from assumptions.
Do not invent missing information.
Validate calculations.
Validate input and output files.
Protect reseller identifiers through masking.
Stop safely when required information is unavailable.
Clearly identify limitations.
Maintain reproducibility through deterministic data generation.
18. Limitations

The project has several limitations.

Simulated Dataset

The dataset is generated for project and demonstration purposes and does not represent actual Meesho production data.

Limited Time Period

The analysis covers only April, May, and June 2026.

Longer-term seasonal and annual patterns cannot therefore be established from this dataset alone.

Limited Business Variables

The dataset does not contain every possible business variable, such as:

Marketing expenditure
Inventory levels
Supplier information
Customer acquisition cost
Product-level profitability
Promotional campaigns
Delivery performance
Local Mock Agent

The current revenue analysis agent is a local/mock implementation rather than a production AI service.

No Real-Time Data

The current pipeline processes locally available data and does not connect to a live production database.

Limited Cause Analysis

Revenue movements are identified, but the project does not independently establish the business causes behind those movements.

Masking Limitation

The masking mechanism is pseudonymization and should not be considered complete anonymization.

19. Future Enhancements

Future versions could include:

Connection to a production database.
Automated data ingestion.
Scheduled analytical pipelines.
Interactive dashboards.
Real-time KPI monitoring.
Automated business alerts.
Integration with a production AI model.
Advanced anomaly detection.
Additional business KPIs.
Role-based access control.
Stronger privacy controls.
Automated PDF and presentation generation.
Historical trend analysis.
Product-level profitability analysis.
Inventory and availability analysis.
Automated management reporting.

A production implementation could connect the verified analytics layer to an enterprise reporting platform while maintaining validation and privacy controls.

20. Conclusion

The Meesho Reseller Revenue Analytics project demonstrates how transactional data can be transformed into structured and validated business insights.

The project combines:

SQL analysis
Python processing
Month-on-Month growth analysis
Threshold-based flagging
Data masking
Evidence-based narrative generation
Agent validation
Negative testing
Safe failure handling

The workflow emphasizes reliability rather than simply producing analytical output.

The project also demonstrates that an AI-assisted analytics workflow can be designed to work from verified numbers while explicitly separating facts from assumptions.

The current implementation provides a foundation that can be extended into a production analytics and AI-assisted reporting system.

21. Appendix A — Project Structure
Capstone Project_Messo Reseller
│
├── .vscode
├── data
├── tasks
│
├── Part1_SQL
│   ├── main.py
│   ├── Queries.sql
│   ├── SQLite.sql
│   └── output
│
├── Part2_Engine
│   ├── Growth_Engine.py
│   ├── Quick_Check.py
│   ├── Test_Growth_Engine.py
│   └── output
│
├── Part3_Narrative
│   ├── Part3_Data_Masking.sql
│   ├── Quick_Mask_Check.py
│   ├── prompt_pack.md
│   └── output
│
├── Part4_Agent
│   ├── Agent_Spec.md
│   ├── Mock_Agent_Runner.py
│   ├── Agent_Test_Report.txt
│   ├── Part4_Summary.txt
│   └── output
│
├── Final_Project
│   ├── Report
│   ├── Presentation
│   └── Evidence
│
├── meesho.db
└── README.md
22. Appendix B — Execution Commands
Dataset Generation
cd Part1_SQL
python main.py
Part 1 SQL Analysis

Open:

Part1_SQL\Queries.sql

Execute the SQL using the SQLite extension in VS Code.

Part 2 Growth Engine
cd Part2_Engine
python Growth_Engine.py
Part 3 Data Masking
cd Part3_Narrative
python Quick_Mask_Check.py
Part 4 Revenue Analysis Agent
cd Part4_Agent
python Mock_Agent_Runner.py
23. Appendix C — Workflow Dependency
Part 1
SQL Analysis
    |
    v
Verified Revenue Data
    |
    v
Part 2
Growth Engine
    |
    v
MoM Growth + Flag Status
    |
    +--------------------+
    |                    |
    v                    v
Part 3                Part 4
Narrative             Revenue Agent
+ Masking             + Validation
    |                    |
    +---------+----------+
              |
              v
       Reliable Business
           Reporting
24. Appendix D — Final Validation

The completed project includes validation for:

Duplicate Order IDs
Revenue calculations
MoM growth calculations
Threshold flagging
Expected flagged categories
Masked data output
Agent output existence
May category verification
June category verification
Growth percentage verification
Missing-input negative testing
Safe agent failure

Final agent validation:

AGENT RELIABILITY VALIDATION
============================================================
Output file exists: True
May categories verified: True
June category verified: True
Growth percentages verified: True

Agent validation PASSED.
25. Appendix E — Zero API Key Architecture

The complete project currently operates without external API credentials.

Python
   |
   +---- Dataset Generation
   |
SQLite
   |
   +---- SQL Analysis
   |
Python Growth Engine
   |
   +---- MoM Calculation
   +---- Threshold Flagging
   |
Data Masking
   |
   +---- Protected Reseller Identifiers
   |
Local Revenue Analysis Agent
   |
   +---- Narrative Generation
   +---- Validation
   |
Final Business Reporting

This architecture makes the project reproducible in a local development environment without depending on an external AI API.