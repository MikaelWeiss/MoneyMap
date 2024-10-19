import streamlit as st

home = st.Page(
    "app.py",
    title="Home",
    icon=":material/home:",
)

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
    "Your Account": [login],
    "Plan": [input_data, update_data],
    "Your Map": [view_your_map]
})

pg.run()
