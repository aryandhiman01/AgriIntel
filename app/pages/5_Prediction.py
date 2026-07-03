import streamlit as st
import pandas as pd
import joblib

from utils.load_data import load_data
from utils.sidebar import sidebar_filters
from utils.helper import format_yield

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Yield Prediction",

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

Predict future crop yield using our trained
Random Forest Machine Learning model.

</p>

</div>

""",

unsafe_allow_html=True)

st.write("")

st.header("🌾 Crop Information")

left,right = st.columns(2)

with left:

    state = st.selectbox(

        "State",

        sorted(

            df["State"].unique()

        )

    )

    crop = st.selectbox(

        "Crop",

        sorted(

            df["Crop"].unique()

        )

    )

with right:

    season = st.selectbox(

        "Season",

        sorted(

            df["Season"].unique()

        )

    )

    area = st.number_input(

        "Area (Hectares)",

        min_value=0.10,

        value=5.00,

        step=0.50

    )

st.divider()

st.header("🌦 Weather Conditions")

c1,c2,c3 = st.columns(3)

with c1:

    temperature = st.number_input(

        "Temperature (°C)",

        value=26.0,

        step=0.5

    )

with c2:

    rainfall = st.number_input(

        "Rainfall (mm)",

        value=1200.0,

        step=10.0

    )

with c3:

    humidity = st.number_input(

        "Humidity (%)",

        value=75.0,

        step=1.0

    )

st.divider()

st.header("🌱 Soil Parameters")

c1,c2,c3,c4 = st.columns(4)

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

predict = st.button(

    "🚀 Predict Crop Yield",

    use_container_width=True

)

# ==========================================================
# PREDICTION
# ==========================================================

if predict:

    # Encode categorical features
    state_encoded = encoders["State"].transform([state])[0]
    crop_encoded = encoders["Crop"].transform([crop])[0]
    season_encoded = encoders["Season"].transform([season])[0]

    # Create input dataframe
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

    # Match training feature order
    input_df = input_df[feature_columns]

    # Prediction
    prediction = model.predict(input_df)[0]

    st.divider()

    st.header("📊 Prediction Result")

    c1, c2, c3 = st.columns(3)

    c1.metric(

        "🌾 Predicted Yield",

        f"{prediction:.2f} t/ha"

    )

    c2.metric(

        "📍 State",

        state

    )

    c3.metric(

        "🌱 Crop",

        crop

    )

    st.divider()

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

Predicted Yield

➡ **{prediction:.2f} t/ha**

Yield Status

➡ **{color} {status}**

Model

➡ **Random Forest Regressor**

""")

    with right:

        st.info(f"""

### 📋 Input Summary

State

➡ **{state}**

Crop

➡ **{crop}**

Season

➡ **{season}**

Area

➡ **{area:.2f} ha**

""")

    st.divider()

    st.header("📈 Feature Summary")

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

    result = pd.DataFrame({

        "State":[state],

        "Crop":[crop],

        "Season":[season],

        "Area":[area],

        "Predicted_Yield":[prediction]

    })

    st.download_button(

        "⬇ Download Prediction",

        result.to_csv(index=False),

        file_name="prediction.csv",

        mime="text/csv"

    )

# ==========================================================
# AI DECISION SUPPORT
# ==========================================================

st.header("🧠 AI Decision Support")

recommendations = []

# Rainfall
if rainfall < 800:
    recommendations.append("💧 Increase irrigation frequency.")

elif rainfall > 2000:
    recommendations.append("🌧 Improve field drainage to avoid waterlogging.")

# Temperature
if temperature > 35:
    recommendations.append("🌡 Use heat stress management practices.")

elif temperature < 15:
    recommendations.append("❄ Protect crops from cold stress.")

# Nitrogen
if nitrogen < 50:
    recommendations.append("🧪 Apply Nitrogen fertilizer.")

# Phosphorus
if phosphorus < 30:
    recommendations.append("🌱 Apply Phosphorus fertilizer.")

# Potassium
if potassium < 40:
    recommendations.append("🌾 Apply Potassium fertilizer.")

# Soil pH
if ph < 5.5:
    recommendations.append("🪨 Apply lime to increase soil pH.")

elif ph > 7.5:
    recommendations.append("🧪 Consider sulphur-based soil treatment.")

# Yield based advice
if prediction < 1:
    recommendations.append("🚨 Expected yield is very low. Immediate intervention is required.")

elif prediction < 3:
    recommendations.append("⚠ Improve nutrient and irrigation management.")

elif prediction < 5:
    recommendations.append("✅ Crop condition is acceptable. Continue monitoring.")

else:
    recommendations.append("🏆 Excellent yield potential. Maintain current practices.")

# ==========================================================
# DISPLAY RECOMMENDATIONS
# ==========================================================

left, right = st.columns(2)

with left:

    st.subheader("🚨 Priority")

    st.success(priority)

with right:

    st.subheader("📈 Total Recommendations")

    st.metric(

        "Actions",

        len(recommendations)

    )

st.subheader("🌱 Recommended Actions")

for rec in recommendations:

    st.write("•", rec)

st.divider()

# ==========================================================
# PREDICTION REPORT
# ==========================================================

report = pd.DataFrame({

    "State":[state],

    "Crop":[crop],

    "Season":[season],

    "Predicted_Yield":[round(prediction,2)],

    "Priority":[priority],

    "Recommendations":[" | ".join(recommendations)]

})

st.download_button(

    "⬇ Download Prediction Report",

    report.to_csv(index=False),

    file_name="Prediction_Report.csv",

    mime="text/csv"

)