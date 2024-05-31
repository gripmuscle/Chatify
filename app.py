import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# Set page title and favicon
st.set_page_config(page_title="Chatify+", page_icon=":robot_face:")

# Log in to huggingface and grant authorization to huggingchat
EMAIL = "your email"
PASSWD = "your password"
cookie_path_dir = "./cookies/"
sign = Login(EMAIL, PASSWD)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

# Create your ChatBot
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

# Streamlit app layout
st.title("Chatify+")

# Get the available models
models = chatbot.get_available_llm_models()

# Model switching
selected_model = st.selectbox("Select a model", models)
model_index = models.index(selected_model)
chatbot.switch_llm(model_index)

# User input for the chatbot
user_input = st.text_input("You:", "Hello, how can I assist you?")

# Generate response when the user enters a message
if user_input:
    # Query the Hugging Chat API
    output = chatbot.query(user_input)

    # Display the model's response
    st.text_area("Bot:", value=output, height=200, max_chars=None, key=None)

# Start new conversation
if st.button("Start New Conversation"):
    chatbot.new_conversation(switch_to=True)

# Delete conversation
if st.button("Delete Conversation"):
    chatbot.delete_conversation()

# Run the Streamlit app
if __name__ == "__main__":
    st.write("")
