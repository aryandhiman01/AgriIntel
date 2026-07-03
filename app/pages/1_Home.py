import streamlit as st
import plotly.express as px

from utils.load_data import (
    load_data,
    filter_data,
    get_states,
    get_crops,
    get_seasons,
    get_kpis
)

from utils.helper import (
    format_number,
    format_yield
)


# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(

    page_title="Home",

    page_icon="🏠",

    layout="wide"

)


# ======================================================
# LOAD DATA
# ======================================================

df = load_data()


# ======================================================
# SIDEBAR FILTERS
# ======================================================

st.sidebar.header("Filters")

state = st.sidebar.selectbox(

    "State",

    get_states(df)

)

crop = st.sidebar.selectbox(

    "Crop",

    get_crops(df)

)

season = st.sidebar.selectbox(

    "Season",

    get_seasons(df)

)

filtered = filter_data(

    df,

    state,

    crop,

    season

)


# ======================================================
# TITLE
# ======================================================

st.title("🌾 AgriIntel Dashboard")

st.caption(
    "Agriculture Intelligence & Decision Support Platform"
)

st.divider()


# ======================================================
# KPIs
# ======================================================

kpi = get_kpis(filtered)

c1,c2,c3 = st.columns(3)

c4,c5,c6 = st.columns(3)


c1.metric(

    "📄 Records",

    format_number(

        kpi["records"]

    )

)

c2.metric(

    "🏛 States",

    kpi["states"]

)

c3.metric(

    "🌾 Crops",

    kpi["crops"]

)

c4.metric(

    "🌱 Total Production",

    format_number(

        kpi["production"]

    )

)

c5.metric(

    "📈 Avg Yield",

    format_yield(

        kpi["avg_yield"]

    )

)

c6.metric(

    "🤖 Avg Prediction",

    format_yield(

        kpi["avg_prediction"]

    )

)

st.divider()


# ======================================================
# ROW 1
# ======================================================

left,right = st.columns(2)

with left:

    production = (

        filtered

        .groupby("State")["Production"]

        .sum()

        .sort_values(ascending=False)

        .head(10)

        .reset_index()

    )

    fig = px.bar(

        production,

        x="Production",

        y="State",

        orientation="h",

        color="Production",

        title="Top Production States"

    )

    fig.update_layout(

        height=500

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    crops = (

        filtered

        .groupby("Crop")["Production"]

        .sum()

        .sort_values(ascending=False)

        .head(10)

        .reset_index()

    )

    fig = px.bar(

        crops,

        x="Crop",

        y="Production",

        color="Production",

        title="Top Producing Crops"

    )

    fig.update_layout(

        height=500

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )


# ======================================================
# ROW 2
# ======================================================

left,right = st.columns(2)

with left:

    priority = (

        filtered["Priority"]

        .value_counts()

        .reset_index()

    )

    priority.columns = [

        "Priority",

        "Count"

    ]

    fig = px.pie(

        priority,

        names="Priority",

        values="Count",

        hole=.45,

        title="Priority Distribution"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    area = (

        filtered["Management_Area"]

        .value_counts()

        .head(10)

        .reset_index()

    )

    area.columns=[

        "Management",

        "Count"

    ]

    fig = px.bar(

        area,

        x="Management",

        y="Count",

        color="Count",

        title="Management Areas"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )


# ======================================================
# DATA PREVIEW
# ======================================================

st.divider()

st.subheader("Dataset Preview")

st.dataframe(

    filtered,

    use_container_width=True,

    height=450

)


# ======================================================
# DOWNLOAD
# ======================================================

st.download_button(

    "⬇ Download Filtered Dataset",

    filtered.to_csv(index=False),

    "Filtered_Dataset.csv",

    "text/csv"

)