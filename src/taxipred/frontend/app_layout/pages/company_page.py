import httpx
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from taxipred.utils.helpers import read_api_endpoint

API_URL_STAT = read_api_endpoint("/company/statistics")
st.header("Statistik för företaget")

with httpx.Client(timeout=10) as client:
    response = client.get(API_URL_STAT)
    response.raise_for_status()
    data = response.json()["stats"]
    
col1, col2, col3, col4 = st.columns(4)
col1.metric("Medianpris", f"{data['median_price']:.2f} kr")
col2.metric("Medelpris", f"{data['avg_price']:.2f} kr")
col3.metric("Pris per km", f"{data['avg_price_per_km']:.2f} kr/km")
col4.metric("Medianresa", f"{data['median_trip_distance_km']:.1f} km")

st.subheader("Populära tider på dygnet")
df_times = pd.DataFrame.from_dict(data["top_times_of_day"], orient="index", columns=["Antal resor"])
st.bar_chart(df_times)

st.subheader("Populära dagar")
df_days = pd.DataFrame.from_dict(data["top_days_of_week"], orient="index", columns=["Antal resor"])
st.bar_chart(df_days)