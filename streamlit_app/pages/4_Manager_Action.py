# Import required libraries

import streamlit as st
import pandas as pd
import plotly.express as px


# Configure page

st.set_page_config(
    page_title="Manager Action Panel",
    page_icon="🎯",
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

.action-card {
    padding: 20px;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,0.25);
    background: rgba(128,128,128,0.05);
    min-height: 160px;
}

</style>
""", unsafe_allow_html=True)


# Load dataset

DATA_PATH = "data/processed/dashboard_dataset.csv"

df = pd.read_csv(DATA_PATH)


# Page header

st.markdown(
    '<div class="main-title">🎯 Manager Action Panel</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Identify priority employee groups and translate engagement and '
    'burnout signals into preventive HR intervention areas.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# Sidebar filters

st.sidebar.markdown("## 🔎 Action Filters")


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


risk_levels = [
    "All",
    "High",
    "Medium",
    "Low"
]

selected_risk = st.sidebar.selectbox(
    "Burnout Risk Level",
    risk_levels
)


engagement_threshold = st.sidebar.slider(
    "Engagement Threshold",
    min_value=1.0,
    max_value=4.0,
    value=2.5,
    step=0.1
)


# Apply filters

filtered_df = df[
    (df["Department"].isin(selected_departments))
    &
    (df["JobRole"].isin(selected_roles))
]


if selected_risk != "All":

    filtered_df = filtered_df[
        filtered_df["Burnout_Risk_Level"]
        == selected_risk
    ]


# Empty check

if filtered_df.empty:

    st.warning(
        "No employees match the selected filters."
    )

    st.stop()


# Create intervention groups

priority_df = filtered_df[
    (filtered_df["Burnout_Risk_Level"] == "High")
    &
    (filtered_df["Engagement_Index"] < engagement_threshold)
]


burnout_df = filtered_df[
    filtered_df["Burnout_Risk_Level"] == "High"
]


low_engagement_df = filtered_df[
    filtered_df["Engagement_Index"] < engagement_threshold
]


overtime_df = filtered_df[
    filtered_df["OverTime"] == "Yes"
]


# KPI calculations

priority_count = len(priority_df)

high_risk_count = len(burnout_df)

low_engagement_count = len(low_engagement_df)

overtime_count = len(overtime_df)


# KPI section

st.markdown(
    '<div class="section-title">Manager Action Snapshot</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4)


with k1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">PRIORITY EMPLOYEES</div>
            <div class="kpi-value">{priority_count:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">HIGH BURNOUT RISK</div>
            <div class="kpi-value">{high_risk_count:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">LOW ENGAGEMENT</div>
            <div class="kpi-value">{low_engagement_count:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">OVERTIME EMPLOYEES</div>
            <div class="kpi-value">{overtime_count:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# Action Areas

st.markdown(
    '<div class="section-title">Recommended Intervention Areas</div>',
    unsafe_allow_html=True
)


a1, a2, a3, a4 = st.columns(4)


with a1:

    st.markdown(
        f"""
        <div class="action-card">
            <h3>🔴 Immediate Attention</h3>
            <p>
            {priority_count} employees show both high burnout
            risk and below-threshold engagement.
            </p>
            <b>Action:</b> Schedule individual check-ins
            and review workload conditions.
        </div>
        """,
        unsafe_allow_html=True
    )


with a2:

    st.markdown(
        f"""
        <div class="action-card">
            <h3>🔥 Burnout Intervention</h3>
            <p>
            {high_risk_count} employees are classified
            as high burnout risk.
            </p>
            <b>Action:</b> Review overtime and work-life
            balance conditions.
        </div>
        """,
        unsafe_allow_html=True
    )


with a3:

    st.markdown(
        f"""
        <div class="action-card">
            <h3>📉 Engagement Improvement</h3>
            <p>
            {low_engagement_count} employees fall below
            the selected engagement threshold.
            </p>
            <b>Action:</b> Review satisfaction and
            employee involvement factors.
        </div>
        """,
        unsafe_allow_html=True
    )


with a4:

    st.markdown(
        f"""
        <div class="action-card">
            <h3>⏱️ Workload Review</h3>
            <p>
            {overtime_count} employees currently report
            working overtime.
            </p>
            <b>Action:</b> Review workload distribution
            and overtime patterns.
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# Priority distribution

st.markdown(
    '<div class="section-title">Priority Employee Distribution</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# Department priority

with col1:

    department_priority = (
        priority_df
        .groupby("Department")
        .size()
        .reset_index(
            name="Priority Employees"
        )
        .sort_values(
            "Priority Employees",
            ascending=False
        )
    )

    fig_department = px.bar(
        department_priority,
        x="Department",
        y="Priority Employees",
        title="Priority Employees by Department"
    )

    fig_department.update_layout(
        height=420,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    st.plotly_chart(
        fig_department,
        use_container_width=True
    )


# Role priority

with col2:

    role_priority = (
        priority_df
        .groupby("JobRole")
        .size()
        .reset_index(
            name="Priority Employees"
        )
        .sort_values(
            "Priority Employees",
            ascending=True
        )
    )

    fig_role = px.bar(
        role_priority,
        x="Priority Employees",
        y="JobRole",
        orientation="h",
        title="Priority Employees by Job Role"
    )

    fig_role.update_layout(
        height=420,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    st.plotly_chart(
        fig_role,
        use_container_width=True
    )


# Engagement and burnout relationship

st.markdown(
    '<div class="section-title">Engagement vs Burnout Risk</div>',
    unsafe_allow_html=True
)


risk_engagement = (
    filtered_df
    .groupby("Burnout_Risk_Level")
    .agg(
        Engagement_Index=(
            "Engagement_Index",
            "mean"
        ),
        Employees=(
            "Engagement_Index",
            "count"
        )
    )
    .reset_index()
)


fig_relationship = px.bar(
    risk_engagement,
    x="Burnout_Risk_Level",
    y="Engagement_Index",
    text_auto=".2f",
    title="Average Engagement by Burnout Risk"
)

fig_relationship.update_layout(
    height=400,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)

st.plotly_chart(
    fig_relationship,
    use_container_width=True
)


# Priority employees section

st.markdown(
    '<div class="section-title">🚨 Priority Intervention Employees</div>',
    unsafe_allow_html=True
)


if priority_df.empty:

    st.success(
        "No employees currently meet both the high-risk "
        "and low-engagement priority criteria."
    )

else:

    st.warning(
        f"{len(priority_df):,} employees require priority review."
    )

    display_columns = [
        "Age",
        "Department",
        "JobRole",
        "JobLevel",
        "Engagement_Index",
        "Engagement_Category",
        "Burnout_Risk_Score",
        "Burnout_Risk_Level",
        "OverTime",
        "WorkLifeBalance",
        "BusinessTravel",
        "DistanceFromHome",
        "YearsAtCompany",
        "YearsInCurrentRole",
        "YearsSinceLastPromotion",
        "Attrition"
    ]

    st.dataframe(
        priority_df[
            display_columns
        ]
        .sort_values(
            [
                "Burnout_Risk_Score",
                "Engagement_Index"
            ],
            ascending=[
                False,
                True
            ]
        ),
        use_container_width=True,
        hide_index=True
    )


# Manager recommendations

st.markdown(
    '<div class="section-title">💡 Manager Recommendations</div>',
    unsafe_allow_html=True
)


recommendations = []

if priority_count > 0:

    recommendations.append(
        "Prioritize one-to-one check-ins with employees showing "
        "both high burnout risk and low engagement."
    )

if high_risk_count > 0:

    recommendations.append(
        "Review overtime patterns and workload distribution "
        "for high-risk employee groups."
    )

if low_engagement_count > 0:

    recommendations.append(
        "Investigate job satisfaction, environment satisfaction, "
        "and employee involvement among low-engagement groups."
    )

if overtime_count > 0:

    recommendations.append(
        "Evaluate whether recurring overtime is concentrated "
        "within specific departments or job roles."
    )

if not recommendations:

    recommendations.append(
        "Current filtered employee groups do not show major "
        "intervention signals."
    )


for recommendation in recommendations:

    st.info(
        recommendation
    )