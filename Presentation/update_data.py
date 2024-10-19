import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Initialize connection to Supabase
url = st.secrets.connections.supabase["SUPABASE_URL"]
key = st.secrets.connections.supabase["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# Fetch data from Supabase
response = supabase.table('user_financial_data').select('*').execute()
data = response.data

# Convert data to DataFrame
df = pd.DataFrame(data)

st.title('User Data')
st.caption('- - -')

data_money = st.data_editor(df, num_rows='dynamic')
