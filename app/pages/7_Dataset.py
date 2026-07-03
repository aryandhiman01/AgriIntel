import streamlit as st
import pandas as pd

from utils.load_data import load_data
from utils.sidebar import sidebar_filters
from utils.helper import format_number

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Dataset Explorer",

    page_icon="📂",

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

<h1>📂 Dataset Explorer</h1>

<p style="font-size:18px;">

Explore, search, filter and download the complete
Agricultural Intelligence dataset.

</p>

</div>

""", unsafe_allow_html=True)

st.write("")

# ==========================================================
# SUMMARY
# ==========================================================

rows = len(df)

columns = len(df.columns)

states = df["State"].nunique()

crops = df["Crop"].nunique()

c1,c2,c3,c4 = st.columns(4)

c1.metric(

    "📄 Records",

    format_number(rows)

)

c2.metric(

    "📑 Columns",

    columns

)

c3.metric(

    "🏛 States",

    states

)

c4.metric(

    "🌾 Crops",

    crops

)

st.divider()

# ==========================================================
# SEARCH
# ==========================================================

st.header("🔍 Search Dataset")

keyword = st.text_input(

    "Search by State, District or Crop"

)

filtered = df.copy()

if keyword:

    mask = (

        filtered["State"]

        .str.contains(

            keyword,

            case=False,

            na=False

        )

        |

        filtered["District"]

        .str.contains(

            keyword,

            case=False,

            na=False

        )

        |

        filtered["Crop"]

        .str.contains(

            keyword,

            case=False,

            na=False

        )

    )

    filtered = filtered[mask]

    # ==========================================================
# DATASET STATS
# ==========================================================

st.header("📈 Dataset Statistics")

stats = pd.DataFrame({

    "Statistic":[

        "Rows",

        "Columns",

        "Missing Values",

        "Duplicate Rows"

    ],

    "Value":[

        len(filtered),

        len(filtered.columns),

        filtered.isna().sum().sum(),

        filtered.duplicated().sum()

    ]

})

st.dataframe(

    stats,

    use_container_width=True,

    hide_index=True

)

st.divider()

# ==========================================================
# COLUMN INFO
# ==========================================================

st.header("📑 Column Information")

column_info = pd.DataFrame({

    "Column":filtered.columns,

    "Data Type":filtered.dtypes.astype(str),

    "Missing Values":filtered.isna().sum().values

})

st.dataframe(

    column_info,

    use_container_width=True,

    hide_index=True

)

st.divider()

# ==========================================================
# DATASET
# ==========================================================

st.header("📋 Dataset Preview")

st.dataframe(

    filtered,

    use_container_width=True,

    height=500,

    hide_index=True

)

st.divider()

# ==========================================================
# DOWNLOAD
# ==========================================================

left,right = st.columns(2)

with left:

    st.download_button(

        "⬇ Download CSV",

        filtered.to_csv(index=False),

        file_name="AgriIntel_Dataset.csv",

        mime="text/csv"

    )

with right:

    st.download_button(

        "⬇ Download Excel",

        filtered.to_excel(index=False),

        file_name="AgriIntel_Dataset.xlsx"

    )

    # ==========================================================
# DATASET HEALTH
# ==========================================================

st.divider()

st.header("🩺 Dataset Health Report")

missing = filtered.isna().sum().sum()

duplicates = filtered.duplicated().sum()

if missing == 0 and duplicates == 0:

    st.success("""

✅ Dataset Quality Check Passed

• No Missing Values

• No Duplicate Records

• Ready for Analytics & Machine Learning

""")

else:

    st.warning(f"""

Missing Values : {missing}

Duplicate Records : {duplicates}

Please clean the dataset before analysis.

""")