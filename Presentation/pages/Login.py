# Login

import streamlit as st
from st_supabase_connection import SupabaseConnection

conn = st.connection("supabase", type=SupabaseConnection)

# Confirm email determines if users need to confirm their email address after signing up.
# If Confirm email is enabled, a user is returned but session is null.
# If Confirm email is disabled, both a user and a session are returned.

session = conn.auth.get_session()
user = conn.auth.get_user()

if user and session:
    st.subheader("Manage Your Account")
    st.write(f"Logged in as {user.email}")
    st.button("Sign out", on_click=conn.auth.sign_out)
elif user and not session:
    st.subheader("Confirm your email address")
    st.write(
        f"Please check your email at {user.email} to confirm your account.")
else:
    tab1, tab2 = st.tabs(["Sign up", "Sign in"])

    with tab1:
        is_OTP = False
        if is_OTP:
            st.subheader("Sign up with OTP")
            email = st.text_input(label="Enter your email ID")
            conn.auth.sign_in_with_otp(dict(email=email))
            token = st.text_input("Enter OTP", type="password")
            conn.auth.verify_otp(
                dict(type="magiclink", email=email, token=token))
        else:
            st.subheader("Sign up")
            lcol, rcol = st.columns(2)
            email = lcol.text_input(label="Email")
            password = rcol.text_input(
                label="Password",
                placeholder="Min 6 characters",
                type="password",
                help="Password is encrypted",
            )

            fname = lcol.text_input(
                label="First name",
                placeholder="Optional",
            )

            attribution = rcol.text_area(
                label="How did you hear about us?",
                placeholder="Optional",
            )

            if st.button("Sign up", use_container_width=True, disabled=not email or not password):
                conn.auth.sign_up(
                    dict(email=email, password=password, fname=fname, attribution=attribution))
                st.success("Check your email to confirm your account")
    with tab2:
        lcol, rcol = st.columns(2)
        email = lcol.text_input(label="Enter your email ID")
        password = rcol.text_input(
            label="Enter your password",
            placeholder="Min 6 characters",
            type="password",
            help="Password is encrypted",
        )
        if st.button("Sign in", use_container_width=True, disabled=not email or not password):
            conn.auth.sign_in(dict(email=email, password=password))
            st.success("Signed in successfully")
