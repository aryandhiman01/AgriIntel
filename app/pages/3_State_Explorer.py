import streamlit as st
import pandas as pd

from utils.load_data import load_data
from utils.sidebar import sidebar_filters

from utils.helper import (
    format_number,
    format_yield
)

from utils.charts import *


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="State Explorer",

    page_icon="🏛",

    layout="wide"

)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

df = sidebar_filters(df)

# =====================================================
# HERO
# =====================================================

st.markdown("""

<div class="hero">

<h1>🏛 State Explorer</h1>

<p style="font-size:18px">

Explore state level agricultural performance,
crop distribution, weather intelligence,
soil health and machine learning insights.

</p>

</div>

""",

unsafe_allow_html=True)

st.write("")

# =====================================================
# STATE
# =====================================================

state = st.selectbox(

    "Select State",

    sorted(

        df["State"].unique()

    )

)

state_df = df[

    df["State"] == state

]

# =====================================================
# KPIs
# =====================================================

records = len(state_df)

districts = state_df["District"].nunique()

crops = state_df["Crop"].nunique()

production = state_df["Production"].sum()

yield_avg = state_df["Yield"].mean()

prediction = state_df["Predicted_Yield"].mean()

priority = state_df["Priority"].mode()[0]

c1,c2,c3,c4 = st.columns(4)

c1.metric(

    "📄 Records",

    format_number(records)

)

c2.metric(

    "🏙 Districts",

    districts

)

c3.metric(

    "🌾 Crops",

    crops

)

c4.metric(

    "🚨 Priority",

    priority

)

c1,c2,c3 = st.columns(3)

c1.metric(

    "🌱 Production",

    format_number(

        production

    )

)

c2.metric(

    "📈 Avg Yield",

    format_yield(

        yield_avg

    )

)

c3.metric(

    "🤖 Predicted Yield",

    format_yield(

        prediction

    )

)

st.divider()

left,right = st.columns([2,1])

with left:

    st.subheader("📘 State Overview")

    st.info(

f"""

State

➡ **{state}**

Districts

➡ **{districts}**

Available Crops

➡ **{crops}**

Machine Learning

➡ Enabled

Recommendation Engine

➡ Active

"""

)

with right:

    st.subheader("⚡ Quick Summary")

    st.success(

f"""

Highest Priority

➡ **{priority}**

Production

➡ **{production:,.0f}**

Average Yield

➡ **{yield_avg:.2f}**

"""

)

st.divider()

st.subheader("🌦 Weather Summary")

a,b,c = st.columns(3)

a.metric(

    "Temperature",

    f"{state_df['avg_temp_c'].mean():.2f} °C"

)

b.metric(

    "Rainfall",

    f"{state_df['total_rainfall_mm'].mean():.2f} mm"

)

c.metric(

    "Humidity",

    f"{state_df['avg_humidity_percent'].mean():.2f}%"

)

st.divider()

st.subheader("🌱 Soil Summary")

a,b,c,d = st.columns(4)

a.metric(

    "Nitrogen",

    f"{state_df['N'].mean():.2f}"

)

b.metric(

    "Phosphorus",

    f"{state_df['P'].mean():.2f}"

)

c.metric(

    "Potassium",

    f"{state_df['K'].mean():.2f}"

)

d.metric(

    "pH",

    f"{state_df['pH'].mean():.2f}"

)

st.divider()

# ==========================================================
# TOP CROPS & DISTRICTS
# ==========================================================

st.header("🌾 Crop Performance")

left, right = st.columns(2)

with left:

    crop_summary = (

        state_df

        .groupby("Crop", as_index=False)

        .agg({

            "Production":"sum"

        })

        .sort_values(

            "Production",

            ascending=False

        )

        .head(10)

    )

    fig = create_horizontal_bar(

        crop_summary,

        x="Production",

        y="Crop",

        color="Production",

        title="Top Producing Crops"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    district_summary = (

        state_df

        .groupby("District", as_index=False)

        .agg({

            "Production":"sum"

        })

        .sort_values(

            "Production",

            ascending=False

        )

        .head(10)

    )

    fig = create_bar_chart(

        district_summary,

        x="District",

        y="Production",

        color="Production",

        title="Top Producing Districts"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

st.divider()

# ==========================================================
# SEASON ANALYSIS
# ==========================================================

st.header("📅 Season Analysis")

left, right = st.columns(2)

with left:

    season = (

        state_df

        .groupby("Season", as_index=False)

        .agg({

            "Production":"sum"

        })

    )

    fig = create_donut_chart(

        season,

        names="Season",

        values="Production",

        title="Production by Season"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    season_yield = (

        state_df

        .groupby("Season", as_index=False)

        .agg({

            "Yield":"mean"

        })

    )

    fig = create_bar_chart(

        season_yield,

        x="Season",

        y="Yield",

        color="Yield",

        title="Average Yield by Season"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

st.divider()

# ==========================================================
# WEATHER ANALYSIS
# ==========================================================

st.header("🌦 Weather Impact")

left, right = st.columns(2)

with left:

    fig = create_scatter_chart(

        state_df,

        x="avg_temp_c",

        y="Yield",

        color="Priority",

        title="Temperature vs Yield"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    fig = create_scatter_chart(

        state_df,

        x="total_rainfall_mm",

        y="Yield",

        color="Priority",

        title="Rainfall vs Yield"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

st.divider()

# ==========================================================
# SOIL ANALYSIS
# ==========================================================

st.header("🌱 Soil Analysis")

soil = state_df[
    [
        "N",
        "P",
        "K",
        "pH"
    ]
].mean()

soil = soil.reset_index()

soil.columns = [

    "Parameter",

    "Average"

]

fig = create_bar_chart(

    soil,

    x="Parameter",

    y="Average",

    color="Average",

    title="Average Soil Parameters"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# ==========================================================
# YEARLY TREND
# ==========================================================

st.header("📈 Production & Yield Trend")

trend = (

    state_df

    .groupby("Start_Year", as_index=False)

    .agg({

        "Production":"sum",

        "Yield":"mean"

    })

)

left, right = st.columns(2)

with left:

    fig = create_line_chart(

        trend,

        x="Start_Year",

        y="Production",

        title="Production Trend"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    fig = create_line_chart(

        trend,

        x="Start_Year",

        y="Yield",

        title="Yield Trend"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

st.divider()

# ==========================================================
# MACHINE LEARNING SUMMARY
# ==========================================================

st.header("🤖 Machine Learning Prediction Summary")

left, right = st.columns([2,1])

prediction = (

    state_df[
        [
            "District",
            "Crop",
            "Yield",
            "Predicted_Yield",
            "Prediction_Error",
            "Yield_Prediction_Category"
        ]
    ]

    .sort_values(

        "Predicted_Yield",

        ascending=False

    )

)

with left:

    st.dataframe(

        prediction,

        use_container_width=True,

        height=350,

        hide_index=True

    )

with right:

    st.metric(

        "Average Actual Yield",

        f"{state_df['Yield'].mean():.2f}"

    )

    st.metric(

        "Average Predicted Yield",

        f"{state_df['Predicted_Yield'].mean():.2f}"

    )

    st.metric(

        "Average Prediction Error",

        f"{state_df['Prediction_Error'].mean():.2f}"

    )

st.divider()

# ==========================================================
# RECOMMENDATION ENGINE
# ==========================================================

st.header("🧠 Recommendation Analytics")

left, right = st.columns(2)

with left:

    recommendation = (

        state_df["Recommendation"]

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

        title="Top Recommendations"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    priority = (

        state_df["Priority"]

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
# BUSINESS INSIGHTS
# ==========================================================

st.header("💡 Business Insights")

top_crop = (

    state_df

    .groupby("Crop")["Production"]

    .sum()

    .idxmax()

)

top_district = (

    state_df

    .groupby("District")["Production"]

    .sum()

    .idxmax()

)

highest_yield = (

    state_df["Yield"]

    .max()

)

highest_prediction = (

    state_df["Predicted_Yield"]

    .max()

)

left, right = st.columns(2)

with left:

    st.success(

f"""

### 🏆 Best Performing Region

Top Crop

➡ **{top_crop}**

Top District

➡ **{top_district}**

Highest Yield

➡ **{highest_yield:.2f}**

"""

    )

with right:

    st.info(

f"""

### 🤖 ML Summary

Highest Predicted Yield

➡ **{highest_prediction:.2f}**

Prediction Engine

➡ Active

Recommendation Engine

➡ Active

"""

    )

st.divider()

# ==========================================================
# DATASET
# ==========================================================

st.header("📋 State Dataset")

st.dataframe(

    state_df,

    use_container_width=True,

    height=450,

    hide_index=True

)

st.divider()

# ==========================================================
# DOWNLOAD REPORT
# ==========================================================

st.download_button(

    "⬇ Download State Report",

    state_df.to_csv(

        index=False

    ),

    file_name=f"{state}_Report.csv",

    mime="text/csv"

)