from taxipred.utils.helpers import read_api_endpoint
import matplotlib.pyplot as plt
import streamlit as st
import httpx
import pandas as pd
import seaborn as sns
import streamlit as st

API_URL = read_api_endpoint("/user/popular")
def best_time_to_travel():
    with httpx.Client(timeout=10) as client:
        response = client.get(API_URL)
        response.raise_for_status()
        data = response.json().get("popular_times", [])

    if not data:
        st.warning("Ingen data att visa.")
        return

    df = pd.DataFrame(data)

    time_map = {"Morning": "Morgon", "Afternoon": "Eftermiddag", "Evening": "Kväll", "Night": "Natt"}
    day_map = {"Weekday": "Veckodag", "Weekend": "Helg"}

    df["Time_of_Day"] = df["Time_of_Day"].map(time_map)
    df["Day_of_Week"] = df["Day_of_Week"].map(day_map)

    df_pivot = df.pivot(index="Time_of_Day", columns="Day_of_Week", values="count")

    st.markdown("Populära restider")
    st.info("Tips för när du bokar!\nHåll utkik efter rusningstider då priserna kan bli dyrare! 💸")
    st.bar_chart(df_pivot)


def modell_predict_histo():
    df = pd.DataFrame(taxi_data.price_stats)
    df["prediction_error"] = df["predicted_price"] - df["Trip_Price"]
    st.bar_chart(df["prediction_error"])
