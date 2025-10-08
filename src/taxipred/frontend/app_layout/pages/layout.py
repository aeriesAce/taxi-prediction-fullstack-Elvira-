import streamlit as st
import base64

def dashboard_pages():
    pages = {
        "Kund": [
            st.Page("app_layout/pages/user_page.py", title="Räkna ut priset för taxi resan")
        ],
        "Företag": [
            st.Page("app_layout/pages/company_page.py", title="Data för företaget"),
            st.Page("app_layout/pages/model_data_page.py", title="Modell data")
        ],
    }

    pg = st.navigation(pages)
    pg.run()