"""
==========================================================
AgriIntel
Data Loader Utility
==========================================================

This module loads the final recommendation dataset
used throughout the Streamlit Dashboard.

Author : Aryan Dhiman
Project : AgriIntel
==========================================================
"""

from pathlib import Path

import pandas as pd
import streamlit as st


# ==========================================================
# DATA PATH
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    ROOT_DIR
    / "data"
    / "final"
    / "master_dataset_recommendation.csv"
)


# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data(show_spinner=False)
def load_data():

    """
    Loads the final AgriIntel dataset.

    Returns
    -------
    pd.DataFrame
    """

    try:

        df = pd.read_csv(DATA_PATH)

    except FileNotFoundError:

        st.error(
            "Dataset not found.\n\n"
            "Expected Location:\n"
            f"{DATA_PATH}"
        )

        st.stop()

    except Exception as e:

        st.error(f"Unable to load dataset.\n\n{e}")

        st.stop()

    return clean_dataframe(df)


# ==========================================================
# CLEAN DATAFRAME
# ==========================================================

def clean_dataframe(df: pd.DataFrame):

    """
    Performs lightweight preprocessing
    required for dashboard.
    """

    df = df.copy()

    # Remove duplicate rows

    df.drop_duplicates(inplace=True)

    # Strip spaces from column names

    df.columns = df.columns.str.strip()

    # Fill text columns

    text_columns = df.select_dtypes(include="object").columns

    df[text_columns] = df[text_columns].fillna("Unknown")

    # Fill numeric columns

    numeric_columns = df.select_dtypes(include="number").columns

    df[numeric_columns] = df[numeric_columns].fillna(0)

    return df


# ==========================================================
# FILTER DATA
# ==========================================================

def filter_data(

    df,

    state=None,

    crop=None,

    season=None

):

    """
    Returns filtered dataframe.
    """

    filtered = df.copy()

    if state and state != "All":

        filtered = filtered[
            filtered["State"] == state
        ]

    if crop and crop != "All":

        filtered = filtered[
            filtered["Crop"] == crop
        ]

    if season and season != "All":

        filtered = filtered[
            filtered["Season"] == season
        ]

    return filtered


# ==========================================================
# UNIQUE VALUES
# ==========================================================

def get_states(df):

    return ["All"] + sorted(

        df["State"].dropna().unique()

    )


def get_crops(df):

    return ["All"] + sorted(

        df["Crop"].dropna().unique()

    )


def get_seasons(df):

    return ["All"] + sorted(

        df["Season"].dropna().unique()

    )


# ==========================================================
# KPI FUNCTIONS
# ==========================================================

def get_kpis(df):

    return {

        "records": len(df),

        "states": df["State"].nunique(),

        "crops": df["Crop"].nunique(),

        "production": df["Production"].sum(),

        "avg_yield": df["Yield"].mean(),

        "avg_prediction": df["Predicted_Yield"].mean()

    }