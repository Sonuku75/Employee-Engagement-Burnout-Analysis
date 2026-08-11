# Employee Engagement, Satisfaction, and Burnout Diagnostic Analysis

## Project Overview

This project analyzes employee engagement, satisfaction, workload, work-life balance, and burnout risk to identify early warning signals that may affect employee experience and retention.

The analysis focuses on preventive HR diagnostics rather than only analyzing attrition after employees leave.

---

## Problem Statement

Organizations need early visibility into declining employee engagement, burnout-prone groups, workload pressure, and work-life imbalance.

This project provides a data-driven approach to identify:

- Low employee engagement
- Burnout-prone employee groups
- Overtime and workload stress
- Work-life balance issues
- Career-stage disengagement
- Potential intervention areas

---

## Objectives

- Build a unified Employee Engagement Index
- Identify employees with potential burnout risk
- Analyze overtime and work-life balance
- Study engagement across departments and job roles
- Analyze career-stage engagement
- Identify potential career stagnation
- Compare engagement with attrition
- Build an interactive Streamlit dashboard
- Provide actionable insights for HR and managers

---

## Dataset

The dataset contains employee-level information related to demographics, job characteristics, satisfaction, workload, career progression, and attrition.

### Major Dataset Categories

- Employee demographics
- Department and job role
- Job level
- Job satisfaction
- Environment satisfaction
- Relationship satisfaction
- Job involvement
- Work-life balance
- Overtime
- Business travel
- Career tenure
- Promotion history
- Attrition

---

## Analytical Methodology

### 1. Data Understanding

The dataset was inspected for:

- Shape and structure
- Data types
- Missing values
- Duplicate records
- Unique values
- Ordinal scales

### 2. Data Cleaning

The dataset was validated and cleaned to ensure consistency and reliability for further analysis.

### 3. Exploratory Data Analysis

EDA was performed to analyze:

- Employee demographics
- Satisfaction patterns
- Overtime
- Business travel
- Work-life balance
- Attrition
- Department and role differences
- Career-stage patterns

### 4. Engagement Index

The Engagement Index combines:

- Job Involvement
- Job Satisfaction
- Environment Satisfaction
- Relationship Satisfaction

The resulting score ranges from 1 to 4.

### 5. Burnout Risk

Burnout risk is assessed using:

- Overtime
- Work-life balance

Employees are classified into:

- Low Risk
- Medium Risk
- High Risk

### 6. KPI Analysis

The project calculates:

- Engagement Index
- Burnout Risk Score
- Work-Life Balance Index
- Satisfaction Stability Score
- Workload Stress Indicator

---

## Dashboard

The project includes an interactive Streamlit dashboard with four major modules.

### Engagement Health Overview

Provides:

- Engagement KPIs
- Satisfaction analysis
- Department-wise engagement
- Job-role engagement
- Engagement vs attrition
- Low-engagement employee identification

### Burnout Risk Dashboard

Provides:

- Burnout risk distribution
- Overtime analysis
- Work-life balance analysis
- Department-wise burnout risk
- Job-role burnout analysis
- Travel and burnout analysis
- High-risk employee identification

### Role & Career Stage Analysis

Provides:

- Engagement by job level
- Engagement by job role
- Tenure analysis
- Current-role tenure analysis
- Promotion gap analysis
- Career-stage distribution
- Potential career stagnation identification

### Manager Action Panel

Provides:

- Priority employee identification
- High burnout risk groups
- Low engagement groups
- Overtime groups
- Department-level intervention areas
- Job-role intervention areas
- Manager recommendations

---

## Dashboard Filters

Users can interact with the dashboard using:

- Department filter
- Job role filter
- Overtime filter
- Burnout risk filter
- Engagement threshold slider
- Work-life balance filter
- Job level filter
- Tenure range selector

---

## Key Performance Indicators

| KPI | Description |
|---|---|
| Engagement Index | Composite measure of employee engagement |
| Burnout Risk Score | Overtime and work-life balance based risk score |
| Work-Life Balance Index | Average work-life balance rating |
| Satisfaction Stability Score | Consistency across satisfaction dimensions |
| Workload Stress Indicator | Composite travel and overtime workload indicator |

---

## Project Structure

```text
Employee-Engagement-Burnout-Analysis/
│
├── data/
│   ├── raw/
│   │   └── Palo Alto Networks.csv
│   │
│   └── processed/
│       ├── employee_engagement_dataset.csv
│       └── dashboard_dataset.csv
│
├── notebooks/
│   ├── 01_Data_Understanding.ipynb
│   ├── 02_Data_Cleaning.ipynb
│   ├── 03_Exploratory_Data_Analysis.ipynb
│   ├── 04_Engagement_Index.ipynb
│   ├── 05_Burnout_Risk.ipynb
│   ├── 06_KPI_Analysis.ipynb
│   └── 07_Streamlit_Data.ipynb
│
├── src/
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   ├── kpi_analysis.py
│   ├── visualization.py
│   └── utils.py
│
├── streamlit_app/
│   ├── app.py
│   │
│   └── pages/
│       ├── 1_Engagement_Overview.py
│       ├── 2_Burnout_Risk.py
│       ├── 3_Career_Analysis.py
│       └── 4_Manager_Action.py
│
├── reports/
│   ├── Research_Paper.docx
│   └── Executive_Summary.docx
│
├── requirements.txt
├── README.md
└── LICENSE