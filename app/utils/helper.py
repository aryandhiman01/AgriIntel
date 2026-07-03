"""
==========================================================
AgriIntel
Helper Utilities
==========================================================

Reusable helper functions used across
the Streamlit dashboard.

==========================================================
"""

import pandas as pd


# ==========================================================
# NUMBER FORMATTER
# ==========================================================

def format_number(value):

    """
    Convert numbers into readable format.

    Example

    1450 -> 1.45K

    1500000 -> 1.50M
    """

    if pd.isna(value):

        return "-"

    value = float(value)

    if value >= 1_000_000_000:

        return f"{value/1_000_000_000:.2f}B"

    if value >= 1_000_000:

        return f"{value/1_000_000:.2f}M"

    if value >= 1_000:

        return f"{value/1_000:.2f}K"

    return f"{value:.2f}"


# ==========================================================
# PERCENTAGE FORMATTER
# ==========================================================

def format_percentage(value):

    if pd.isna(value):

        return "-"

    return f"{value:.2f}%"


# ==========================================================
# YIELD FORMATTER
# ==========================================================

def format_yield(value):

    if pd.isna(value):

        return "-"

    return f"{value:.2f} t/ha"


# ==========================================================
# PRIORITY COLOR
# ==========================================================

def priority_color(priority):

    colors = {

        "Immediate Action Required": "#E74C3C",

        "High Priority": "#F39C12",

        "Moderate Priority": "#F1C40F",

        "Routine Monitoring": "#2ECC71"

    }

    return colors.get(priority, "#3498DB")


# ==========================================================
# MANAGEMENT COLOR
# ==========================================================

def management_color(area):

    mapping = {

        "Water Management": "#3498DB",

        "Climate Adaptation": "#16A085",

        "Soil Health": "#8E44AD",

        "Nutrient Management": "#27AE60",

        "General Monitoring": "#95A5A6"

    }

    return mapping.get(area, "#34495E")


# ==========================================================
# RECOMMENDATION COLOR
# ==========================================================

def recommendation_color(text):

    text = str(text).lower()

    if "irrigation" in text:

        return "#3498DB"

    if "nitrogen" in text:

        return "#2ECC71"

    if "phosphorus" in text:

        return "#9B59B6"

    if "potassium" in text:

        return "#F39C12"

    if "fungal" in text:

        return "#E74C3C"

    return "#1ABC9C"


# ==========================================================
# STATUS BADGE
# ==========================================================

def get_status(predicted):

    if predicted < 1:

        return "Critical"

    elif predicted < 2:

        return "Low"

    elif predicted < 4:

        return "Average"

    else:

        return "Excellent"


# ==========================================================
# ICONS
# ==========================================================

def status_icon(status):

    icons = {

        "Critical": "🔴",

        "Low": "🟠",

        "Average": "🟡",

        "Excellent": "🟢"

    }

    return icons.get(status, "⚪")


# ==========================================================
# DATAFRAME DOWNLOAD
# ==========================================================

def convert_csv(df):

    return df.to_csv(index=False).encode("utf-8")