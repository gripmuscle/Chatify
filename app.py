import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# Set page title and favicon
st.set_page_config(page_title="Chatify+", page_icon=":robot_face:")

# Streamlit app layout
st.title("Chatify+")

# Sidebar for email, password input, and chat history
with st.sidebar:
    # User input for email and password
    email = st.text_input("Email:")
    password = st.text_input("Password:", type="password")

    # Check if email and password are provided
    if email and password:
        # Log in to huggingface and grant authorization to huggingchat
        cookie_path_dir = "./cookies/"
        sign = Login(email, password)
        cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

        # Create your ChatBot
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

        # Get the available models
        models = chatbot.get_available_llm_models()

        # Extract model names from the Model objects
        model_names = [model.name for model in models]

        # Model switching
        selected_model = st.selectbox("Select a model", model_names)
        model_index = model_names.index(selected_model)
        chatbot.switch_llm(model_index)

        # Display chat history
        st.subheader("Chat History")
        conversation_list = chatbot.get_conversation_list()
        for conversation in conversation_list:
            st.write(f"**{conversation.title}** (Author: {conversation.author})")

# Main chat interface
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
