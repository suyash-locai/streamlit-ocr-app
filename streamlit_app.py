import streamlit as st
import requests

st.title("OCR Demo")
st.write("")
st.write("")

# File uploader UI
st.header("Upload file for the character recognition (PNG/JPG)")
uploaded_file = st.file_uploader("Upload File")

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


st.write("")
st.write("")
st.write("")
st.write("")


# Section 2: String List Submission UI
st.header("Submit list of uploaded (in S3) file names for the bulk character recognition (PNG/JPG)")

# Input list of strings in Streamlit using the textarea
string_input = st.text_area("Enter S3 object keys (one per line)", "")
string_list = string_input.splitlines()

if st.button("Submit Strings"):
    if string_list:
        api_url = "https://ocr-poc.mofkrah.ai/arabic-ocr/batch"
        response = requests.post(api_url, json=string_list)

        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error(f"Error: Unable to process strings. Status code: {response.status_code}")
    else:
        st.error("Please enter at least one string.")

# Add vertical space
st.write("")
st.write("")

# Section 3: Get Batch Job Status UI
st.header("Check Batch Job Status")

# Input field for job_id
job_id = st.text_input("Enter Job ID")
if st.button("Check Job Status"):
    if job_id:
        # Make a GET request to FastAPI with the job_id parameter
        api_url = f"https://ocr-poc.mofkrah.ai/ocr-result/batch/{job_id}"
        response = requests.get(api_url)

        if response.status_code == 200:
            st.success("Job status retrieved successfully!")
            st.json(response.json())
        else:
            st.error(f"Error: Unable to fetch job status. Status code: {response.status_code}")
    else:
        st.error("Please enter a valid Job ID.")


