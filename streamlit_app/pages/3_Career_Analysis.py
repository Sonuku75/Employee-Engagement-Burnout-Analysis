# Import required libraries

import streamlit as st
import pandas as pd
import plotly.express as px


# Configure page

st.set_page_config(
    page_title="Career Analysis",
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


# Page header

st.markdown(
    '<div class="main-title">🎯 Role & Career Stage Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Explore engagement across job levels, roles, tenure, '
    'current-role duration, and promotion history.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# Sidebar filters

st.sidebar.markdown("## 🔎 Career Filters")


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


job_levels = sorted(df["JobLevel"].unique())

selected_levels = st.sidebar.multiselect(
    "Job Level",
    job_levels,
    default=job_levels
)


# Apply filters

filtered_df = df[
    (df["Department"].isin(selected_departments))
    &
    (df["JobRole"].isin(selected_roles))
    &
    (df["JobLevel"].isin(selected_levels))
]


# Empty check

if filtered_df.empty:

    st.warning(
        "No employees match the selected filters."
    )

    st.stop()


# KPI calculations

average_engagement = (
    filtered_df["Engagement_Index"].mean()
)

average_tenure = (
    filtered_df["YearsAtCompany"].mean()
)

average_current_role = (
    filtered_df["YearsInCurrentRole"].mean()
)

average_promotion_gap = (
    filtered_df["YearsSinceLastPromotion"].mean()
)


# KPI section

st.markdown(
    '<div class="section-title">Career Health Snapshot</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4)


with k1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">AVERAGE ENGAGEMENT</div>
            <div class="kpi-value">{average_engagement:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">AVERAGE TENURE</div>
            <div class="kpi-value">{average_tenure:.1f} yrs</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">CURRENT ROLE TENURE</div>
            <div class="kpi-value">{average_current_role:.1f} yrs</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">PROMOTION GAP</div>
            <div class="kpi-value">{average_promotion_gap:.1f} yrs</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# Engagement by job level

st.markdown(
    '<div class="section-title">Engagement by Career Level</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


with col1:

    level_engagement = (
        filtered_df
        .groupby("JobLevel")["Engagement_Index"]
        .mean()
        .reset_index()
        .sort_values("JobLevel")
    )

    fig_level = px.bar(
        level_engagement,
        x="JobLevel",
        y="Engagement_Index",
        title="Average Engagement by Job Level",
        text_auto=".2f"
    )

    fig_level.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_level,
        use_container_width=True
    )


# Job role engagement

with col2:

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
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_role,
        use_container_width=True
    )


# Tenure analysis

st.markdown(
    '<div class="section-title">Tenure & Engagement</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


with col1:

    fig_tenure = px.scatter(
    filtered_df,
    x="YearsAtCompany",
    y="Engagement_Index",
    opacity=0.55,
    title="Years at Company vs Engagement"
)

    fig_tenure.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_tenure,
        use_container_width=True
    )


with col2:

    # Plot current role tenure vs engagement

    fig_role_tenure = px.scatter(
    filtered_df,
    x="YearsInCurrentRole",
    y="Engagement_Index",
    opacity=0.55,
    title="Current Role Tenure vs Engagement"
)

    fig_role_tenure.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_role_tenure,
        use_container_width=True
    )


# Promotion analysis

st.markdown(
    '<div class="section-title">Promotion & Career Progression</div>',
    unsafe_allow_html=True
)

fig_promotion = px.scatter(
    filtered_df,
    x="YearsSinceLastPromotion",
    y="Engagement_Index",
    color="JobLevel",
    opacity=0.6,
    title="Years Since Last Promotion vs Engagement"
)

fig_promotion.update_layout(
    height=430,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig_promotion,
    use_container_width=True
)


# Career stage classification

st.markdown(
    '<div class="section-title">Career Stage Distribution</div>',
    unsafe_allow_html=True
)


def career_stage(years):

    if years <= 2:
        return "Early Career"

    elif years <= 7:
        return "Developing"

    elif years <= 15:
        return "Established"

    else:
        return "Experienced"


career_df = filtered_df.copy()

career_df["Career_Stage"] = (
    career_df["YearsAtCompany"]
    .apply(career_stage)
)


career_stage_counts = (
    career_df["Career_Stage"]
    .value_counts()
    .reset_index()
)

career_stage_counts.columns = [
    "Career Stage",
    "Employees"
]


fig_career = px.pie(
    career_stage_counts,
    names="Career Stage",
    values="Employees",
    hole=0.45,
    title="Employee Career Stage Distribution"
)

fig_career.update_layout(
    height=420,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig_career,
    use_container_width=True
)


# Stagnation analysis

st.markdown(
    '<div class="section-title">⚠️ Potential Career Stagnation</div>',
    unsafe_allow_html=True
)


stagnation_df = filtered_df[
    (filtered_df["YearsInCurrentRole"] >= 5)
    &
    (filtered_df["YearsSinceLastPromotion"] >= 4)
    &
    (filtered_df["Engagement_Index"] < 2.5)
]


st.markdown(
    f"""
    <div class="alert-box">
        <strong>{len(stagnation_df):,}</strong>
        employees show potential career stagnation signals
        based on extended role tenure, longer promotion gaps,
        and below-average engagement.
    </div>
    """,
    unsafe_allow_html=True
)


# Stagnation employee table

if not stagnation_df.empty:

    display_columns = [
        "Age",
        "Department",
        "JobRole",
        "JobLevel",
        "YearsAtCompany",
        "YearsInCurrentRole",
        "YearsSinceLastPromotion",
        "Engagement_Index",
        "Engagement_Category",
        "JobSatisfaction",
        "Attrition"
    ]

    st.dataframe(
        stagnation_df[
            display_columns
        ].sort_values(
            "Engagement_Index"
        ),
        use_container_width=True,
        hide_index=True
    )