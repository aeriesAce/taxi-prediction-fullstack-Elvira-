import requests
import streamlit as st
from urllib.parse import urljoin
import httpx

# helper to fetch the api endpint
def read_api_endpoint(endpoint = "/", base_url = "http://127.0.0.1:8000"):
    return urljoin(base_url, f"/api/taxi/{endpoint.strip('/')}")

def post_api_endpoint(payload, endpoint="/", base_url="http://127.0.0.1:8000"):
    url = urljoin(base_url, endpoint)
    response = requests.post(url=url, json=payload)
    response.raise_for_status()
    return response.json()

# helper function to calculate the price
def predict_price(payload):
    API_URL = read_api_endpoint("predict/user")
    with httpx.Client(timeout=10) as client:
        response = client.post(API_URL, json=payload)
        response.raise_for_status()
        return response

# for ui
def button_colour():
    st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: #060606ff;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    
# converts between usd to sek
def usd_to_sek(convert):
    return convert * 9.38;

