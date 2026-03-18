# Credit Risk & Expected Credit Loss (ECL) Analytics System

## What this project is about

This project simulates the work of a credit risk analyst at a bank or lending company. Using real loan data from Lending Club (2007–2018), we analyze a portfolio of 2 million+ loans to estimate how much money the lender is expected to lose — and which segments of the portfolio carry the most risk.

The entire workflow mirrors what financial institutions actually do to comply with credit risk frameworks like IFRS 9 and Basel III.

---

## Regulatory framework

This project is built on the principles of two current global banking standards:

### IFRS 9 — International Financial Reporting Standard 9
IFRS 9 is the current global accounting standard for financial instruments, in effect since **January 2018**. It replaced the older IAS 39 standard. One of its core requirements is that banks must calculate and report **Expected Credit Loss (ECL)** on all loan portfolios — which is exactly what this project does.

IFRS 9 defines a three-stage impairment model:

| Stage | Loan condition | ECL measured over |
|---|---|---|
| Stage 1 | Performing normally, no significant risk increase | Next 12 months |
| Stage 2 | Significant increase in credit risk since origination | Lifetime of the loan |
| Stage 3 | Credit-impaired or in default | Lifetime of the loan |

This project implements the **core ECL formula (PD × LGD × EAD)** at portfolio level, which is the foundation of the IFRS 9 framework. A full production implementation would additionally classify every loan into one of the three stages and apply stage-specific ECL calculations.

### Basel III
Basel III is the current global regulatory framework for banks, developed by the Basel Committee on Banking Supervision. It governs how much capital banks must hold against credit risk. The risk segmentation, stress testing, and scenario analysis in this project reflect Basel III thinking — specifically the requirement that banks understand and quantify the risk in their loan portfolios and demonstrate resilience under adverse economic conditions.

### Note on Indian context
In India, the **Reserve Bank of India (RBI)** has aligned its prudential norms with IFRS 9 and Basel III principles. Indian banks are required to maintain capital adequacy ratios and provision for expected credit losses in line with these frameworks.

*This project does not claim to be a fully production-grade IFRS 9 system. It implements the core ECL methodology as a portfolio analytics project, demonstrating the concepts and calculations that underpin the standard.*

---

## The core concept

Every calculation in this project is built on three numbers:

- **PD — Probability of Default**: What is the likelihood that a borrower will not repay their loan?
- **LGD — Loss Given Default**: If a borrower defaults, what fraction of the outstanding amount is unrecoverable?
- **EAD — Exposure at Default**: How much money is outstanding at the time of default?

These three combine into the central formula:

**ECL = PD × LGD × EAD**

ECL (Expected Credit Loss) is the dollar/rupee amount the lender expects to lose on a loan or across the entire portfolio.

---

## Dataset

**Source**: Lending Club Loan Data (Kaggle)
**File used**: `accepted_2007_to_2018Q4.csv`
**Size**: ~1.6 GB, 2.2 million loans, 150+ columns
**Key columns used**: `loan_status`, `loan_amnt`, `funded_amnt`, `int_rate`, `grade`, `sub_grade`, `annual_inc`, `dti`, `issue_d`, `recoveries`, `total_pymnt`, `out_prncp`

---

## Project phases

### Phase 1 — Data setup
Load the dataset into Python using pandas, select only the relevant columns to manage memory, clean missing values, fix data types, and store the processed data in a SQLite database for SQL analysis.

### Phase 2 — SQL: PD, LGD, EAD calculation
Use SQL queries to calculate:
- PD by loan grade (historical default rates per grade)
- LGD using recovery data (1 − recovery rate)
- EAD from outstanding principal at time of default

### Phase 3 — Python: ECL computation
Apply ECL = PD × LGD × EAD at the individual loan level using pandas. Aggregate to portfolio level to get total expected loss. Produce a clean summary table by loan grade.

### Phase 4 — Risk segmentation & vintage analysis
- Segment the portfolio by loan grade (A through G) to identify which grades carry the most risk
- Perform vintage analysis: group loans by issue year (cohort) and track default rates over time to see which origination years performed best and worst

### Phase 5 — Stress testing
Simulate adverse economic scenarios by increasing default rates (e.g. +25%, +50%, +100%). Measure the impact on total ECL to understand portfolio resilience under stress conditions similar to a recession.

### Phase 6 — Dashboard & reporting
Build interactive dashboards in Tableau or Power BI to visualize:
- Portfolio ECL breakdown by grade
- PD, LGD, EAD KPIs
- Vintage performance heatmap
- Stress scenario comparison

---

## Tools & technologies

| Tool | Purpose |
|---|---|
| Python (pandas, numpy) | Data loading, cleaning, ECL calculation |
| SQL (SQLite) | Risk metric queries and aggregation |
| Matplotlib / Seaborn | Exploratory charts and analysis visuals |
| Tableau / Power BI | Final dashboards for stakeholder reporting |
| VS Code + Jupyter | Development environment |

---

## Skills demonstrated

- Large dataset handling (1.6 GB CSV)
- Credit risk modeling (PD, LGD, EAD, ECL)
- SQL-based financial analysis
- Cohort and vintage analysis
- Stress testing and scenario simulation
- Business dashboard design
- Applied knowledge of IFRS 9 and Basel III frameworks

---

## Project structure

```
credit_risk/
│
├── data/
│   └── accepted_2007_to_2018Q4.csv        # Raw Lending Club dataset
│
├── notebooks/
│   ├── 01_data_loading.ipynb              # Phase 1 — Load and clean data
│   ├── 02_sql_pd_lgd_ead.ipynb            # Phase 2 — SQL risk metrics
│   ├── 03_ecl_calculation.ipynb           # Phase 3 — ECL computation
│   ├── 04_segmentation_vintage.ipynb      # Phase 4 — Risk segmentation
│   ├── 05_stress_testing.ipynb            # Phase 5 — Stress scenarios
│   └── 06_dashboard_prep.ipynb            # Phase 6 — Dashboard data export
│
├── outputs/
│   ├── ecl_by_grade.csv                   # ECL summary by loan grade
│   ├── vintage_analysis.csv               # Vintage cohort default rates
│   └── stress_scenarios.csv              # Stress test results
│
└── README.md

```

---

*Built using real-world Lending Club data as a portfolio project in credit risk analytics, applying IFRS 9 and Basel III principles.*

---

That's your complete README. Once you've pasted it, also go ahead and create the folder structure shown at the bottom — `data/`, `notebooks/`, `outputs/` — inside your project folder in VS Code. Then we're ready to write Phase 1 code.