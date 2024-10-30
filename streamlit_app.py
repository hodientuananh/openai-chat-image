import streamlit as st
import streamlit as st

from openai import OpenAI
from env.consts import OPENAI_API_KEY
from openai import OpenAI
from component.login import login_form
from component.ask_image import ask_image

# INITIALIZATION
## Init global variables
if 'client' not in st.session_state:
    st.session_state['client'] = OpenAI(
        api_key = OPENAI_API_KEY,
    )
    
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []
    
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None
    
## Init login form function
login_form()

# ASK FOR IMAGE
if st.session_state['logged_in']:
    st.title("Image Chatbot")
    st.write("This app uses OpenAI's GPT-4 to generate responses based on the image and text input.")
    
    # File uploader for image
    st.session_state['uploaded_file'] = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    # Init conversation history function
    ask_image()
    