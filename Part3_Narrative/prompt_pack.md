# Prompt Pack: Four Required Sections
# 1. Trigger

# The prompt runs only when a category's is_flagged result is exactly "flagged".

if flag == "flagged":
    # Generate AI narrative for this category
    pass

# 2.Input list

Placeholder	             |  Description
{category}               |  Name of the product category
{previous_revenue}       |  Revenue in the previous month
{current_revenue}        |  Revenue in the current month
{mom_pct}                |  Verified Month-on-Month growth percentage
{month}                  |  Current month
{prev_month}             |  Previous month

All revenue and growth values must come from the validated Python Growth Engine output, not be invented or estimated by the AI.

 # 3.Prompt — Context → Insight → Implication
  Reliable AI Narrative Prompt

**Role:** You are a business reporting assistant for a Meesho Reseller analytics project.

**Context:** Analyze the following verified category-wise revenue data:

* Category: {category}
* Previous Month: {prev_month}
* Previous Month Revenue: AED {previous_revenue}
* Current Month: {month}
* Current Month Revenue: AED {current_revenue}
* Verified MoM Growth: {mom_pct}%

The category has been flagged by the Python Growth Engine because its MoM growth exceeds the configured 8% threshold.

**Insight:**

Explain the observed revenue movement between {prev_month} and {month} using only the supplied figures.

Clearly state:

* Whether revenue increased or decreased.
* The absolute revenue difference, calculated from the supplied revenue values.
* The verified MoM growth percentage.

Do not invent causes, customer behavior, market trends, or business events. Do not claim that the growth is sustainable or that it will continue.

**Implication:**

Provide one practical, neutral business consideration for the management team based on the observed revenue movement.

Clearly distinguish verified facts from suggested actions. If the supplied data is insufficient to explain why the change occurred, explicitly state that further investigation is required.

**Output format:**

1. Context: Briefly summarize the category and reporting period.
2. Insight: Explain the verified revenue movement and percentage.
3. Implication: Provide one practical next step for management.

Use concise, professional business English. Do not introduce any figures that are not supported by the supplied data or transparent calculations.

# 4. Checklist — Output Validation

Use this checklist to review every AI-generated narrative before including it in the final report.

Narrative validation checklist:

* The prompt was triggered only when is_flagged = 'flagged'.
* The category and both reporting months match the validated input data.
* The previous and current revenue figures match the Python output exactly.
* The stated MoM percentage matches the verified Growth Engine result.
* The absolute revenue difference is mathematically correct.
* The narrative does not invent causes, market trends, or unsupported numbers.
* The implication is clearly presented as a suggestion, not a verified fact.


* The Prompt Structure: Context → Insight → Implication

The purpose is to turn verified revenue figures from your Python Growth Engine into a clear, factual, and useful business narrative.

1. Context — What happened?

Provide the verified category, reporting months, previous revenue, current revenue, and MoM growth percentage.

Verified inputs

2. Insight — What do the numbers show?

Explain whether revenue increased or decreased, calculate the absolute revenue change, and state the supplied MoM percentage.

Evidence-based analysis

3. Implication — What should management consider?

Suggest a practical next step based on the observed revenue movement, without claiming unsupported causes or future outcomes.

Illustrative example (Using our Mesho  Reseller Data)

The following numbers are taken from the data  "Category_Wise_MoM_Growth.csv", for explaining the structure only.

Example category: Ethnic Wear | April to May 2026

Input	                       |    Illustrative value
Previous revenue (April)       |    AED 421858.43
Current revenue (May)          |    AED 493572.34
MoM growth                     |    17.0%
Revenue difference             |    AED 71713.91

* Context : 
Ethnic Wear revenue increased from AED 421858.43 in April to AED 493572.34 in May 2026.
* Insight : 
Revenue increased by AED 71713.91, representing a verified illustrative MoM growth of 17%.
* Implication : 
Management could review order volumes, product availability, and sales performance to understand the factors associated with the increase and assess whether inventory adjustments are appropriate.