import streamlit as st
import requests

# Set page title and favicon
st.set_page_config(page_title="Chatify+", page_icon=":robot_face:")

# Define the API endpoints and headers for each model
models = {
    "Llama 3 8B": {
        "API_URL": "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct",
        "headers": {"Authorization": "Bearer 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"}
    },
    "Mixtral": {
        "API_URL": "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
        "headers": {"Authorization": "Bearer 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"}
    },
    "Llama 3 70B": {
        "API_URL": "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct",
        "headers": {"Authorization": "Bearer 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"}
    }
}

# Function to query the model API
def query(model_config, payload):
    response = requests.post(model_config['API_URL'], headers=model_config['headers'], json=payload)
    return response.json()

# Streamlit app layout
st.title("Chatify+")

# User input for the chatbot
user_input = st.text_input("You:", "Hello, how can I assist you?")

# Select the model
selected_model = st.selectbox("Select a model", list(models.keys()))

# Generate response when the user enters a message
if user_input:
    # Query the selected model API
    model_config = models[selected_model]
    output = query(model_config, {
        "inputs": user_input,
    })
    
    # Display the model's response
    st.text_area("Bot:", value=output[0]['generated_text'], height=200, max_chars=None, key=None)

# Run the Streamlit app
if __name__ == "__main__":
    st.write("")
