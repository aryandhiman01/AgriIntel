import streamlit as st
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AgriIntel",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

css_path = Path(__file__).parent / "assets" / "style.css"

with open(css_path) as f:

    st.markdown(

        f"<style>{f.read()}</style>",

        unsafe_allow_html=True

    )

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.image(

        "assets/logo.png",

        use_container_width=True

    )

    st.markdown("# 🌾 AgriIntel")

    st.caption("Agriculture Intelligence & Decision Support Platform")

    st.divider()

    st.success("Version 1.0")

    st.caption("Built using Machine Learning")

# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.title("🌾 AgriIntel")

st.markdown(

"""
### Agriculture Intelligence & Decision Support Platform

Analyze crop production, explore agricultural insights, predict crop yield,
and generate intelligent recommendations using Machine Learning.

"""
)

st.divider()

# --------------------------------------------------
# INFORMATION
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.info(

        "📊 Business Intelligence"

    )

with col2:

    st.info(

        "🤖 Machine Learning"

    )

with col3:

    st.info(

        "🧠 Recommendation Engine"

    )

st.divider()

st.markdown(

"""
### 👈 Select a page from the sidebar to begin exploring the platform.

Available Modules:

- Home Dashboard
- Crop Explorer
- State Explorer
- Analytics
- Crop Yield Prediction
- Recommendation Engine
- Dataset Explorer

"""
)