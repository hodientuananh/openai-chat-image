import os
import streamlit as st
import base64
from PIL import Image
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Initialize conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

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
