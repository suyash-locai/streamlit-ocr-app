import streamlit as st
import requests

st.title("FastAPI and Streamlit Integration")

# Send a request to the FastAPI backend
api_url = "https://ocr-poc.mofkrah.ai"
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    st.write(f"Response from FastAPI: {data}")
else:
    st.write(f"Error: Unable to fetch data from FastAPI. Status code: {response.status_code}")

