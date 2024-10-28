import streamlit as st
import requests
import random

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;} /* Hides the hamburger menu */
    footer {visibility: hidden;} /* Hides the footer */
    .css-2trqyj {visibility: hidden;} /* Hides the GitHub "Fork" button */
    .css-1lsmgbg {visibility: hidden;} /* Hides the GitHub user icon at the bottom */
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Hardcoded users for demo purposes
USER_DATA = {
    "test@mail.com": "test123",
    "admin": "admin123"
}


# Function to authenticate user
def authenticate(username, password):
    return username in USER_DATA and USER_DATA[username] == password


# Initialize session state for login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Display login form if not authenticated
if not st.session_state.authenticated:
    st.title("Login to Access the OCR Demo")

    # Input fields for login
    username = st.text_input("Username or Email")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.success("Successfully logged in!")
            st.rerun()
        else:
            st.error("Invalid username or password. Please try again.")
else:
    # Demo app accessible only after login
    VALID_API_KEYS = [
        '187a4438-c0f2-4ac9-bbe1-e588168889ef',
        '6949f296-4a0d-4722-a57d-a4fd7c221316',
        '20ccb153-b205-47a1-a994-fa22e597078f',
        'd1c4384c-9498-4a1d-9ac0-c716a78533d0',
        'd2573460-7d91-4137-a505-ee6cffdd6d00',
        '848a4459-f35f-4e14-9530-4b93f95320fb'
    ]


    def get_random_api_key():
        return random.choice(VALID_API_KEYS)


    st.title("OCR Demo")
    st.write("")
    st.write("")

    with open("README.md", "r") as file:
        readme_text = file.read()

    # Display the README.md content in the Streamlit app
    st.markdown(readme_text, unsafe_allow_html=True)

    st.write("")
    st.write("")

    st.header('API Playground')
    st.write("")

    # api_key = st.text_input("API Key (auto-generated)", value=get_random_api_key())
    api_key = st.text_input("API Key")

    st.write("")

    # File uploader UI
    st.subheader("Upload file for the character recognition (PNG/JPG)")
    uploaded_file = st.file_uploader("Upload File")

    if uploaded_file is not None:
        # Convert the uploaded file to bytes
        files = {'file': (uploaded_file.name, uploaded_file.getvalue())}

        # Make a POST request to FastAPI with the uploaded file
        api_url = "https://ocr-poc.mofkrah.ai/arabic-ocr/"
        headers = {"x-api-key": api_key}
        response = requests.post(api_url, files=files, headers=headers)

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
    st.subheader("Submit list of uploaded (in S3) file names for the bulk character recognition (PNG/JPG)")

    # Input list of strings in Streamlit using the textarea
    string_input = st.text_area("Enter S3 object keys (one per line)", "")
    string_list = string_input.splitlines()

    if st.button("Submit Strings"):
        if string_list:
            headers = {"x-api-key": api_key}
            api_url = "https://ocr-poc.mofkrah.ai/arabic-ocr/batch"
            response = requests.post(api_url, json=string_list, headers=headers)

            if response.status_code == 200:
                st.json(response.json())
            else:
                st.error(f"Error: Unable to process strings. Status code: {response.status_code}")
        else:
            st.error("Please enter at least one string.")

    st.write("")
    st.write("")

    # Section 3: Get Batch Job Status UI
    st.subheader("Check Batch Job Status")

    # Input field for job_id
    job_id = st.text_input("Enter Job ID")
    if st.button("Check Job Status"):
        if job_id:
            headers = {"x-api-key": api_key}
            api_url = f"https://ocr-poc.mofkrah.ai/ocr-result/batch/{job_id}"
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                st.success("Job status retrieved successfully!")
                st.json(response.json())
            else:
                st.error(f"Error: Unable to fetch job status. Status code: {response.status_code}")
        else:
            st.error("Please enter a valid Job ID.")
