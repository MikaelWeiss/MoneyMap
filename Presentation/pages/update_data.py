import streamlit as st
import pandas as pd
st.title('User Data')
st.caption('- - -')


df = pd.DataFrame(columns=['Month','user_income','User-saving-APY', 'user-savings','user-debt','user-debt-intrist'])
data_money = ({
  'Month': st.column_config.NumberColumn('Age (years)', min_value=0, max_value=122),
  'user_income': st.column_config.NumberColumn('Age (years)', min_value=0, max_value=122),
  'User-saving-APY': st.column_config.NumberColumn('Age (years)', min_value=0, max_value=122),
  'user-savings': st.column_config.NumberColumn('Age (years)', min_value=0, max_value=122),
  'user-debt': st.column_config.NumberColumn('Age (years)', min_value=0, max_value=122),
  'user-debt-intrist': st.column_config.NumberColumn('Age (years)', min_value=0, max_value=122),
})
data_money = st.data_editor(df, num_rows = 'dynamic')

