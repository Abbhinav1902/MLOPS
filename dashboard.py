
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

# Connect to SQLite logs
conn = sqlite3.connect("logs.db")
df = pd.read_sql_query("SELECT * FROM logs", conn)

st.title("Iris Prediction Dashboard")

st.metric("Total Predictions", len(df))

if not df.empty:
    # Distribution of predictions
    dist = df["prediction"].value_counts().reset_index()
    dist.columns = ["Prediction", "Count"]
    fig = px.bar(dist, x="Prediction", y="Count", title="Prediction Distribution")
    st.plotly_chart(fig)

    # Show recent logs
    st.subheader("Recent Predictions")
    st.dataframe(df.tail(10))
else:
    st.warning("No predictions logged yet.")
