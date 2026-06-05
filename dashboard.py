import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="IoT Spatial Traffic Analytics", layout="wide")
st.title("📊 Real-Time Spatial Traffic Analytics Dashboard")
st.subheader("TechwithGK   FT. Gulshan Kumar")

placeholder = st.empty()

while True:
    try:
        df = pd.read_csv("traffic_log.csv")
        with placeholder.container():
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric(label="Total Objects Logged (N)", value=len(df))
            kpi2.metric(label="Average Interaction Time (ms)", value=int(df["duration_ms"].mean()) if len(df)>0 else 0)
            kpi3.metric(label="Anomalies/Intrusions Detected 🚨", value=int(df["anomaly_flag"].sum()) if len(df)>0 else 0)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 📈 Time-Series Dashboard")
                if not df.empty: st.line_chart(df.set_index("timestamp")["duration_ms"])
            with col2:
                st.markdown("### 🕒 Hourly Density")
                if not df.empty:
                    hourly_counts = df.groupby("hour").size().reset_index(name="counts")
                    st.bar_chart(hourly_counts.set_index("hour")["counts"])
            st.dataframe(df.tail(10))
    except Exception as e:
        pass
    time.sleep(2)