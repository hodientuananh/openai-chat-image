import os
import bcrypt
import streamlit as st
import base64
from PIL import Image
from openai import OpenAI
from consts import OPENAI_API_KEY, USER_DB

# INITIALIZATION
client = OpenAI(
    api_key = OPENAI_API_KEY,
)
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
    st.session_state.logged_in = False
    
# FUNCTION
def verify_password(stored_password, provided_password):
    """Verify the hashed password."""
    return bcrypt.checkpw(provided_password.encode(), stored_password)

def login(username, password):
    """Check if the username and password are correct."""
    if username in USER_DB:
        stored_password = USER_DB[username]
        if verify_password(stored_password, password):
            return True
    return False
    
# LOGIN FORM
if not st.session_state.logged_in:
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        # Simple validation (replace with actual validation logic)
        if login(username, password):
            st.session_state.logged_in = True
            st.sidebar.success("Logged in successfully!")
        else:
            st.sidebar.error("Invalid username or password")
else:
    st.sidebar.success("You are logged in")

# ASK FOR IMAGE
if st.session_state.logged_in:
    st.title("Image Chatbot")
    st.write("This app uses OpenAI's GPT-4 to generate responses based on the image and text input.")
    
    # File uploader for image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    # Function to encode the image
    def encode_image(uploaded_file):
        return base64.b64encode(uploaded_file.getvalue()).decode("utf-8")

    # Display conversation history in the sidebar
    st.sidebar.header("Conversation History")

    # Conversation UI
    if uploaded_file is not None:
        # Encode the file content to base64
        base64_image = encode_image(uploaded_file)

        # Display the image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        # Input text area
        user_input = st.text_area("Enter your message:", "What is in this image?")

        if st.button("Send"):
            # Append user message to conversation history
            st.session_state.conversation_history.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_input,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            })

            # Generate response
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.conversation_history
            )

            # Append assistant response to conversation history
            st.session_state.conversation_history.append({
                "role": "assistant",
                "content": response.choices[0].message.content
            })

            # Display the response
            st.write(response.choices[0].message.content)
            
            # Save history chat
            for message in st.session_state.conversation_history[1:]:
                role = message["role"]
                content = message["content"]
                if role == "user":
                    st.sidebar.write(f"User: {content[0]['text']}")
                if role == "assistant":
                    st.sidebar.write(f"Assistant: {content}")
