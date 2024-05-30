import streamlit as st
import requests

# Set page title and favicon
st.set_page_config(page_title="Multi-Model Chatbot", page_icon=":robot_face:")

# Define the API endpoint and headers
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": "Bearer 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"}

# Function to query the model API
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Streamlit app layout
st.title("Multi-Model Chatbot")

# User input for the chatbot
user_input = st.text_input("You:", "Hello, how can I assist you?")

# Generate response when the user enters a message
if user_input:
    # Query the model API
    output = query({
        "inputs": user_input,
    })
    
    # Display the model's response
    st.text_area("Bot:", value=output[0]['generated_text'], height=200, max_chars=None, key=None)

# Run the Streamlit app
if __name__ == "__main__":
    st.write("")
