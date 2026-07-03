import streamlit as st
import pandas as pd
import joblib

from utils.load_data import load_data
from utils.sidebar import sidebar_filters

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="AI Yield Prediction",

    page_icon="🤖",

    layout="wide"

)

# ==========================================================
# LOAD DATA
# ==========================================================

df = load_data()

df = sidebar_filters(df)

# ==========================================================
# LOAD MODEL
# ==========================================================

model = joblib.load(

    "models/random_forest_model.pkl"

)

encoders = joblib.load(

    "models/label_encoders.pkl"

)

feature_columns = joblib.load(

    "models/feature_columns.pkl"

)

# ==========================================================
# HERO
# ==========================================================

st.markdown("""

<div class="hero">

<h1>🤖 AI Crop Yield Prediction</h1>

<p style="font-size:18px">

Predict agricultural yield using the trained
Random Forest Machine Learning model.

</p>

</div>

""",

unsafe_allow_html=True)

st.write("")

# ==========================================================
# INPUT SECTION
# ==========================================================

st.header("🌾 Crop Information")

col1, col2 = st.columns(2)

with col1:

    state = st.selectbox(

        "State",

        sorted(df["State"].unique())

    )

    crop = st.selectbox(

        "Crop",

        sorted(df["Crop"].unique())

    )

with col2:

    season = st.selectbox(

        "Season",

        sorted(df["Season"].unique())

    )

    area = st.number_input(

        "Area (Hectares)",

        min_value=0.10,

        value=5.00,

        step=0.50

    )

st.divider()

# ==========================================================
# WEATHER
# ==========================================================

st.header("🌦 Weather Conditions")

c1, c2, c3 = st.columns(3)

with c1:

    temperature = st.number_input(

        "Average Temperature (°C)",

        value=26.0,

        step=0.5

    )

with c2:

    rainfall = st.number_input(

        "Total Rainfall (mm)",

        value=1200.0,

        step=10.0

    )

with c3:

    humidity = st.number_input(

        "Average Humidity (%)",

        value=75.0,

        step=1.0

    )

st.divider()

# ==========================================================
# SOIL
# ==========================================================

st.header("🌱 Soil Parameters")

c1, c2, c3, c4 = st.columns(4)

with c1:

    nitrogen = st.number_input(

        "Nitrogen (N)",

        value=60.0

    )

with c2:

    phosphorus = st.number_input(

        "Phosphorus (P)",

        value=35.0

    )

with c3:

    potassium = st.number_input(

        "Potassium (K)",

        value=40.0

    )

with c4:

    ph = st.number_input(

        "Soil pH",

        value=6.5,

        step=0.1

    )

st.divider()

# ==========================================================
# PREDICT BUTTON
# ==========================================================

predict = st.button(

    "🚀 Predict Crop Yield",

    use_container_width=True

)

# ==========================================================
# MODEL INFERENCE
# ==========================================================

if predict:

    state_encoded = encoders["State"].transform([state])[0]

    crop_encoded = encoders["Crop"].transform([crop])[0]

    season_encoded = encoders["Season"].transform([season])[0]

    input_df = pd.DataFrame({

        "State":[state_encoded],

        "Crop":[crop_encoded],

        "Season":[season_encoded],

        "Area":[area],

        "avg_temp_c":[temperature],

        "total_rainfall_mm":[rainfall],

        "avg_humidity_percent":[humidity],

        "N":[nitrogen],

        "P":[phosphorus],

        "K":[potassium],

        "pH":[ph]

    })

    input_df = input_df[feature_columns]

    prediction = float(

        model.predict(input_df)[0]

    )

    st.divider()

    st.header("📊 Prediction Result")

    a, b, c = st.columns(3)

    a.metric(

        "🌾 Predicted Yield",

        f"{prediction:.2f} t/ha"

    )

    b.metric(

        "📍 State",

        state

    )

    c.metric(

        "🌱 Crop",

        crop

    )

    st.divider()

        # ==========================================================
    # YIELD STATUS
    # ==========================================================

    if prediction >= 5:

        status = "Excellent"

        color = "🟢"

    elif prediction >= 3:

        status = "Good"

        color = "🟡"

    elif prediction >= 1:

        status = "Average"

        color = "🟠"

    else:

        status = "Poor"

        color = "🔴"

    left, right = st.columns(2)

    with left:

        st.success(f"""

### 🤖 AI Prediction Summary

**Predicted Yield**

➡ {prediction:.2f} t/ha

**Yield Status**

➡ {color} {status}

**Machine Learning Model**

➡ Random Forest Regressor

""")

    with right:

        st.info(f"""

### 📋 Input Summary

**State**

➡ {state}

**Crop**

➡ {crop}

**Season**

➡ {season}

**Area**

➡ {area:.2f} ha

""")

    st.divider()

        # ==========================================================
    # FEATURE SUMMARY
    # ==========================================================

    st.header("🌱 Input Feature Summary")

    summary = pd.DataFrame({

        "Feature":[

            "Temperature",

            "Rainfall",

            "Humidity",

            "Nitrogen",

            "Phosphorus",

            "Potassium",

            "Soil pH"

        ],

        "Value":[

            temperature,

            rainfall,

            humidity,

            nitrogen,

            phosphorus,

            potassium,

            ph

        ]

    })

    st.dataframe(

        summary,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

        # ==========================================================
    # AI DECISION SUPPORT
    # ==========================================================

    st.header("🧠 AI Decision Support")

    recommendations = []

    if rainfall < 800:
        recommendations.append("💧 Increase irrigation frequency.")

    elif rainfall > 2000:
        recommendations.append("🌧 Improve field drainage to avoid waterlogging.")

    if temperature > 35:
        recommendations.append("🌡 High temperature detected. Consider heat stress management.")

    elif temperature < 15:
        recommendations.append("❄ Low temperature detected. Protect crop from cold stress.")

    if nitrogen < 50:
        recommendations.append("🧪 Apply Nitrogen fertilizer.")

    if phosphorus < 30:
        recommendations.append("🌱 Apply Phosphorus fertilizer.")

    if potassium < 40:
        recommendations.append("🌾 Apply Potassium fertilizer.")

    if ph < 5.5:
        recommendations.append("🪨 Apply lime to increase soil pH.")

    elif ph > 7.5:
        recommendations.append("🧪 Reduce alkalinity using sulphur treatment.")

    if prediction < 1:
        recommendations.append("🚨 Very low yield expected. Immediate intervention required.")

    elif prediction < 3:
        recommendations.append("⚠ Improve irrigation and nutrient management.")

    elif prediction < 5:
        recommendations.append("✅ Crop health is acceptable. Continue monitoring.")

    else:
        recommendations.append("🏆 Excellent yield potential. Maintain current practices.")

     # ==========================================================
    # PRIORITY ENGINE
    # ==========================================================

    risk_score = 0

    if prediction < 1:
        risk_score += 3

    elif prediction < 3:
        risk_score += 2

    if rainfall < 800 or rainfall > 2000:
        risk_score += 1

    if temperature > 35 or temperature < 15:
        risk_score += 1

    if nitrogen < 50:
        risk_score += 1

    if phosphorus < 30:
        risk_score += 1

    if potassium < 40:
        risk_score += 1

    if ph < 5.5 or ph > 7.5:
        risk_score += 1

    if risk_score >= 6:

        priority = "🔴 Immediate Action Required"

    elif risk_score >= 4:

        priority = "🟠 High Priority"

    elif risk_score >= 2:

        priority = "🟡 Moderate Priority"

    else:

        priority = "🟢 Routine Monitoring"

    
        # ==========================================================
    # DISPLAY RECOMMENDATIONS
    # ==========================================================

    left, right = st.columns(2)

    with left:

        st.subheader("🚨 Priority Level")

        st.success(priority)

    with right:

        st.subheader("📈 Recommended Actions")

        st.metric(

            "Total",

            len(recommendations)

        )

    st.subheader("🌾 AI Recommendations")

    for item in recommendations:

        st.write("•", item)

    st.divider()

        # ==========================================================
    # PREDICTION REPORT
    # ==========================================================

    st.header("📋 Prediction Report")

    report = pd.DataFrame({

        "State":[state],

        "Crop":[crop],

        "Season":[season],

        "Area (ha)":[area],

        "Temperature (°C)":[temperature],

        "Rainfall (mm)":[rainfall],

        "Humidity (%)":[humidity],

        "Nitrogen":[nitrogen],

        "Phosphorus":[phosphorus],

        "Potassium":[potassium],

        "Soil pH":[ph],

        "Predicted Yield (t/ha)":[round(prediction,2)],

        "Yield Status":[status],

        "Priority":[priority]

    })

    st.dataframe(

        report,

        use_container_width=True,

        hide_index=True

    )

    st.divider()


        # ==========================================================
    # RISK ANALYSIS
    # ==========================================================

    st.header("📈 Risk Analysis")

    c1, c2, c3 = st.columns(3)

    c1.metric(

        "Risk Score",

        risk_score

    )

    c2.metric(

        "Priority",

        priority

    )

    c3.metric(

        "Recommendations",

        len(recommendations)

    )

    st.divider()


        # ==========================================================
    # RECOMMENDATION REPORT
    # ==========================================================

    st.header("🌱 Recommendation Summary")

    recommendation_df = pd.DataFrame({

        "Recommendation":recommendations

    })

    st.dataframe(

        recommendation_df,

        use_container_width=True,

        hide_index=True

    )

    st.divider()


        # ==========================================================
    # DOWNLOAD REPORTS
    # ==========================================================

    report_csv = report.to_csv(

        index=False

    )

    recommendation_csv = recommendation_df.to_csv(

        index=False

    )

    left, right = st.columns(2)

    with left:

        st.download_button(

            "⬇ Download Prediction Report",

            report_csv,

            file_name="Prediction_Report.csv",

            mime="text/csv"

        )

    with right:

        st.download_button(

            "⬇ Download Recommendations",

            recommendation_csv,

            file_name="Recommendations.csv",

            mime="text/csv"

        )

    st.divider()

        # ==========================================================
    # FINAL SUMMARY
    # ==========================================================

    st.success(f"""

## ✅ Prediction Completed Successfully

The Random Forest model estimated a crop yield of

### 🌾 {prediction:.2f} t/ha

Priority Level

### {priority}

Total Recommendations Generated

### {len(recommendations)}

""")