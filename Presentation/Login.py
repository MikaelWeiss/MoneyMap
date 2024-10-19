import streamlit as st
from supabase import create_client, Client

# Initialize Supabase client
SUPABASE_URL = st.secrets.connections.supabase['SUPABASE_URL']
SUPABASE_KEY = st.secrets.connections.supabase['SUPABASE_KEY']
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize session state variables
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'session' not in st.session_state:
    st.session_state['session'] = None


def sign_out():
    supabase.auth.sign_out()
    st.session_state['user'] = None
    st.session_state['session'] = None
    st.success("Signed out successfully")


# Check if user is logged in
if st.session_state['user'] and st.session_state['session']:
    st.subheader("Manage Your Account")
    st.write(f"Logged in as {st.session_state['user'].email}")
    if st.button("Sign out"):
        sign_out()
else:
    tab1, tab2 = st.tabs(["Sign up", "Sign in"])

    with tab1:
        st.subheader("Sign up")
        lcol, rcol = st.columns(2)
        email = lcol.text_input(label="Email", key="signup_email")
        password = rcol.text_input(
            label="Password",
            placeholder="Min 6 characters",
            type="password",
            help="Password is encrypted",
            key="signup_password"
        )

        fname = lcol.text_input(
            label="First name",
            placeholder="Optional",
            key="signup_fname"
        )

        attribution = rcol.text_area(
            label="How did you hear about us?",
            placeholder="Optional",
            key="signup_attribution"
        )

        if st.button("Sign up", use_container_width=True, disabled=not email or not password):
            response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "fname": fname,
                        "attribution": attribution
                    }
                }
            })
            if response.user:
                st.success("Check your email to confirm your account")
            else:
                st.error("Sign up failed. Please try again.")

    with tab2:
        st.subheader("Sign in")
        lcol, rcol = st.columns(2)
        email = lcol.text_input(label="Email", key="signin_email")
        password = rcol.text_input(
            label="Password",
            placeholder="Min 6 characters",
            type="password",
            help="Password is encrypted",
            key="signin_password"
        )
        if st.button("Sign in", use_container_width=True, disabled=not email or not password):
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if response.user:
                st.session_state['user'] = response.user
                st.session_state['session'] = response.session
                # Set the session for the Supabase client
                # Only use session, no refresh_token
                supabase.auth.set_session(response.session)
                st.success("Signed in successfully")
            else:
                st.error("Sign in failed. Please check your credentials.")

# Example of inserting data using the user's session
if st.session_state['user']:
    st.subheader("Insert Data")
    data_input = st.text_input("Enter some data to insert")
    if st.button("Insert Data") and data_input:
        # Ensure the Supabase client uses the user's session
        supabase.auth.set_session(st.session_state['session'])
        # Insert data into a table (replace 'your_table' with your actual table name)
        # Adjust the data structure as needed
        data = {"column_name": data_input}
        response = supabase.table('your_table').insert(data).execute()
        if response.data:
            st.success("Data inserted successfully")
        else:
            st.error(f"Failed to insert data: {response.error}")
