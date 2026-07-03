import streamlit as st
import pandas as pd

from utils.load_data import load_data
from utils.sidebar import sidebar_filters
from utils.helper import format_number
from utils.charts import *

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Recommendation Center",

    page_icon="🧠",

    layout="wide"

)

# ==========================================================
# LOAD DATA
# ==========================================================

df = load_data()

df = sidebar_filters(df)

# ==========================================================
# HERO
# ==========================================================

st.markdown("""

<div class="hero">

<h1>🧠 AI Recommendation Center</h1>

<p style="font-size:18px;">

Analyze priority levels, management areas,
and AI-generated recommendations for
better agricultural decision making.

</p>

</div>

""", unsafe_allow_html=True)

st.write("")

# ==========================================================
# KPI VALUES
# ==========================================================

records = len(df)

recommendations = df["Recommendation"].nunique()

states = df["State"].nunique()

critical = (

    df["Priority"] == "Immediate Action Required"

).sum()

high = (

    df["Priority"] == "High Priority"

).sum()

moderate = (

    df["Priority"] == "Moderate Priority"

).sum()

routine = (

    df["Priority"] == "Routine Monitoring"

).sum()

# ==========================================================
# KPI ROW
# ==========================================================

c1,c2,c3,c4 = st.columns(4)

with c1:

    st.metric(

        "📄 Records",

        format_number(records)

    )

with c2:

    st.metric(

        "🏛 States",

        states

    )

with c3:

    st.metric(

        "🧠 Recommendation Types",

        recommendations

    )

with c4:

    st.metric(

        "🚨 Critical Cases",

        critical

    )

c1,c2,c3 = st.columns(3)

with c1:

    st.metric(

        "🔴 High Priority",

        high

    )

with c2:

    st.metric(

        "🟡 Moderate",

        moderate

    )

with c3:

    st.metric(

        "🟢 Routine",

        routine

    )

st.divider()

# ==========================================================
# OVERVIEW
# ==========================================================

left, right = st.columns([2,1])

with left:

    st.subheader("📘 Recommendation Overview")

    st.info(f"""

Recommendation Engine Status

➡ **Active**

Machine Learning Model

➡ **Random Forest Regressor**

Recommendation Categories

➡ **{recommendations}**

States Covered

➡ **{states}**

Total Records

➡ **{records:,}**

""")

with right:

    st.subheader("⚡ Executive Summary")

    st.success(f"""

Immediate Action Required

➡ **{critical}**

High Priority

➡ **{high}**

Moderate Priority

➡ **{moderate}**

Routine Monitoring

➡ **{routine}**

""")

st.divider()

# ==========================================================
# PRIORITY SUMMARY
# ==========================================================

st.header("🚨 Priority Overview")

priority = (

    df["Priority"]

    .value_counts()

    .reset_index()

)

priority.columns = [

    "Priority",

    "Count"

]

fig = create_donut_chart(

    priority,

    names="Priority",

    values="Count",

    title="Priority Distribution"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# ==========================================================
# RECOMMENDATION SUMMARY
# ==========================================================

st.header("🧠 Recommendation Distribution")

recommendation = (

    df["Recommendation"]

    .value_counts()

    .head(10)

    .reset_index()

)

recommendation.columns = [

    "Recommendation",

    "Count"

]

fig = create_horizontal_bar(

    recommendation,

    x="Count",

    y="Recommendation",

    color="Count",

    title="Top 10 AI Recommendations"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# ==========================================================
# PRIORITY SNAPSHOT
# ==========================================================

st.header("📊 Recommendation Snapshot")

a,b,c,d = st.columns(4)

a.metric(

    "Critical",

    critical

)

b.metric(

    "High",

    high

)

c.metric(

    "Moderate",

    moderate

)

d.metric(

    "Routine",

    routine

)

st.divider()


# ==========================================================
# STATES & CROPS REQUIRING ATTENTION
# ==========================================================

st.header("🌾 High Attention Areas")

left, right = st.columns(2)

with left:

    state_attention = (

        df[df["Priority"].isin([

            "Immediate Action Required",

            "High Priority"

        ])]

        .groupby("State", as_index=False)

        .size()

        .rename(columns={"size":"Cases"})

        .sort_values(

            "Cases",

            ascending=False

        )

        .head(10)

    )

    fig = create_horizontal_bar(

        state_attention,

        x="Cases",

        y="State",

        color="Cases",

        title="Top States Requiring Attention"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    crop_attention = (

        df[df["Priority"].isin([

            "Immediate Action Required",

            "High Priority"

        ])]

        .groupby("Crop", as_index=False)

        .size()

        .rename(columns={"size":"Cases"})

        .sort_values(

            "Cases",

            ascending=False

        )

        .head(10)

    )

    fig = create_bar_chart(

        crop_attention,

        x="Crop",

        y="Cases",

        color="Cases",

        title="Top Crops Requiring Attention"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

st.divider()

# ==========================================================
# MANAGEMENT AREA
# ==========================================================

st.header("📊 Management Area Analysis")

management = (

    df["Management_Area"]

    .value_counts()

    .reset_index()

)

management.columns = [

    "Management Area",

    "Count"

]

fig = create_horizontal_bar(

    management,

    x="Count",

    y="Management Area",

    color="Count",

    title="Management Area Distribution"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# ==========================================================
# PRIORITY BY STATE
# ==========================================================

st.header("📈 Priority by State")

priority_state = (

    df.groupby(

        ["State","Priority"]

    )

    .size()

    .reset_index(name="Count")

)

fig = create_grouped_bar(

    priority_state,

    x="State",

    y="Count",

    color="Priority",

    title="Priority Distribution Across States"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# ==========================================================
# CRITICAL RECORDS
# ==========================================================

st.header("🚨 Critical Cases")

critical_df = df[

    df["Priority"] == "Immediate Action Required"

][

    [

        "State",

        "District",

        "Crop",

        "Yield",

        "Predicted_Yield",

        "Recommendation"

    ]

]

st.dataframe(

    critical_df,

    use_container_width=True,

    height=350,

    hide_index=True

)

st.divider()

# ==========================================================
# RECOMMENDATION FREQUENCY
# ==========================================================

st.header("🧠 Recommendation Frequency")

recommendation_freq = (

    df.groupby(

        "Recommendation",

        as_index=False

    )

    .size()

    .rename(columns={"size":"Frequency"})

    .sort_values(

        "Frequency",

        ascending=False

    )

    .head(15)

)

fig = create_horizontal_bar(

    recommendation_freq,

    x="Frequency",

    y="Recommendation",

    color="Frequency",

    title="Most Frequent Recommendations"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# ==========================================================
# EXECUTIVE SNAPSHOT
# ==========================================================

st.header("📌 Executive Snapshot")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(

        "High Attention States",

        state_attention["State"].nunique()

    )

with col2:

    st.metric(

        "Critical Records",

        len(critical_df)

    )

with col3:

    st.metric(

        "Recommendation Types",

        df["Recommendation"].nunique()

    )

st.divider()

# ==========================================================
# AI ADVISORY PANEL
# ==========================================================

st.header("💡 AI Advisory Panel")

high_attention_states = (
    df[df["Priority"].isin([
        "Immediate Action Required",
        "High Priority"
    ])]["State"].nunique()
)

high_attention_crops = (
    df[df["Priority"].isin([
        "Immediate Action Required",
        "High Priority"
    ])]["Crop"].nunique()
)

top_recommendation = (
    df["Recommendation"]
    .mode()[0]
)

left, right = st.columns(2)

with left:

    st.success(f"""

### 🌾 Key Recommendations

• States requiring attention: **{high_attention_states}**

• Crops requiring attention: **{high_attention_crops}**

• Most frequent recommendation:

**{top_recommendation}**

""")

with right:

    st.info(f"""

### 🤖 AI Decision Summary

✔ Recommendation Engine : Active

✔ Priority Classification : Completed

✔ Machine Learning Analysis : Completed

✔ Dataset Status : Validated

""")

st.divider()

# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

st.header("📊 Executive Business Insights")

top_state = (
    df.groupby("State")["Production"]
    .sum()
    .idxmax()
)

top_crop = (
    df.groupby("Crop")["Production"]
    .sum()
    .idxmax()
)

best_prediction = (
    df.groupby("Crop")["Predicted_Yield"]
    .mean()
    .idxmax()
)

c1, c2, c3 = st.columns(3)

c1.metric(

    "🏛 Best Production State",

    top_state

)

c2.metric(

    "🌾 Best Crop",

    top_crop

)

c3.metric(

    "🤖 Best Predicted Crop",

    best_prediction

)

st.divider()

# ==========================================================
# DATASET
# ==========================================================

st.header("📋 Recommendation Dataset")

recommendation_dataset = df[

    [

        "State",

        "District",

        "Crop",

        "Priority",

        "Recommendation",

        "Management_Area",

        "Yield",

        "Predicted_Yield"

    ]

]

st.dataframe(

    recommendation_dataset,

    use_container_width=True,

    height=500,

    hide_index=True

)

st.divider()


# ==========================================================
# SEARCH
# ==========================================================

st.header("🔍 Search Recommendations")

keyword = st.text_input(

    "Search Recommendation"

)

if keyword:

    result = recommendation_dataset[

        recommendation_dataset["Recommendation"]

        .str.contains(

            keyword,

            case=False,

            na=False

        )

    ]

    st.dataframe(

        result,

        use_container_width=True,

        hide_index=True

    )

st.divider()


# ==========================================================
# DOWNLOAD REPORT
# ==========================================================

st.download_button(

    "⬇ Download Recommendation Report",

    recommendation_dataset.to_csv(

        index=False

    ),

    file_name="Recommendation_Report.csv",

    mime="text/csv"

)

# ==========================================================
# FINAL SUMMARY
# ==========================================================

st.success("""

## ✅ Recommendation Analysis Completed

The AI Recommendation Engine analyzed the agricultural dataset
and identified priority levels, management areas, and actionable
recommendations to support informed agricultural decision-making.

""")
