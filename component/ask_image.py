import base64
import streamlit as st

from PIL import Image

# Function to encode the image
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode("utf-8")

# Conversation UI
def ask_image():
    if st.session_state['uploaded_file'] is not None:
        # Get the uploaded file
        uploaded_file = st.session_state['uploaded_file']
        # Get the OpenAI client
        client = st.session_state['client']
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