# FUNCTION
import bcrypt
import streamlit as st

from env.consts import USER_DB

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
def login_form():
    if not st.session_state['logged_in']:
        st.sidebar.header("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            # Simple validation (replace with actual validation logic)
            if login(username, password):
                st.session_state['logged_in'] = True
                st.sidebar.success("Logged in successfully!")
            else:
                st.sidebar.error("Invalid username or password")
    else:
        st.sidebar.success("You are logged in")