"""
==========================================================
AgriIntel
Sidebar Component
==========================================================

Reusable sidebar used across the dashboard.

Author : Aryan Dhiman
==========================================================
"""

import streamlit as st

from utils.load_data import (
    filter_data,
    get_states,
    get_crops,
    get_seasons
)


# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

def sidebar_filters(df):

    """
    Creates common sidebar filters for all pages.

    Returns
    -------
    Filtered DataFrame
    """

    with st.sidebar:

        st.title("🌾 AgriIntel")

        st.caption(
            "Agriculture Intelligence Platform"
        )

        st.divider()

        st.subheader("Filters")

        state = st.selectbox(

            "State",

            get_states(df)

        )

        crop = st.selectbox(

            "Crop",

            get_crops(df)

        )

        season = st.selectbox(

            "Season",

            get_seasons(df)

        )

        filtered = filter_data(

            df,

            state,

            crop,

            season

        )

        st.divider()

        st.markdown("### Dataset Summary")

        st.write(

            f"📄 Records : {len(filtered):,}"

        )

        st.write(

            f"🏛 States : {filtered['State'].nunique()}"

        )

        st.write(

            f"🌾 Crops : {filtered['Crop'].nunique()}"

        )

        st.divider()

        st.caption("AgriIntel v1.0")

    return filtered