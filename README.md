# production-planning-capacity-utilization (Operations Analytics)
operations analytics project analyzing production capacity utilization, bottlenecks, downtime, and shift productivity using SQL and python

## Project Overview
This project simulates a **real world manufacturing operations dataset** and applies SQL based analytics to answer **core plant level decision questions** around capacity utilization, bottlenecks, and shift productivity.

The goal is not visualization first, but **decision oriented operations analysis** , the kind used by Plant Heads, Operations Managers and other teams.

The dataset and analysis are inspired by **large integrated manufacturing environments** (textiles / FMCG / heavy manufacturing).

---

## Business Questions Answered

This project answers the following **operations critical questions**:

1. Are we fully utilizing the capacity we already have?
2. Which production lines are true bottlenecks limiting throughput?
3. How does productivity vary across shifts?
4. Where is time being lost due to downtime?
5. Which shifts are most expensive per unit produced?

---

## Dataset Design (Realistic & Operations Grade)

**Granularity:**  
Line × Shift × Day × Product

**Time Period:**  
6 months (Jan–Jun 2024)

### Tables Used
| Table Name | Description |
|-----------|-------------|
| plants | Manufacturing plant master |
| production_lines | Physical production lines with rated capacity |
| shifts | Shift definitions with labor cost |
| products | Product master with standard minutes |
| production_calendar | Plant level working calendar |
| orders | Demand inputs (priority, customer type) |
| production_runs | Core fact table (actual execution) |
| maintenance_logs | Downtime & maintenance events |

All KPIs are **derived**, not stored, mirroring real analytics best practices.

---

## Data Modeling
- `production_runs` acts as the **central fact table**
- Strong use of **primary & foreign keys**
- Referential integrity enforced between plants, lines, shifts, and products
- Composite key used where business grain demands it (calendar)

---

## Analysis Performed (SQL)

### Step 1: Capacity Utilization Analysis
- Utilization by plant, line, shift, and month
- Identification of under-utilized assets
- Sanity checks to validate physical feasibility

**Key Metric:**
Capacity Utilization % = Actual Units / (Rated Capacity × Run Hours)

---

### Step 2: Bottleneck & Downtime Analysis
- Downtime contribution by line
- Downtime as % of available production time
- Planned vs breakdown maintenance analysis
- Quantification of **lost production due to downtime**

This step identifies **true constraints**, not just low performing areas.

---

### Step 3: Shift Productivity & Labor Efficiency
- Units produced per hour by shift
- Capacity utilization by shift
- Labor cost per unit by shift
- Planned vs actual achievement by shift

This translates operations performance directly into **cost and people decisions**.

---

## Key Insights
- Certain lines consistently show high downtime and low utilization → bottlenecks
- Night shift shows lower productivity and higher labor cost per unit
- Reducing downtime yields higher ROI than adding new capacity
- Capacity issues are execution-driven, not demand-driven

---

## 🛠 Tools & Technologies
- **SQL Server** – core analytics
- **Python (pandas, numpy)** – realistic data generation
- **Excel / Power BI** – visualization layer

---
