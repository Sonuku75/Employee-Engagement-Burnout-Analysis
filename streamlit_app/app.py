# Import required libraries

import streamlit as st
import pandas as pd


# Configure Streamlit page

st.set_page_config(
    page_title="Employee Engagement & Burnout Analytics",
    page_icon="📊",
    layout="wide"
)


# Load dashboard dataset

DATA_PATH = "data/processed/dashboard_dataset.csv"

df = pd.read_csv(DATA_PATH)


# Dashboard title

st.title("Employee Engagement & Burnout Analytics")

st.write(
    "Interactive dashboard for analyzing employee engagement, "
    "satisfaction, burnout risk, workload, and career-stage indicators."
)


# Calculate KPIs

total_employees = len(df)

engagement_index = df["Engagement_Index"].mean()

burnout_rate = (
    (df["Burnout_Risk_Level"] == "High").mean() * 100
)

worklife_balance = df["WorkLifeBalance"].mean()

satisfaction_stability = (
    df["Satisfaction_Stability_Score"].mean()
)


# Display KPI cards

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Employees",
    total_employees
)

col2.metric(
    "Engagement Index",
    f"{engagement_index:.2f}"
)

col3.metric(
    "High Burnout Risk",
    f"{burnout_rate:.1f}%"
)

col4.metric(
    "Work-Life Balance",
    f"{worklife_balance:.2f}"
)

col5.metric(
    "Satisfaction Stability",
    f"{satisfaction_stability:.1f}%"
)


# Dashboard overview

st.divider()

st.subheader("Dashboard Overview")

st.write(
    "Use the navigation menu to explore employee engagement, "
    "burnout risk, career-stage trends, and manager intervention areas."
)