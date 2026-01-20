import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# Page title
st.set_page_config(page_title="Aadhaar Demographic Dashboard", layout="wide")

st.title("Aadhaar Lifecycle Stress Dashboard")
st.subheader("Madhya Pradesh | Age Group Analysis")

# Load data
df = pd.read_csv("mp_filtered_data.csv")
st.success("Data loaded successfully")

#preview
st.header("Filtered Data Preview")
st.dataframe(df.head(20))

#District wise bar chart 
st.header("District-wise Youth Population (Age 5–17)")
district_data = df.groupby("district")["demo_age_5_17"].sum().sort_values(ascending=False)

fig, ax = plt.subplots()
district_data.head(10).plot(kind="bar", ax=ax)
ax.set_xlabel("District")
ax.set_ylabel("Population")
ax.set_title("Top 10 Districts (Age 5 - 17)")

st.pyplot(fig)

# =========================
# State-wise Heat Map
# =========================

st.markdown("---")
st.header("State-wise Heat Map (Age 5–17)")

state_data = (
    df.groupby("state")["demo_age_5_17"]
    .sum()
    .reset_index()
)

state_data["iso"] ="IND"
fig = px.choropleth(
    state_data,
    locations="iso",
    locationmode="ISO-3",
    color="demo_age_5_17",
    hover_name="state",
    color_continuous_scale="Reds",
    scope="asia",
    title="Youth Population Heat Map (Age 5–17)"
)

st.plotly_chart(fig, use_container_width=True)

st.write(df.columns)

st.header("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Districts", df["district"].nunique())
col2.metric("Total Population (5–17)", int(df["demo_age_5_17"].sum()))
col3.metric("Total Records", len(df))

st.header("Key Insight")

st.info(
    "Districts with higher youth population indicate future Aadhaar lifecycle stress "
    "due to increased biometric updates, address changes, and service dependency "
    "as this group transitions into the 5–17 age range."
)

# Load filtered data
df = pd.read_csv("mp_filtered_data.csv")
st.success("Data loaded successfully")

# Show data
st.write(df.head())

# Optional filters
selected_state = st.selectbox("Select State", df['state'].unique())
selected_age_group = st.slider("Select Age Group", 5, 17, (5,17))

filtered_df = df[(df['state'] == selected_state) & 
                 (df['demo_age_5_17'] >= selected_age_group[0]) & 
                 (df['demo_age_5_17'] <= selected_age_group[1])]

st.write(filtered_df)

# Bar chart
age_counts = filtered_df['demo_age_5_17'].value_counts()
st.bar_chart(age_counts)

# Pie chart
district_counts = filtered_df['district'].value_counts()
plt.figure(figsize=(10,10))
plt.pie(district_counts, labels=district_counts.index, autopct='%1.1f%%')
st.write("District-wise distribution")
st.pyplot(plt)

#trends analysis
st.markdown("---")
st.header("📈 Trend Analysis: Age Group 5–17 Over Time")

df['date'] = pd.to_datetime(df['date'])

trend_df = (
    df[df['state'] == 'Madhya Pradesh']
    .groupby('date')['demo_age_5_17']
    .sum()
    .reset_index()
)

st.line_chart(trend_df.set_index('date'))

#pattern discovery
st.markdown("---")
st.header("📊 Pattern: Districts with Consistently High Youth Population")

district_pattern = (
    df[df['state'] == 'Madhya Pradesh']
    .groupby('district')['demo_age_5_17']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(district_pattern)

#anomaly detection
st.markdown("---")
st.header("🚨 Anomaly Detection: Sudden Spikes in Youth Data")

mean_val = trend_df['demo_age_5_17'].mean()
std_val = trend_df['demo_age_5_17'].std()

anomalies = trend_df[
    trend_df['demo_age_5_17'] > mean_val + 2 * std_val
]

st.write("Detected Anomalies (Unusual Spikes)")
st.dataframe(anomalies)

