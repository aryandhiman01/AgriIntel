"""
==========================================================
AgriIntel
Reusable Plotly Charts
==========================================================

Author : Aryan Dhiman

This module contains reusable Plotly chart
functions used across the complete dashboard.
==========================================================
"""

import plotly.express as px
import plotly.graph_objects as go


# ==========================================================
# COMMON THEME
# ==========================================================

BACKGROUND = "#08111F"

CARD = "#132238"

FONT = "white"

ACCENT = "#59E390"

GRID = "rgba(255,255,255,0.08)"


# ==========================================================
# APPLY COMMON LAYOUT
# ==========================================================

def apply_layout(

    fig,

    title

):

    fig.update_layout(

        title={

            "text": title,

            "x":0.03,

            "font":{

                "size":22,

                "color":FONT

            }

        },

        paper_bgcolor=BACKGROUND,

        plot_bgcolor=BACKGROUND,

        font=dict(

            color=FONT,

            family="Inter"

        ),

        margin=dict(

            l=25,

            r=25,

            t=60,

            b=25

        ),

        legend=dict(

            bgcolor="rgba(0,0,0,0)"

        ),

        hoverlabel=dict(

            bgcolor=CARD,

            font_size=14

        )

    )

    fig.update_xaxes(

        showgrid=True,

        gridcolor=GRID,

        zeroline=False

    )

    fig.update_yaxes(

        showgrid=True,

        gridcolor=GRID,

        zeroline=False

    )

    return fig


# ==========================================================
# BAR CHART
# ==========================================================

def create_bar_chart(

    data,

    x,

    y,

    color,

    title

):

    fig = px.bar(

        data,

        x=x,

        y=y,

        color=color,

        text_auto=".2s",

        color_continuous_scale="Viridis"

    )

    fig.update_traces(

        marker_line_width=0

    )

    return apply_layout(

        fig,

        title

    )


# ==========================================================
# HORIZONTAL BAR
# ==========================================================

def create_horizontal_bar(

    data,

    x,

    y,

    color,

    title

):

    fig = px.bar(

        data,

        x=x,

        y=y,

        orientation="h",

        color=color,

        text_auto=".2s",

        color_continuous_scale="Aggrnyl"

    )

    fig.update_traces(

        marker_line_width=0

    )

    return apply_layout(

        fig,

        title

    )


# ==========================================================
# LINE CHART
# ==========================================================

def create_line_chart(

    data,

    x,

    y,

    title

):

    fig = px.line(

        data,

        x=x,

        y=y,

        markers=True

    )

    fig.update_traces(

        line_width=4,

        marker_size=8

    )

    return apply_layout(

        fig,

        title

    )


# ==========================================================
# AREA CHART
# ==========================================================

def create_area_chart(

    data,

    x,

    y,

    title

):

    fig = px.area(

        data,

        x=x,

        y=y

    )

    return apply_layout(

        fig,

        title

    )


# ==========================================================
# KPI INDICATOR
# ==========================================================

def create_indicator(

    value,

    title

):

    fig = go.Figure(

        go.Indicator(

            mode="number",

            value=value,

            title={

                "text":title

            },

            number={

                "font":{

                    "size":48,

                    "color":ACCENT

                }

            }

        )

    )

    fig.update_layout(

        paper_bgcolor=BACKGROUND,

        height=180,

        margin=dict(

            l=10,

            r=10,

            t=40,

            b=10

        )

    )

    return fig


# ==========================================================
# EMPTY CHART
# ==========================================================

def empty_chart(

    title="No Data Available"

):

    fig = go.Figure()

    fig.update_layout(

        title=title,

        paper_bgcolor=BACKGROUND,

        plot_bgcolor=BACKGROUND,

        font_color="white"

    )

    return fig

# ==========================================================
# PIE CHART
# ==========================================================

def create_pie_chart(

    data,

    names,

    values,

    title

):

    fig = px.pie(

        data,

        names=names,

        values=values,

        hole=.45,

        color_discrete_sequence=px.colors.qualitative.Set2

    )

    fig.update_traces(

        textinfo="percent+label",

        pull=[0.02]*len(data)

    )

    return apply_layout(

        fig,

        title

    )


# ==========================================================
# DONUT CHART
# ==========================================================

def create_donut_chart(

    data,

    names,

    values,

    title

):

    fig = px.pie(

        data,

        names=names,

        values=values,

        hole=.65,

        color_discrete_sequence=px.colors.qualitative.Bold

    )

    fig.update_traces(

        textposition="inside",

        textinfo="percent"

    )

    return apply_layout(

        fig,

        title

    )


# ==========================================================
# SCATTER CHART
# ==========================================================

def create_scatter_chart(

    data,

    x,

    y,

    color,

    title

):

    fig = px.scatter(

        data,

        x=x,

        y=y,

        color=color,

        size_max=18,

        opacity=.75

    )

    fig.update_traces(

        marker=dict(

            size=10,

            line=dict(

                width=1,

                color="white"

            )

        )

    )

    return apply_layout(

        fig,

        title

    )


# ==========================================================
# HISTOGRAM
# ==========================================================

def create_histogram(

    data,

    x,

    title

):

    fig = px.histogram(

        data,

        x=x,

        nbins=40,

        color_discrete_sequence=[ACCENT]

    )

    return apply_layout(

        fig,

        title

    )


# ==========================================================
# BOX PLOT
# ==========================================================

def create_box_plot(

    data,

    x,

    y,

    color,

    title

):

    fig = px.box(

        data,

        x=x,

        y=y,

        color=color

    )

    return apply_layout(

        fig,

        title

    )


# ==========================================================
# TREEMAP
# ==========================================================

def create_treemap(

    data,

    path,

    values,

    title

):

    fig = px.treemap(

        data,

        path=path,

        values=values,

        color=values,

        color_continuous_scale="Viridis"

    )

    fig.update_layout(

        paper_bgcolor=BACKGROUND

    )

    return apply_layout(

        fig,

        title

    )


# ==========================================================
# SUNBURST
# ==========================================================

def create_sunburst(

    data,

    path,

    values,

    title

):

    fig = px.sunburst(

        data,

        path=path,

        values=values,

        color=values,

        color_continuous_scale="Turbo"

    )

    fig.update_layout(

        paper_bgcolor=BACKGROUND

    )

    return apply_layout(

        fig,

        title

    )


# ==========================================================
# VIOLIN PLOT
# ==========================================================

def create_violin_plot(

    data,

    x,

    y,

    color,

    title

):

    fig = px.violin(

        data,

        x=x,

        y=y,

        color=color,

        box=True,

        points="outliers"

    )

    return apply_layout(

        fig,

        title

    )


# ==========================================================
# STRIP PLOT
# ==========================================================

def create_strip_plot(

    data,

    x,

    y,

    color,

    title

):

    fig = px.strip(

        data,

        x=x,

        y=y,

        color=color

    )

    return apply_layout(

        fig,

        title

    )


# ==========================================================
# SCATTER CHART
# ==========================================================

def create_scatter_chart(
    df,
    x,
    y,
    color=None,
    size=None,
    title=""
):

    fig = px.scatter(

        df,

        x=x,

        y=y,

        color=color,

        size=size,

        template="plotly_dark",

        title=title,

        height=500

    )

    fig.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        title_x=0.02,

        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )

    )

    return fig


# ==========================================================
# GROUPED BAR CHART
# ==========================================================

def create_grouped_bar(
    data,
    x,
    y,
    color,
    title
):

    fig = px.bar(

        data,

        x=x,

        y=y,

        color=color,

        barmode="group",

        text_auto=".2s",

        template="plotly_dark"

    )

    fig.update_traces(

        marker_line_width=0

    )

    fig.update_layout(

        title={
            "text": title,
            "x": 0.03
        },

        paper_bgcolor=BACKGROUND,

        plot_bgcolor=BACKGROUND,

        font=dict(
            color=FONT,
            family="Inter"
        ),

        margin=dict(
            l=25,
            r=25,
            t=60,
            b=25
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        )

    )

    fig.update_xaxes(

        showgrid=True,

        gridcolor=GRID,

        zeroline=False

    )

    fig.update_yaxes(

        showgrid=True,

        gridcolor=GRID,

        zeroline=False

    )

    return fig