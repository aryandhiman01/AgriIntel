import streamlit as st

from utils.load_data import load_data
from utils.sidebar import sidebar_filters
from utils.helper import format_number, format_yield

from utils.charts import (
    create_bar_chart,
    create_horizontal_bar,
    create_line_chart,
    create_donut_chart
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="AgriIntel",

    page_icon="🌾",

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

<h1>🌾 AgriIntel</h1>

<p style="font-size:20px;">

Agriculture Intelligence & Decision Support Platform

</p>

</div>

""",

unsafe_allow_html=True

)

st.write("")


# ==========================================================
# KPI VALUES
# ==========================================================

records = len(df)

states = df["State"].nunique()

districts = df["District"].nunique()

crops = df["Crop"].nunique()

production = df["Production"].sum()

yield_avg = df["Yield"].mean()

prediction_avg = df["Predicted_Yield"].mean()

recommendations = df["Recommendation"].nunique()


# ==========================================================
# KPI ROW 1
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

        "🏙 Districts",

        districts

    )

with c4:

    st.metric(

        "🌾 Crops",

        crops

    )


# ==========================================================
# KPI ROW 2
# ==========================================================

c1,c2,c3,c4 = st.columns(4)

with c1:

    st.metric(

        "🌱 Production",

        format_number(production)

    )

with c2:

    st.metric(

        "📈 Avg Yield",

        format_yield(yield_avg)

    )

with c3:

    st.metric(

        "🤖 Predicted Yield",

        format_yield(prediction_avg)

    )

with c4:

    st.metric(

        "🧠 Recommendations",

        recommendations

    )


st.divider()


# ==========================================================
# QUICK OVERVIEW
# ==========================================================

left,right = st.columns([2,1])

with left:

    st.subheader("📘 Project Overview")

    st.info(

        """

AgriIntel combines

• Agricultural Production Analytics

• Weather Intelligence

• Soil Intelligence

• Machine Learning Prediction

• Recommendation Engine

• Business Intelligence

into one interactive analytics platform.

"""

    )

with right:

    st.subheader("⚡ Dataset Status")

    st.success(

f"""

✔ Records : {records:,}

✔ States : {states}

✔ Districts : {districts}

✔ Crops : {crops}

✔ Prediction Ready

✔ Recommendation Ready

"""

    )


st.divider()


# ==========================================================
# QUICK STATS
# ==========================================================

st.subheader("📊 Quick Statistics")

a,b,c = st.columns(3)

with a:

    st.metric(

        "Average Temperature",

        f"{df['avg_temp_c'].mean():.2f} °C"

    )

with b:

    st.metric(

        "Average Rainfall",

        f"{df['total_rainfall_mm'].mean():.2f} mm"

    )

with c:

    st.metric(

        "Average Humidity",

        f"{df['avg_humidity_percent'].mean():.2f}%"

    )


st.divider()


# ==========================================================
# DATA PREVIEW
# ==========================================================

st.subheader("🗂 Dataset Preview")

preview = df[

    [

        "State",

        "District",

        "Crop",

        "Season",

        "Production",

        "Yield",

        "Predicted_Yield",

        "Priority"

    ]

].head(15)

st.dataframe(

    preview,

    use_container_width=True,

    hide_index=True

)


st.download_button(

    "⬇ Download Filtered Dataset",

    df.to_csv(index=False),

    "AgriIntel_Filtered.csv",

    "text/csv"

)

# ==========================================================
# ANALYTICS DASHBOARD
# ==========================================================

st.divider()

st.header("📊 Agriculture Analytics")

col1, col2 = st.columns(2)

# ==========================================================
# TOP STATES
# ==========================================================

with col1:

    state_summary = (

        df.groupby("State", as_index=False)

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

        state_summary,

        x="Production",

        y="State",

        color="Production",

        title="Top 10 States by Production"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ==========================================================
# TOP CROPS
# ==========================================================

with col2:

    crop_summary = (

        df.groupby("Crop", as_index=False)

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

        crop_summary,

        x="Crop",

        y="Production",

        color="Production",

        title="Top Producing Crops"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

st.write("")

col1, col2 = st.columns(2)

# ==========================================================
# PRIORITY
# ==========================================================

with col1:

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

# ==========================================================
# MANAGEMENT
# ==========================================================

with col2:

    management = (

        df["Management_Area"]

        .value_counts()

        .head(10)

        .reset_index()

    )

    management.columns = [

        "Management",

        "Count"

    ]

    fig = create_bar_chart(

        management,

        x="Management",

        y="Count",

        color="Count",

        title="Management Areas"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

st.write("")

col1, col2 = st.columns(2)

# ==========================================================
# WEATHER
# ==========================================================

with col1:

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

        title="Highest Average Temperature"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ==========================================================
# RAINFALL
# ==========================================================

with col2:

    rainfall = (

        df.groupby(

            "State",

            as_index=False

        )

        .agg({

            "total_rainfall_mm":"mean"

        })

        .sort_values(

            "total_rainfall_mm",

            ascending=False

        )

        .head(10)

    )

    fig = create_horizontal_bar(

        rainfall,

        x="total_rainfall_mm",

        y="State",

        color="total_rainfall_mm",

        title="Highest Rainfall"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

st.divider()

st.header("📈 Production Trend")

trend = (

    df.groupby(

        "Start_Year",

        as_index=False

    )

    .agg({

        "Production":"sum"

    })

)

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


# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

st.divider()

st.header("💡 AI Powered Business Insights")

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

highest_yield = (
    df.groupby("Crop")["Yield"]
    .mean()
    .idxmax()
)

high_priority = (
    df["Priority"] == "High Priority"
).sum()

critical = (
    df["Priority"] == "Immediate Action Required"
).sum()

c1, c2 = st.columns(2)

with c1:

    st.success(f"""

### 🏆 Production Leader

**State :** {top_state}

**Top Crop :** {top_crop}

**Highest Average Yield Crop :** {highest_yield}

""")

with c2:

    st.warning(f"""

### 🚨 Decision Summary

High Priority Records : **{high_priority:,}**

Immediate Action Required : **{critical:,}**

Recommendation Engine : **Active**

""")
    
# ==========================================================
# WEATHER OVERVIEW
# ==========================================================

st.divider()

st.header("🌦 Weather Intelligence")

c1, c2, c3 = st.columns(3)

c1.metric(

    "🌡 Avg Temperature",

    f"{df['avg_temp_c'].mean():.2f} °C"

)

c2.metric(

    "🌧 Avg Rainfall",

    f"{df['total_rainfall_mm'].mean():.2f} mm"

)

c3.metric(

    "💧 Avg Humidity",

    f"{df['avg_humidity_percent'].mean():.2f}%"

)

# ==========================================================
# SOIL SUMMARY
# ==========================================================

st.divider()

st.header("🌱 Soil Health")

soil = df[
    [

        "N",

        "P",

        "K",

        "pH"

    ]

].mean()

soil_df = soil.reset_index()

soil_df.columns = [

    "Parameter",

    "Average"

]

fig = create_bar_chart(

    soil_df,

    x="Parameter",

    y="Average",

    color="Average",

    title="Average Soil Parameters"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ==========================================================
# MODEL SUMMARY
# ==========================================================

st.divider()

st.header("🤖 Machine Learning Status")

c1, c2, c3, c4 = st.columns(4)

c1.metric(

    "Model",

    "Random Forest"

)

c2.metric(

    "Prediction",

    "Ready"

)

c3.metric(

    "Recommendation",

    "Active"

)

c4.metric(

    "Dataset",

    "Validated"

)


# ==========================================================
# QUICK ACTIONS
# ==========================================================

st.divider()

st.header("⚡ Quick Actions")

a, b, c = st.columns(3)

with a:

    st.info("""

📊 Explore Crop Analytics

Navigate to Crop Explorer
for detailed crop analysis.

""")

with b:

    st.info("""

🏛 Explore State Analytics

Analyze state-wise
agriculture performance.

""")

with c:

    st.info("""

🧠 Open Recommendation Engine

View recommendations.

""")
    
# ==========================================================
# FEATURES
# ==========================================================

st.divider()

st.header("🚀 Platform Features")

st.markdown("""

✅ Agricultural Production Analytics

✅ Weather Intelligence

✅ Soil Intelligence

✅ Machine Learning Prediction

✅ Recommendation Engine

✅ Business Intelligence

✅ Interactive Dashboard

✅ Dataset Explorer

""")

