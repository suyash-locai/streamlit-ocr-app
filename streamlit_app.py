import streamlit as st
import requests

st.title("File Upload to FastAPI")

# File uploader UI
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # Convert the uploaded file to bytes
    files = {'file': (uploaded_file.name, uploaded_file.getvalue())}

    # Make a POST request to FastAPI with the uploaded file
    api_url = "https://ocr-poc.mofkrah.ai/arabic-ocr/"
    response = requests.post(api_url, files=files)

    if response.status_code == 200:
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        st.json(response.json())
    else:
        st.error(f"Error: Unable to upload file. Status code: {response.status_code}")


