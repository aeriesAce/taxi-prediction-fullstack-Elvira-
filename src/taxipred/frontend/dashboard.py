from taxipred.frontend.app_layout.pages.layout import dashboard_pages
from taxipred.utils.helpers import button_colour
import streamlit as st

# def Main():
st.set_page_config(page_title="TaxiPrediction", layout="centered")
button_colour()
dashboard_pages()

# if __name__ == "__Main__":
#     Main()