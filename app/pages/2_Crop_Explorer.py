import streamlit as st
import plotly.express as px

from utils.load_data import load_data
from utils.sidebar import sidebar_filters
from utils.helper import (
    format_number,
    format_yield
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="Crop Explorer",

    page_icon="🌾",

    layout="wide"

)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

filtered = sidebar_filters(df)

# =====================================================
# PAGE TITLE
# =====================================================

st.title("🌾 Crop Explorer")

st.caption(
    "Explore crop performance, productivity, weather and recommendations."
)

st.divider()

# =====================================================
# CROP SELECTION
# =====================================================

crop = st.selectbox(

    "Select Crop",

    sorted(filtered["Crop"].unique())

)

crop_df = filtered[
    filtered["Crop"] == crop
]

# =====================================================
# KPIs
# =====================================================

c1,c2,c3,c4 = st.columns(4)

c1.metric(

    "Production",

    format_number(

        crop_df["Production"].sum()

    )

)

c2.metric(

    "Average Yield",

    format_yield(

        crop_df["Yield"].mean()

    )

)

c3.metric(

    "Predicted Yield",

    format_yield(

        crop_df["Predicted_Yield"].mean()

    )

)

c4.metric(

    "States",

    crop_df["State"].nunique()

)

st.divider()

# =====================================================
# ROW 1
# =====================================================

left,right = st.columns(2)

with left:

    state_prod = (

        crop_df

        .groupby("State")["Production"]

        .sum()

        .sort_values(ascending=False)

        .head(10)

        .reset_index()

    )

    fig = px.bar(

        state_prod,

        x="Production",

        y="State",

        orientation="h",

        color="Production",

        title="Top Producing States"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    season_prod = (

        crop_df

        .groupby("Season")["Production"]

        .sum()

        .reset_index()

    )

    fig = px.pie(

        season_prod,

        names="Season",

        values="Production",

        hole=.45,

        title="Season Contribution"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# =====================================================
# ROW 2
# =====================================================

left,right = st.columns(2)

with left:

    fig = px.scatter(

        crop_df,

        x="avg_temp_c",

        y="Yield",

        color="Priority",

        hover_data=[

            "State"

        ],

        title="Temperature vs Yield"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    fig = px.scatter(

        crop_df,

        x="total_rainfall_mm",

        y="Yield",

        color="Priority",

        hover_data=[

            "State"

        ],

        title="Rainfall vs Yield"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# =====================================================
# ROW 3
# =====================================================

left,right = st.columns(2)

with left:

    priority = (

        crop_df["Priority"]

        .value_counts()

        .reset_index()

    )

    priority.columns=[

        "Priority",

        "Count"

    ]

    fig = px.bar(

        priority,

        x="Priority",

        y="Count",

        color="Priority",

        title="Priority Distribution"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    management = (

        crop_df["Management_Area"]

        .value_counts()

        .head(10)

        .reset_index()

    )

    management.columns=[

        "Management",

        "Count"

    ]

    fig = px.bar(

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

# =====================================================
# RECOMMENDATION
# =====================================================

st.divider()

st.subheader("🧠 Recommendation Summary")

recommendation = (

    crop_df

    [

        [

            "State",

            "Recommendation",

            "Priority"

        ]

    ]

)

st.dataframe(

    recommendation,

    use_container_width=True,

    height=300

)

# =====================================================
# DATASET
# =====================================================

st.divider()

st.subheader("Filtered Dataset")

st.dataframe(

    crop_df,

    use_container_width=True,

    height=450

)

# =====================================================
# DOWNLOAD
# =====================================================

st.download_button(

    "⬇ Download Crop Report",

    crop_df.to_csv(index=False),

    file_name=f"{crop}_Report.csv",

    mime="text/csv"

)