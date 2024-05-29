import streamlit as st
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

# Function to initialize Rhea 72B pipeline
@st.cache_resource
def get_rhea_pipeline():
    return pipeline("text-generation", model="davidkim205/Rhea-72b-v0.5")

# Function to load Rhea 72B model and tokenizer directly
@st.cache_resource
def get_rhea_model():
    model = AutoModelForCausalLM.from_pretrained("davidkim205/Rhea-72b-v0.5")
    tokenizer = AutoTokenizer.from_pretrained("davidkim205/Rhea-72b-v0.5")
    return model, tokenizer

# Function to initialize Mixtral 8x22B pipeline
@st.cache_resource
def get_mixtral_pipeline():
    return pipeline("text-generation", model="mistralai/Mixtral-8x22B-Instruct-v0.1")

# Function to load Mixtral 8x22B model and tokenizer directly
@st.cache_resource
def get_mixtral_model():
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mixtral-8x22B-Instruct-v0.1")
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mixtral-8x22B-Instruct-v0.1")
    return model, tokenizer

# Function to load OpenCode 34B model and tokenizer
@st.cache_resource
def get_open_code_model():
    return AutoModelForCausalLM.from_pretrained("m-a-p/OpenCodeInterpreter-DS-33B"), AutoTokenizer.from_pretrained("m-a-p/OpenCodeInterpreter-DS-33B")

# Streamlit app main function
def main():
    st.title("Chatbot Interface")

    # Model selection
    model_options = {
        "Rhea 72B (Pipeline)": "rhea_pipeline",
        "Rhea 72B (Direct)": "rhea_direct",
        "Mixtral 8x22B (Pipeline)": "mixtral_pipeline",
        "Mixtral 8x22B (Direct)": "mixtral_direct",
        "OpenCode 34B (Pipeline)": "open_code_pipeline",
        "OpenCode 34B (Direct)": "open_code_direct",
    }
    model_name = st.selectbox("Select Model", list(model_options.keys()))

    # Chat interface
    st.subheader("Chat Interface")
    user_input = st.text_input("You:")
    if st.button("Send"):
        response = inference(model_name, user_input)
        st.text_area("Chatbot:", value=response, height=200)

@st.cache_data
def inference(model_name, user_input):
    model_options = {
        "Rhea 72B (Pipeline)": "rhea_pipeline",
        "Rhea 72B (Direct)": "rhea_direct",
        "Mixtral 8x22B (Pipeline)": "mixtral_pipeline",
        "Mixtral 8x22B (Direct)": "mixtral_direct",
        "OpenCode 34B (Pipeline)": "open_code_pipeline",
        "OpenCode 34B (Direct)": "open_code_direct",
    }
    response = ""
    if model_options[model_name] == "rhea_pipeline":
        response = get_rhea_pipeline()(user_input, max_length=50, do_sample=True)[0]['generated_text']
    elif model_options[model_name] == "rhea_direct":
        model, tokenizer = get_rhea_model()
        inputs = tokenizer(user_input, return_tensors="pt")
        output = model.generate(**inputs)
        response = tokenizer.decode(output[0], skip_special_tokens=True)
    elif model_options[model_name] == "mixtral_pipeline":
        response = get_mixtral_pipeline()(user_input, max_length=50, do_sample=True)[0]['generated_text']
    elif model_options[model_name] == "mixtral_direct":
        model, tokenizer = get_mixtral_model()
        inputs = tokenizer(user_input, return_tensors="pt")
        output = model.generate(**inputs)
        response = tokenizer.decode(output[0], skip_special_tokens=True)
    else:  # OpenCode pipeline and direct
        model, tokenizer = get_open_code_model()
        inputs = tokenizer(user_input, return_tensors="pt")
        output = model.generate(**inputs)
        response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

if __name__ == "__main__":
    main()
