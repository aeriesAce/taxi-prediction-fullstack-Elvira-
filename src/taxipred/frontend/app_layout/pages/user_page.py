import streamlit as st
import time
from taxipred.utils.helpers import read_api_endpoint, usd_to_sek, post_api_endpoint, predict_price
from taxipred.backend.charts import best_time_to_travel
API_URL_COND = read_api_endpoint("/conditions")
st.title("Beräkna taxipriser")

col1, col2 = st.columns([2, 2])
with col1:
    distance = st.number_input("Reslängd (km)", min_value=1.0, max_value=1000.0, step=1.0)
    passengers = st.number_input("Antal passagerare", min_value=1, max_value=4, value=1, step=1)
    day_of_week = st.selectbox("Dag", ["Veckodag", "Helg"])
    submitted = st.button("Räkna ut")

    with st.spinner("Räknar ut priset, ett ögonblick 🚖"):
        if submitted:
            time.sleep(1)
            payload = {
                "Trip_Distance_km": distance,
                "Passenger_Count": passengers,
                "Day_of_Week": day_of_week
            }

            response = predict_price(payload=payload).json()
            price_usd = response.get("predicted_price")
            price_sek = usd_to_sek(price_usd)
            st.session_state["base_price"] = price_sek

            st.success(f"Priset för resan blir: {price_sek:.2f} kr")


with col2:
        best_time_to_travel()
        
col_left, col_center, col_right = st.columns([3,3,1])
with col_left:
    st.markdown("❄️ Olika villkor som kan påverka priset.")
    time_of_day = st.selectbox("Tid på dygnet", ["Morgon", "Eftermiddag", "Kväll", "Natt"])
    weather = st.selectbox("Väder", ["Klart", "Regn", "Snö"], key = "weather")
    traffic = st.selectbox("Trafik", ["Låg", "Medium", "Hög"], key = "traffic")
    price_submit = st.button("Räkna med väder/trafik")

    with st.spinner("Räknar ut priset, ett ögonblick 🚖"):
        time.sleep(1)
        if price_submit:
            payload = {
                "Base_Fare": st.session_state["base_price"],
                "Time_of_Day": time_of_day,
                "Weather": weather,
                "Traffic_Conditions": traffic,
            }

            response = post_api_endpoint(payload, endpoint = API_URL_COND)
            new_price = response["price"]
            diff = new_price - st.session_state["base_price"]

            st.success(f"Nytt pris: {new_price:.2f} kr")
            st.info(f"Skillnad: {diff:+.2f} kr")

with col_center:
     with st.expander("Hur priset beräknas"):
        st.info("""
        **Prisberäkning:**
        - **Baspris per kilometer:** Slutpriset baseras på resans längd.
        - **Väder:** Dåligt väder kan öka priset eftersom resan tar längre tid.
        - **Tid på dygnet och trafik:** Vissa tider, t.ex. rusningstimmar kan ge små prisjusteringar.
    """)