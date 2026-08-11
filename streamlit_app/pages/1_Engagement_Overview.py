# Import required libraries

import streamlit as st
import pandas as pd
import plotly.express as px


# Configure page

st.set_page_config(
    page_title="Engagement Overview",
    page_icon="📊",
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

.alert-box {
    padding: 18px;
    border-radius: 12px;
    border: 1px solid rgba(255, 165, 0, 0.35);
    background: rgba(255, 165, 0, 0.08);
}

</style>
""", unsafe_allow_html=True)


# Load dataset

DATA_PATH = "data/processed/dashboard_dataset.csv"

df = pd.read_csv(DATA_PATH)


# Page Header

st.markdown(
    '<div class="main-title">📊 Engagement Health Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Monitor employee engagement, satisfaction, work-life balance, '
    'and retention indicators across the organization.'
    '</div>',
    unsafe_allow_html=True
)


# Sidebar Filters

st.sidebar.markdown("## 🔎 Dashboard Filters")

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

engagement_threshold = st.sidebar.slider(
    "Engagement Threshold",
    min_value=1.0,
    max_value=4.0,
    value=2.5,
    step=0.1
)

min_tenure = int(df["YearsAtCompany"].min())
max_tenure = int(df["YearsAtCompany"].max())

selected_tenure = st.sidebar.slider(
    "Years at Company",
    min_value=min_tenure,
    max_value=max_tenure,
    value=(min_tenure, max_tenure)
)


# Apply Filters

filtered_df = df[
    (df["Department"].isin(selected_departments))
    &
    (df["JobRole"].isin(selected_roles))
    &
    (df["YearsAtCompany"].between(
        selected_tenure[0],
        selected_tenure[1]
    ))
]

if selected_overtime != "All":

    filtered_df = filtered_df[
        filtered_df["OverTime"] == selected_overtime
    ]


# Empty Filter Check

if filtered_df.empty:

    st.warning(
        "No employees match the selected filters."
    )

    st.stop()


# KPI Calculations

total_employees = len(filtered_df)

average_engagement = filtered_df[
    "Engagement_Index"
].mean()

high_engagement_percentage = (
    filtered_df["Engagement_Index"]
    .ge(engagement_threshold)
    .mean()
    * 100
)

average_worklife = filtered_df[
    "WorkLifeBalance"
].mean()

average_satisfaction = filtered_df[
    "JobSatisfaction"
].mean()


# KPI Section

st.markdown(
    '<div class="section-title">Organization Snapshot</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">TOTAL EMPLOYEES</div>
            <div class="kpi-value">{total_employees:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">ENGAGEMENT INDEX</div>
            <div class="kpi-value">{average_engagement:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">ABOVE THRESHOLD</div>
            <div class="kpi-value">{high_engagement_percentage:.1f}%</div>
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


# Engagement Distribution + Satisfaction

st.markdown(
    '<div class="section-title">Engagement & Satisfaction</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# Engagement Distribution

with col1:

    fig_engagement = px.histogram(
        filtered_df,
        x="Engagement_Index",
        nbins=12,
        title="Engagement Index Distribution",
        labels={
            "Engagement_Index": "Engagement Index"
        }
    )

    fig_engagement.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_engagement,
        use_container_width=True
    )


# Satisfaction Distribution

with col2:

    satisfaction_data = filtered_df[
        [
            "JobSatisfaction",
            "EnvironmentSatisfaction",
            "RelationshipSatisfaction",
            "WorkLifeBalance"
        ]
    ].melt(
        var_name="Dimension",
        value_name="Rating"
    )

    satisfaction_data["Dimension"] = (
        satisfaction_data["Dimension"]
        .str.replace(
            "Satisfaction",
            "",
            regex=False
        )
        .str.replace(
            "WorkLifeBalance",
            "Work-Life Balance",
            regex=False
        )
    )

    fig_satisfaction = px.box(
        satisfaction_data,
        x="Dimension",
        y="Rating",
        title="Satisfaction Dimensions",
        points=False
    )

    fig_satisfaction.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_satisfaction,
        use_container_width=True
    )


# Department & Engagement Category

st.markdown(
    '<div class="section-title">Engagement Segmentation</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# Department Engagement

with col1:

    department_engagement = (
        filtered_df
        .groupby("Department")["Engagement_Index"]
        .mean()
        .reset_index()
        .sort_values(
            "Engagement_Index",
            ascending=False
        )
    )

    fig_department = px.bar(
        department_engagement,
        x="Department",
        y="Engagement_Index",
        title="Average Engagement by Department",
        text_auto=".2f"
    )

    fig_department.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_department,
        use_container_width=True
    )


# Engagement Categories

with col2:

    category_counts = (
        filtered_df[
            "Engagement_Category"
        ]
        .value_counts()
        .reset_index()
    )

    category_counts.columns = [
        "Engagement Category",
        "Employees"
    ]

    fig_category = px.pie(
        category_counts,
        names="Engagement Category",
        values="Employees",
        hole=0.45,
        title="Engagement Category Distribution"
    )

    fig_category.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# Job Role Analysis

st.markdown(
    '<div class="section-title">Job Role Analysis</div>',
    unsafe_allow_html=True
)

role_engagement = (
    filtered_df
    .groupby("JobRole")["Engagement_Index"]
    .mean()
    .reset_index()
    .sort_values(
        "Engagement_Index",
        ascending=True
    )
)

fig_role = px.bar(
    role_engagement,
    x="Engagement_Index",
    y="JobRole",
    orientation="h",
    title="Average Engagement by Job Role",
    text_auto=".2f"
)

fig_role.update_layout(
    height=500,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig_role,
    use_container_width=True
)


# Attrition Comparison

st.markdown(
    '<div class="section-title">Engagement & Attrition</div>',
    unsafe_allow_html=True
)

attrition_engagement = (
    filtered_df
    .groupby("Attrition")["Engagement_Index"]
    .mean()
    .reset_index()
)

fig_attrition = px.bar(
    attrition_engagement,
    x="Attrition",
    y="Engagement_Index",
    title="Average Engagement by Attrition Status",
    text_auto=".2f"
)

fig_attrition.update_layout(
    height=350,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig_attrition,
    use_container_width=True
)


# Low Engagement Section

low_engagement = filtered_df[
    filtered_df["Engagement_Index"]
    < engagement_threshold
]

st.markdown(
    '<div class="section-title">⚠️ Low Engagement Alert</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="alert-box">
        <strong>{len(low_engagement):,}</strong>
        employees are currently below the selected engagement
        threshold of <strong>{engagement_threshold:.1f}</strong>.
    </div>
    """,
    unsafe_allow_html=True
)


# Employee Table

if not low_engagement.empty:

    display_columns = [
        "Age",
        "Department",
        "JobRole",
        "JobLevel",
        "Engagement_Index",
        "Engagement_Category",
        "JobSatisfaction",
        "EnvironmentSatisfaction",
        "RelationshipSatisfaction",
        "WorkLifeBalance",
        "OverTime",
        "YearsAtCompany"
    ]

    st.dataframe(
        low_engagement[
            display_columns
        ]
        .sort_values(
            "Engagement_Index"
        ),
        use_container_width=True,
        hide_index=True
    )