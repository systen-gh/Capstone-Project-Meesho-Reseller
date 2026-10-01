# Meesho Reseller — Reliable Revenue Analytics Capstone Project

## 1. Project Overview

This project is a complete revenue analytics pipeline for a simulated Meesho reseller business.

The project demonstrates how raw order data can be transformed into verified business insights through:

- Python-based dataset generation
- SQLite data analysis
- Month-on-Month (MoM) growth calculations
- Rule-based flagging
- Data masking
- Reliable AI-style narrative generation
- Agent-based revenue analysis
- Validation and safe-failure handling

The complete pipeline is designed to run locally and requires **zero external API keys**.

---

## 2. Business Problem

A reseller business needs a reliable way to analyze order and revenue data and identify meaningful month-on-month revenue movements.

The project addresses the following questions:

- How much revenue was generated each month?
- Which product categories generated the revenue?
- How did category revenue change month over month?
- Which categories exceeded the defined growth threshold?
- How can reseller information be masked before further analysis?
- How can verified numbers be converted into concise management narratives?
- How can an analysis agent validate its inputs and outputs before producing results?

The main focus is **reliable, evidence-based revenue analysis** rather than unsupported business assumptions.

---

## 3. Project Objectives

The project aims to:

1. Generate a reproducible reseller order dataset.
2. Store and analyze the data using SQLite.
3. Produce verified revenue reports using SQL.
4. Calculate Month-on-Month revenue growth using Python.
5. Apply deterministic growth flagging rules.
6. Protect reseller identity using data masking.
7. Generate structured business narratives from verified numbers.
8. Build a local revenue analysis agent.
9. Validate agent outputs against verified source data.
10. Demonstrate safe failure when required input files are missing.
11. Create a complete, auditable analytics workflow.

---

## 4. Dataset Description

The dataset contains **900 reseller orders** covering:

- April 2026
- May 2026
- June 2026

### Dataset Structure

| Attribute | Description |
|---|---|
| Total Orders | 900 |
| Monthly Orders | 300 per month |
| Resellers | 24 |
| Regions | 4 |
| Cities | 3 per region |
| Categories | 5 |
| Analysis Period | April–June 2026 |

### Product Categories

- Ethnic Wear
- Western Wear
- Kids Wear
- Home & Kitchen
- Beauty & Personal Care

### Order Status Distribution

The dataset uses the following status weights:

- Delivered — 70%
- Returned — 15%
- Cancelled — 10%
- Pending — 5%

A fixed random seed is used during dataset generation so that the dataset can be reproduced consistently.

---

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Dataset generation, calculations and agent processing |
| Pandas | Data processing and CSV generation |
| SQLite | Local database and SQL analysis |
| SQL | Revenue aggregation and reporting |
| VS Code | Development environment |
| SQLite Extension for VS Code | SQL execution |
| Markdown | Documentation |
| CSV | Intermediate and final analytical outputs |

No external AI API or external service is required.

---

# 6. Project Structure

```text
Capstone Project_Messo Reseller
│
├── Part1_SQL
│   ├── main.py
│   ├── Queries.sql
│   └── output
│
├── Part2_Engine
│   ├── Growth_Engine.py
│   ├── Quick_Check.py
│   ├── Test_Growth_Engine.py
│   └── Part2_Output
│
├── Part3_Narrative
│   ├── Quick_Mask_Check.py
│   ├── Part3_Data_Masking.sql
│   ├── prompt_pack.md
│   ├── narrative_report.md
│   ├── Masked_Orders.csv
│   └── output
│
├── Part4_Agent
│   ├── Agent_Spec.md
│   ├── Mock_Agent_Runner.py
│   ├── Agent_Test_Report.txt
│   ├── Part4_Summary.txt
│   └── Output
│       └── Agent_Narratives.txt
│
├── Final_Project
│   ├── Report
│   ├── Presentation
│   └── Evidence
│
└── meesho.db

# 7. How to Regenerate the Dataset

The dataset can be regenerated using:

Part1_SQL\main.py

Open the VS Code terminal and run:

cd Part1_SQL
python main.py

The generator uses a fixed random seed to ensure reproducible results.

The generated data is then used for the SQLite-based analysis.

8. How to Run the Complete Pipeline

The project should be executed in the following order.

Part 1 — Dataset Generation and SQL Analysis
Step 1 — Generate the dataset

From the project terminal:

cd Part1_SQL
python main.py
Step 2 — Run SQL analysis

Open:

Part1_SQL\Queries.sql

Use the SQLite extension in VS Code to execute the SQL queries against:

meesho.db

The SQL analysis produces CSV reports in:

Part1_SQL\output\

Important outputs include:

Monthly_Category_Revenue.csv
Region_Wise_Revenue_Order_Count.csv
Top_5_Resellers_By_Spend.csv
Zero_Order_Resellers.csv
June_AOV_Delivered_Only.csv
Part 2 — Growth Engine

The Growth Engine reads the verified order data and calculates Month-on-Month revenue growth.

Main file:

Part2_Engine\Growth_Engine.py

Run:

cd Part2_Engine
python Growth_Engine.py

The Growth Engine:

Reads the SQLite revenue data.
Calculates monthly revenue.
Calculates MoM growth.
Applies the growth rule.
Validates the generated feed.
Saves the results.

The primary output is:

Part2_Engine\Part2_Output\Monthly_MoM_Growth.csv

The project also generates category-level MoM analysis and flagging outputs.

Growth Flagging Rule

The project uses an 8% threshold.

MoM Growth > 8%
        ↓
Flagged
MoM Growth = 8%
        ↓
Escalate Exact Boundary
MoM Growth < 8%
        ↓
Not Flagged

Negative growth is therefore not automatically classified as a flagged condition under this rule.

Part 3 — Reliable AI Narrative and Data Masking

Part 3 focuses on communicating verified numbers safely and protecting reseller identifiers.

Main execution file:

Part3_Narrative\Quick_Mask_Check.py

Run:

cd Part3_Narrative
python Quick_Mask_Check.py

The script executes the data-masking SQL and performs validation.

The SQL file is:

Part3_Narrative\Part3_Data_Masking.sql

The masked data is produced as:

Part3_Narrative\output\Masked_Orders.csv
Narrative Structure

The narrative follows three sections:

Context

What happened according to the verified numbers?

Insight

What does the numerical change show?

Implication

What should management consider investigating?

The narrative must not invent causes, trends, or unsupported business explanations.

Part 4 — Reliable Revenue Analysis Agent

Part 4 implements a local/mock revenue analysis agent.

Main file:

Part4_Agent\Mock_Agent_Runner.py

Run:

cd Part4_Agent
python Mock_Agent_Runner.py

The agent generates:

Part4_Agent\Output\Agent_Narratives.txt

The agent also validates:

Output file existence
Expected May categories
Expected June category
Growth percentages
Input consistency

Successful validation produces:

AGENT RELIABILITY VALIDATION
============================================================
Output file exists: True
May categories verified: True
June category verified: True
Growth percentages verified: True

Agent validation PASSED.
9. How the Parts Connect

The project follows a sequential data pipeline.

Raw Dataset
     │
     ▼
Part 1 — SQL Analysis
     │
     ▼
Verified Revenue Results
     │
     ▼
Part 2 — Growth Engine
     │
     ▼
MoM Growth + Flagging
     │
     ├───────────────┐
     ▼               ▼
Part 3              Part 4
Data Masking        Revenue Agent
+ Narrative         + Validation
     │               │
     └───────┬───────┘
             ▼
     Reliable Business Output
Data Flow

Part 1 provides the verified revenue data.

Part 2 transforms the revenue data into deterministic MoM growth measurements and flags.

Part 3 uses verified information for masked analysis and structured narrative generation.

Part 4 consumes verified analytical results and produces validated business narratives.

10. Zero API Key Requirement

The complete project works without external API keys.

No:

OpenAI API key
Grok API key
Gemini API key
Cloud database
External AI service

is required to execute the project.

The project uses local:

Python
SQLite
Pandas
SQL
Deterministic business rules
Mock/local agent processing

This makes the project reproducible in a local development environment.

11. Workflow Pattern Mapping

Each project part demonstrates a different analytics/AI workflow pattern.

Part	Workflow Pattern	Implementation
Part 1	Data Retrieval & Aggregation	SQL queries against SQLite
Part 2	Deterministic Transformation & Rule-Based Decision	MoM calculations and threshold flagging
Part 3	Structured Prompting & Guardrailed Narrative Generation	Context → Insight → Implication
Part 3	Data Privacy	Reseller identifier masking
Part 4	Agentic Processing	Revenue analysis agent
Part 4	Validation	Output and data verification
Part 4	Safe Failure Handling	Stops when required input is missing
12. Key Verified Findings

The Growth Engine produced the following category-level results.

May 2026 — Flagged Categories
Category	May MoM Growth
Beauty & Personal Care	+13.64%
Ethnic Wear	+17.00%
Western Wear	+9.63%
June 2026 — Flagged Categories
Category	June MoM Growth
Ethnic Wear	+35.48%

The project deliberately distinguishes between:

verified numerical movement
rule-based flags
possible management investigations

It does not automatically treat a revenue change as evidence of a specific business cause.

13. Reliability and Validation

Reliability checks are included throughout the pipeline.

Data Validation

The project checks:

Duplicate order IDs
Required fields
Revenue values
Growth calculations
Required CSV columns
Growth Engine Validation

The Growth Engine validates:

File existence
Required columns
Non-empty data
Numeric revenue values
Valid MoM growth values
Agent Validation

The Part 4 agent validates:

Output file existence
Expected categories
Growth percentages
Period consistency
Negative Test

The project also tests safe failure by temporarily removing the required Growth Engine input file.

The agent correctly stopped with:

ERROR: Required Growth Engine output file is missing.
Agent execution stopped safely.

This demonstrates that the agent does not continue processing when a required input is unavailable.

14. Data Privacy and Masking

Part 3 masks reseller identifiers before downstream analysis.

For example:

Original Reseller ID
        ↓
Masked Reseller ID
        ↓
Reseller_001
Reseller_002
Reseller_003
...

The original reseller identity is not included in the masked analytical output.

The mapping between original and masked identifiers is maintained separately.

Important Note

Identifier masking is a privacy protection measure, but it is not the same as complete anonymization.

15. Limitations

The project has several limitations:

The dataset is simulated rather than production business data.
The analysis covers only April–June 2026.
The agent is a local/mock implementation.
No external AI API is integrated.
Revenue movements are not automatically attributed to business causes.
The reseller masking mapping remains available within the local project environment.
The dataset does not represent real Meesho operational performance.
16. Future Enhancements

Possible future improvements include:

Integration with a production database
Automated scheduled data refresh
Interactive dashboards
Additional business KPIs
Return and cancellation analysis
Reseller performance analysis
Inventory analysis
External LLM integration with strict validation
Role-based access control
Automated report distribution
Monitoring and alerting
More advanced anomaly detection
17. Conclusion

This project demonstrates a complete and reproducible revenue analytics workflow.

The pipeline progresses from:

Dataset Generation
        ↓
SQL Analysis
        ↓
Growth Calculation
        ↓
Rule-Based Flagging
        ↓
Data Masking
        ↓
Structured Narrative
        ↓
Validated Revenue Agent

The primary design principle is:

Communicate verified numbers safely.

The project combines traditional data analytics with reliable AI-style workflow patterns while maintaining validation, traceability, privacy controls, and safe failure handling.

Most importantly, the complete pipeline can be executed locally without external API keys.