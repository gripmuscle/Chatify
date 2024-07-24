import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
from pymongo import MongoClient
import uuid

# Load secrets from the secrets.toml file
huggingface_token = st.secrets["default"]["huggingface_token"]
mongodb_connection_string = st.secrets["mongodb"]["connection_string"]
rhea_model_name = st.secrets["models"]["rhea_model_name"]
mixtral_model_name = st.secrets["models"]["mixtral_model_name"]
opencode_model_name = st.secrets["models"]["opencode_model_name"]
max_new_tokens = st.secrets["config"]["max_new_tokens"]

# Set page title and favicon
st.set_page_config(page_title="Chatify+", page_icon=":robot_face:")

# Streamlit app layout
st.title("Chatify+ :robot_face:")
st.write("Welcome to Chatify+, your personal AI-powered chat assistant!")

# Function to load conversation history from MongoDB
def load_conversation_history(collection, chat_id):
    history = collection.find_one({"chat_id": chat_id})
    return history["messages"] if history else []

# Function to save conversation history to MongoDB
def save_conversation_history(collection, chat_id, history):
    collection.update_one({"chat_id": chat_id}, {"$set": {"messages": history}}, upsert=True)

# Function to get all chat IDs from MongoDB
def get_all_chat_ids(collection):
    return [doc["chat_id"] for doc in collection.find({}) if "chat_id" in doc]

# Function to delete a conversation from MongoDB
def delete_conversation(collection, chat_id):
    collection.delete_one({"chat_id": chat_id})

# Sidebar for email, password input, and chat history
with st.sidebar:
    st.header("Login")
    email = st.text_input("Email:")
    password = st.text_input("Password:", type="password")

    if email and password:
        # Log in to HuggingFace and grant authorization to HuggingChat
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

# Main chat interface
if 'chatbot' in locals():
    # MongoDB connection
    client = MongoClient(mongodb_connection_string)
    db = client.Chatify
    collection = db.conversation_history

    # Initialize the conversation history
    chat_id = st.session_state.get("chat_id", str(uuid.uuid4()))
    conversation_history = load_conversation_history(collection, chat_id)

    # Display the conversation history in the sidebar
    st.sidebar.subheader("Conversation History")
    chat_ids = get_all_chat_ids(collection)
    selected_chat_id = st.sidebar.selectbox("Select a chat", chat_ids, key="selected_chat_id")

    if selected_chat_id:
        selected_chat_history = load_conversation_history(collection, selected_chat_id)
        st.subheader(f"Conversation with {selected_chat_id}")
        for i, message in enumerate(selected_chat_history):
            if message.startswith("You:"):
                st.text_area(f"You:", value=message.split(": ", 1)[1], height=75, key=f"user_message_{i}", disabled=True)
            else:
                st.text_area(f"Bot:", value=message.split(": ", 1)[1], height=75, key=f"bot_message_{i}", disabled=True)

    # User input for the chatbot
    user_input = st.text_input("You:", key="user_input")

    if user_input:
        # Append the user's message to the history
        conversation_history.append(f"You: {user_input}")

        # Query the Hugging Chat API
        output = chatbot.query(user_input)

        # Append the bot's response to the history
        conversation_history.append(f"Bot: {output}")

        # Save the conversation history
        save_conversation_history(collection, chat_id, conversation_history)

        # Display the model's response
        st.text_area("Bot:", value=output, height=200, max_chars=None, key="bot_response", disabled=True)

    # Allow user to name the conversation
    chat_name = st.text_input("Name this conversation:", key="chat_name")

    # Start new conversation
    if st.button("Start New Conversation"):
        if chat_name:
            chat_id = chat_name
        else:
            chat_id = str(uuid.uuid4())
        st.session_state["chat_id"] = chat_id
        chatbot.new_conversation(switch_to=True)
        conversation_history = []  # Reset the conversation history
        save_conversation_history(collection, chat_id, conversation_history)

    # Delete conversation
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Delete Chat"):
            delete_conversation(collection, selected_chat_id)
            st.experimental_rerun()

    with col2:
        user_input_bottom = st.text_input("", key="user_input_bottom", label_visibility="collapsed")
        if user_input_bottom:
            # Append the user's message to the history
            conversation_history.append(f"You: {user_input_bottom}")

            # Query the Hugging Chat API
            output_bottom = chatbot.query(user_input_bottom)

            # Append the bot's response to the history
            conversation_history.append(f"Bot: {output_bottom}")

            # Save the conversation history
            save_conversation_history(collection, chat_id, conversation_history)

            # Display the model's response
            st.text_area("Bot:", value=output_bottom, height=200, max_chars=None, key="bot_response_bottom", disabled=True)

# Run the Streamlit app
if __name__ == "__main__":
    st.write("")
