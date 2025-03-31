import streamlit as st
import requests
import io
from PIL import Image
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Correct Hugging Face Inference API endpoint
API_URL = "https://api-inference.huggingface.co/models/openfree/flux-chatgpt-ghibli-lora"
headers = {"Authorization": f"Bearer {API_KEY}"}

# Function to send request to Hugging Face API
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)

    # Debugging: Print API response status and content type
    print("Status Code:", response.status_code)
    print("Content Type:", response.headers.get("Content-Type"))

    # If the API returns JSON, it's likely an error
    if "application/json" in response.headers.get("Content-Type", ""):
        error_response = response.json()
        print("Error Response:", error_response)
        return None  # Return None if an error occurs

    return response.content  # Return image bytes if valid

# Streamlit UI
st.title("AI Image Generator")
st.write("Enter a description to generate an image:")

# Get user input
description = st.text_input("Description")

if st.button("Generate Image"):
    if description:
        with st.spinner('Generating image...'):
            image_bytes = query({"inputs": description})

            if image_bytes:  # Ensure the response is valid
                try:
                    image = Image.open(io.BytesIO(image_bytes))
                    st.image(image, caption=description)
                except Exception as e:
                    st.error(f"Failed to generate image: {e}")
            else:
                st.error("The API did not return a valid image. Check API Key and parameters.")
    else:
        st.warning("Please enter a description.")

# Add a footer
st.markdown("---")
st.markdown("Made by Sakshi Ambavade")
