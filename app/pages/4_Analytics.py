import streamlit as st

from utils.load_data import load_data
from utils.sidebar import sidebar_filters
from utils.helper import (
    format_number,
    format_yield
)

from utils.charts import (
    create_histogram,
    create_bar_chart,
    create_scatter_chart,
    create_donut_chart,
    create_horizontal_bar,
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Analytics",

    page_icon="📊",

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

<h1>📊 Analytics Dashboard</h1>

<p style="font-size:18px">

Explore weather, soil, yield and production
analytics through interactive visualizations.

</p>

</div>

""",

unsafe_allow_html=True)

st.write("")

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

records = len(df)

states = df["State"].nunique()

districts = df["District"].nunique()

crops = df["Crop"].nunique()

production = df["Production"].sum()

yield_avg = df["Yield"].mean()

prediction = df["Predicted_Yield"].mean()

c1,c2,c3,c4 = st.columns(4)

c1.metric(

    "📄 Records",

    format_number(records)

)

c2.metric(

    "🏛 States",

    states

)

c3.metric(

    "🏙 Districts",

    districts

)

c4.metric(

    "🌾 Crops",

    crops

)

c1,c2,c3 = st.columns(3)

c1.metric(

    "🌱 Production",

    format_number(

        production

    )

)

c2.metric(

    "📈 Average Yield",

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

# ==========================================================
# CLIMATE ANALYTICS
# ==========================================================

st.header("🌦 Climate Analytics")

left,right = st.columns(2)

with left:

    fig = create_histogram(

        df,

        x="avg_temp_c",

        title="Temperature Distribution"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    fig = create_histogram(

        df,

        x="total_rainfall_mm",

        title="Rainfall Distribution"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

st.write("")

left,right = st.columns(2)

with left:

    fig = create_histogram(

        df,

        x="avg_humidity_percent",

        title="Humidity Distribution"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    weather = (

        df.groupby(

            "State",

            as_index=False

        )

        .agg({

            "avg_temp_c":"mean"

        })

        .sort_values(

            "avg_temp_c",

            ascending=False

        )

        .head(10)

    )

    fig = create_bar_chart(

        weather,

        x="State",

        y="avg_temp_c",

        color="avg_temp_c",

        title="Top 10 Warmest States"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

st.divider()

# ==========================================================
# CLIMATE INSIGHTS
# ==========================================================

st.header("💡 Climate Insights")

highest_temp = (

    df.groupby("State")["avg_temp_c"]

    .mean()

    .idxmax()

)

highest_rain = (

    df.groupby("State")["total_rainfall_mm"]

    .mean()

    .idxmax()

)

highest_humidity = (

    df.groupby("State")["avg_humidity_percent"]

    .mean()

    .idxmax()

)

left,right = st.columns(2)

with left:

    st.success(f"""

### 🌡 Temperature

Highest Average Temperature

➡ **{highest_temp}**

### 🌧 Rainfall

Highest Average Rainfall

➡ **{highest_rain}**

""")

with right:

    st.info(f"""

### 💧 Humidity

Highest Average Humidity

➡ **{highest_humidity}**

Weather Analytics

➡ **Completed**

""")

st.divider()

# ==========================================================
# SOIL ANALYTICS
# ==========================================================

st.header("🌱 Soil Analytics")

soil_avg = (
    df[["N", "P", "K", "pH"]]
    .mean()
    .reset_index()
)

soil_avg.columns = [
    "Parameter",
    "Average"
]

fig = create_bar_chart(
    soil_avg,
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
# YIELD ANALYTICS
# ==========================================================

st.header("🌾 Yield Analytics")

left, right = st.columns(2)

with left:

    fig = create_histogram(
        df,
        x="Yield",
        title="Actual Yield Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = create_histogram(
        df,
        x="Predicted_Yield",
        title="Predicted Yield Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ==========================================================
# ACTUAL VS PREDICTED
# ==========================================================

st.header("🤖 Actual vs Predicted Yield")

fig = create_scatter_chart(

    df,

    x="Yield",

    y="Predicted_Yield",

    color="Priority",

    title="Actual Yield vs Predicted Yield"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# ==========================================================
# PREDICTION ERROR
# ==========================================================

st.header("📉 Prediction Error Analysis")

fig = create_histogram(

    df,

    x="Prediction_Error",

    title="Prediction Error Distribution"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# ==========================================================
# PREDICTION CATEGORY
# ==========================================================

st.header("🎯 Prediction Categories")

prediction_category = (

    df["Yield_Prediction_Category"]

    .value_counts()

    .reset_index()

)

prediction_category.columns = [

    "Category",

    "Count"

]

fig = create_donut_chart(

    prediction_category,

    names="Category",

    values="Count",

    title="Yield Prediction Categories"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# ==========================================================
# YIELD SUMMARY
# ==========================================================

st.header("📈 Yield Statistics")

c1, c2, c3, c4 = st.columns(4)

c1.metric(

    "Minimum Yield",

    f"{df['Yield'].min():.2f}"

)

c2.metric(

    "Maximum Yield",

    f"{df['Yield'].max():.2f}"

)

c3.metric(

    "Average Yield",

    f"{df['Yield'].mean():.2f}"

)

c4.metric(

    "Average Prediction Error",

    f"{df['Prediction_Error'].mean():.2f}"

)

st.divider()

# ==========================================================
# MACHINE LEARNING INSIGHTS
# ==========================================================

st.header("💡 Machine Learning Insights")

highest_prediction = df.loc[
    df["Predicted_Yield"].idxmax()
]

lowest_prediction = df.loc[
    df["Predicted_Yield"].idxmin()
]

left, right = st.columns(2)

with left:

    st.success(f"""

### 🌾 Highest Predicted Yield

State : **{highest_prediction['State']}**

Crop : **{highest_prediction['Crop']}**

Predicted Yield : **{highest_prediction['Predicted_Yield']:.2f}**

""")

with right:

    st.warning(f"""

### 📉 Lowest Predicted Yield

State : **{lowest_prediction['State']}**

Crop : **{lowest_prediction['Crop']}**

Predicted Yield : **{lowest_prediction['Predicted_Yield']:.2f}**

""")

st.divider()

# ==========================================================
# PRIORITY ANALYTICS
# ==========================================================

st.header("🚨 Priority Analytics")

left, right = st.columns(2)

with left:

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

with right:

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
# RECOMMENDATION ANALYTICS
# ==========================================================

st.header("🧠 Recommendation Analytics")

recommendation = (

    df["Recommendation"]

    .value_counts()

    .head(15)

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

    title="Top Recommended Actions"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# ==========================================================
# EXECUTIVE INSIGHTS
# ==========================================================

st.header("💡 Executive Business Insights")

highest_production_state = (

    df.groupby("State")["Production"]

    .sum()

    .idxmax()

)

highest_yield_crop = (

    df.groupby("Crop")["Yield"]

    .mean()

    .idxmax()

)

highest_prediction_crop = (

    df.groupby("Crop")["Predicted_Yield"]

    .mean()

    .idxmax()

)

left, right = st.columns(2)

with left:

    st.success(f"""

### 🌾 Agriculture Highlights

🏛 Highest Production State

**{highest_production_state}**

🌾 Highest Yield Crop

**{highest_yield_crop}**

🤖 Best Predicted Crop

**{highest_prediction_crop}**

""")

with right:

    st.info(f"""

### 📊 Dashboard Summary

Records Analysed

**{len(df):,}**

States Covered

**{df['State'].nunique()}**

Machine Learning

**Random Forest**

Recommendation Engine

**Active**

""")

st.divider()

# ==========================================================
# ANALYTICS SNAPSHOT
# ==========================================================

st.header("📈 Analytics Snapshot")

c1, c2, c3, c4 = st.columns(4)

c1.metric(

    "Average Temperature",

    f"{df['avg_temp_c'].mean():.2f} °C"

)

c2.metric(

    "Average Rainfall",

    f"{df['total_rainfall_mm'].mean():.2f} mm"

)

c3.metric(

    "Average Humidity",

    f"{df['avg_humidity_percent'].mean():.2f}%"

)

c4.metric(

    "Average Soil pH",

    f"{df['pH'].mean():.2f}"

)

st.divider()

# ==========================================================
# DATASET PREVIEW
# ==========================================================

st.header("📋 Analytics Dataset Preview")

preview = df[

    [

        "State",

        "District",

        "Crop",

        "Yield",

        "Predicted_Yield",

        "Prediction_Error",

        "Priority",

        "Management_Area"

    ]

]

st.dataframe(

    preview,

    use_container_width=True,

    height=450,

    hide_index=True

)

st.divider()

# ==========================================================
# EXPORT ANALYTICS
# ==========================================================

st.download_button(

    "⬇ Download Analytics Dataset",

    df.to_csv(index=False),

    "Analytics_Report.csv",

    "text/csv"

)