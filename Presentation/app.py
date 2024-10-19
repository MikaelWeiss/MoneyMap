import streamlit as st

login = st.Page(
    "pages/Login.py",
    title="Login",
    icon=":material/lock:",
)

input_data = st.Page(
    "pages/input_data.py",
    title="Input Data",
    icon=":material/edit:",
)

view_your_map = st.Page(
    "pages/view_your_map.py",
    title="View Your Map",
    icon=":material/map:",
)

update_data = st.Page(
    "pages/update_data.py",
    title="Update Data",
    icon=":material/update:",
)

pg = st.navigation({
    "Plan": [input_data, update_data],
    "Your Map": [view_your_map],
    "Your Account": [login]
})

pg.run()
