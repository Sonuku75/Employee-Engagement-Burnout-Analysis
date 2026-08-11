# Import required libraries

import streamlit as st
import pandas as pd
import plotly.express as px


# Configure page

st.set_page_config(
    page_title="Burnout Risk",
    page_icon="🔥",
    layout="wide"
)


# Custom CSS

st.markdown("""
<style>

.main-title {
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 16px;
    color: #8b949e;
    margin-bottom: 25px;
}

.section-title {
    font-size: 24px;
    font-weight: 650;
    margin-top: 15px;
    margin-bottom: 15px;
}

.kpi-card {
    padding: 20px;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,0.25);
    background: rgba(128,128,128,0.05);
    min-height: 125px;
}

.kpi-label {
    font-size: 14px;
    color: #8b949e;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 30px;
    font-weight: 700;
}

.risk-box {
    padding: 20px;
    border-radius: 14px;
    border: 1px solid rgba(255, 100, 100, 0.35);
    background: rgba(255, 100, 100, 0.08);
}

</style>
""", unsafe_allow_html=True)


# Load dataset

DATA_PATH = "data/processed/dashboard_dataset.csv"

df = pd.read_csv(DATA_PATH)


# Page Header

st.markdown(
    '<div class="main-title">🔥 Burnout Risk Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Identify burnout-prone employee groups using overtime, '
    'work-life balance, workload, travel, and engagement indicators.'
    '</div>',
    unsafe_allow_html=True
)


st.divider()


# Sidebar filters

st.sidebar.markdown("## 🔎 Burnout Filters")


departments = sorted(df["Department"].unique())

selected_departments = st.sidebar.multiselect(
    "Department",
    departments,
    default=departments
)


roles = sorted(df["JobRole"].unique())

selected_roles = st.sidebar.multiselect(
    "Job Role",
    roles,
    default=roles
)


selected_overtime = st.sidebar.radio(
    "Overtime",
    ["All", "Yes", "No"],
    horizontal=True
)


worklife_range = st.sidebar.slider(
    "Work-Life Balance",
    min_value=1,
    max_value=4,
    value=(1, 4)
)


# Apply filters

filtered_df = df[
    (df["Department"].isin(selected_departments))
    &
    (df["JobRole"].isin(selected_roles))
    &
    (df["WorkLifeBalance"].between(
        worklife_range[0],
        worklife_range[1]
    ))
]


if selected_overtime != "All":

    filtered_df = filtered_df[
        filtered_df["OverTime"] == selected_overtime
    ]


# Empty check

if filtered_df.empty:

    st.warning(
        "No employees match the selected filters."
    )

    st.stop()


# KPI calculations

total_employees = len(filtered_df)

high_risk_count = (
    filtered_df["Burnout_Risk_Level"] == "High"
).sum()

high_risk_percentage = (
    high_risk_count / total_employees * 100
)

average_burnout_score = (
    filtered_df["Burnout_Risk_Score"].mean()
)

average_worklife = (
    filtered_df["WorkLifeBalance"].mean()
)


# KPI cards

st.markdown(
    '<div class="section-title">Burnout Risk Snapshot</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4)


with k1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">HIGH RISK EMPLOYEES</div>
            <div class="kpi-value">{high_risk_count:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">HIGH RISK RATE</div>
            <div class="kpi-value">{high_risk_percentage:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">AVG BURNOUT SCORE</div>
            <div class="kpi-value">{average_burnout_score:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">WORK-LIFE BALANCE</div>
            <div class="kpi-value">{average_worklife:.2f} / 4</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# Risk distribution

st.markdown(
    '<div class="section-title">Burnout Risk Distribution</div>',
    unsafe_allow_html=True
)

risk_counts = (
    filtered_df["Burnout_Risk_Level"]
    .value_counts()
    .reset_index()
)

risk_counts.columns = [
    "Risk Level",
    "Employees"
]

fig_risk = px.pie(
    risk_counts,
    names="Risk Level",
    values="Employees",
    hole=0.45,
    title="Employee Burnout Risk Distribution"
)

fig_risk.update_layout(
    height=420,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)


# Overtime and Work-Life Balance

st.markdown(
    '<div class="section-title">Workload & Burnout Drivers</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


with col1:

    overtime_burnout = pd.crosstab(
        filtered_df["OverTime"],
        filtered_df["Burnout_Risk_Level"]
    ).reset_index()

    overtime_burnout_long = overtime_burnout.melt(
        id_vars="OverTime",
        var_name="Risk Level",
        value_name="Employees"
    )

    fig_overtime = px.bar(
        overtime_burnout_long,
        x="OverTime",
        y="Employees",
        color="Risk Level",
        barmode="group",
        title="Overtime vs Burnout Risk"
    )

    fig_overtime.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_overtime,
        use_container_width=True
    )


with col2:

    wlb_burnout = pd.crosstab(
        filtered_df["WorkLifeBalance"],
        filtered_df["Burnout_Risk_Level"]
    ).reset_index()

    wlb_burnout_long = wlb_burnout.melt(
        id_vars="WorkLifeBalance",
        var_name="Risk Level",
        value_name="Employees"
    )

    fig_wlb = px.bar(
        wlb_burnout_long,
        x="WorkLifeBalance",
        y="Employees",
        color="Risk Level",
        barmode="group",
        title="Work-Life Balance vs Burnout Risk"
    )

    fig_wlb.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_wlb,
        use_container_width=True
    )


# Department analysis

st.markdown(
    '<div class="section-title">High-Risk Employee Segments</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


with col1:

    department_high_risk = (
        filtered_df[
            filtered_df["Burnout_Risk_Level"] == "High"
        ]
        .groupby("Department")
        .size()
        .reset_index(name="High Risk Employees")
        .sort_values(
            "High Risk Employees",
            ascending=False
        )
    )

    fig_department = px.bar(
        department_high_risk,
        x="Department",
        y="High Risk Employees",
        title="High Burnout Risk by Department"
    )

    fig_department.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_department,
        use_container_width=True
    )


with col2:

    role_high_risk = (
        filtered_df[
            filtered_df["Burnout_Risk_Level"] == "High"
        ]
        .groupby("JobRole")
        .size()
        .reset_index(name="High Risk Employees")
        .sort_values(
            "High Risk Employees",
            ascending=False
        )
    )

    fig_role = px.bar(
        role_high_risk,
        x="High Risk Employees",
        y="JobRole",
        orientation="h",
        title="High Burnout Risk by Job Role"
    )

    fig_role.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_role,
        use_container_width=True
    )


# Travel analysis

st.markdown(
    '<div class="section-title">Travel & Burnout</div>',
    unsafe_allow_html=True
)

travel_burnout = (
    filtered_df
    .groupby("BusinessTravel")
    .agg(
        Burnout_Score=("Burnout_Risk_Score", "mean"),
        Engagement=("Engagement_Index", "mean")
    )
    .reset_index()
)

fig_travel = px.bar(
    travel_burnout,
    x="BusinessTravel",
    y="Burnout_Score",
    title="Average Burnout Risk Score by Business Travel"
)

fig_travel.update_layout(
    height=380,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig_travel,
    use_container_width=True
)


# Burnout vs Engagement

st.markdown(
    '<div class="section-title">Burnout & Engagement Relationship</div>',
    unsafe_allow_html=True
)

burnout_engagement = (
    filtered_df
    .groupby("Burnout_Risk_Level")
    .agg(
        Engagement_Index=("Engagement_Index", "mean"),
        Employees=("Engagement_Index", "count")
    )
    .reset_index()
)

fig_relationship = px.bar(
    burnout_engagement,
    x="Burnout_Risk_Level",
    y="Engagement_Index",
    text_auto=".2f",
    title="Average Engagement by Burnout Risk Level"
)

fig_relationship.update_layout(
    height=380,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig_relationship,
    use_container_width=True
)


# Priority intervention employees

priority_employees = filtered_df[
    (filtered_df["Burnout_Risk_Level"] == "High")
    &
    (filtered_df["Engagement_Category"] == "Low")
]


st.markdown(
    '<div class="section-title">🚨 Priority Intervention Area</div>',
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <div class="risk-box">
        <strong>{len(priority_employees):,}</strong>
        employees show both <strong>High Burnout Risk</strong>
        and <strong>Low Engagement</strong>.
        These employees represent the highest-priority group
        for preventive HR intervention.
    </div>
    """,
    unsafe_allow_html=True
)


# Priority employee table

if not priority_employees.empty:

    display_columns = [
        "Age",
        "Department",
        "JobRole",
        "OverTime",
        "WorkLifeBalance",
        "Engagement_Index",
        "Burnout_Risk_Score",
        "BusinessTravel",
        "DistanceFromHome",
        "YearsAtCompany",
        "Attrition"
    ]

    st.dataframe(
        priority_employees[
            display_columns
        ],
        use_container_width=True,
        hide_index=True
    )