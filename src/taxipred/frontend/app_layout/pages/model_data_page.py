import httpx
import altair as alt
import streamlit as st
import pandas as pd
from taxipred.utils.helpers import read_api_endpoint

API_URL_MODEL = read_api_endpoint("/model/statistics")
API_URL_RESIDUALS = read_api_endpoint("/model/residuals")
st.header("Modellprestanda 📈")

# Hämta modellstatistik från API
with httpx.Client(timeout=10) as client:
    response = client.get(API_URL_MODEL)
    response.raise_for_status()
    stats = response.json()["stats"]

with httpx.Client(timeout=10) as client:
        response = client.get(f"{API_URL_RESIDUALS}?top_n=5")
        response.raise_for_status()
        residuals = response.json()["residuals"]

col1, col2, col3= st.columns(3)
col1.metric("MAE", f"{stats['mae']:.2f} kr")
col2.metric("RMSE", f"{stats['rmse']:.2f} kr")
col3.metric("R²", f"{stats['r2']:.2f}")

with st.expander("Hur man tolkar modellstatistiken"):
    st.markdown("""
    - **MAE (Mean Absolute Error):** Hur mycket modellen i genomsnitt avviker från verkliga priser.
    - **RMSE (Root Mean Squared Error):** Tar större hänsyn till stora avvikelser.
    - **R²:** Hur stor del av variationen i data som modellen förklarar (1 = perfekt, 0 = ingen förklaring).
    """)

# prediction vs real price
st.subheader("Prediktion vs Verkligt pris")
df_pred = pd.DataFrame({
    "Predicted": stats["predicted_prices"],
    "Actual": stats["actual_prices"]
})


line = alt.Chart(pd.DataFrame({
    'x': [df_pred["Actual"].min(), df_pred["Actual"].max()],
    'y': [df_pred["Actual"].min(), df_pred["Actual"].max()]
})).mark_line(color='red', strokeDash=[5,5]).encode(
    x='x',
    y='y'
)
df_pred["Residual"] = df_pred["Actual"] - df_pred["Predicted"]
scatter = alt.Chart(df_pred).mark_circle(size=60, opacity=0.6).encode(
    x=alt.X('Actual', title='Verkligt pris'),
    y=alt.Y('Predicted', title='Predikterat pris')
)
st.altair_chart(scatter + line, use_container_width=True)
with st.expander("Tolka scatterplott och referenslinje"):
    st.markdown("""
    - Punkterna representerar varje resa: x = verkligt pris, y = predikterat pris.
    - Den röda streckade linjen visar perfekt prediktion.
    - Punkter ovanför linjen betyder att modellen underskattade priset, under = överskattade.
    """)

st.subheader("Residualer (verkligt - predikterat)")
st.bar_chart(df_pred["Residual"])
df_pred["Residual"] = df_pred["Actual"] - df_pred["Predicted"]
scatter = alt.Chart(df_pred).mark_circle(size=60, opacity=0.6).encode(
    x=alt.X('Actual', title='Verkligt pris'),
    y=alt.Y('Predicted', title='Predikterat pris')
)

st.markdown("Största residualer")
st.write("Största negativa residualer (modell överskattade):")
st.dataframe(residuals["negative_residuals"])

st.write("Största positiva residualer (modell underskattade):")
st.dataframe(residuals["positive_residuals"])

    
st.write("Så hur ska det här tolkas? 💡")
st.info("""
        Residualer visar hur mycket modellen skiljer sig från verkliga värden.

        - En **negativ residual** betyder att modellen **förutsåg ett högre pris** än det faktiska.  
        ➜ Modellen överskattade priset.
        
        - En **positiv residual** betyder att modellen **förutsåg ett lägre pris** än det faktiska.  
        ➜ Modellen underskattade priset.

        Ju **mindre residualer**, desto mer träffsäker är modellen.  
        Stora residualer kan uppstå vid ovanliga kombinationer av faktorer, t.ex.:
        - mycket långa eller mycket korta resor,  
        - extrema trafikförhållanden eller väder,  
        - tider på dygnet där få resor finns i träningsdata.

        📊 Genom att analysera dessa kan vi förstå hur vi ska samla in data för att korrekt träna modellen.
        """)