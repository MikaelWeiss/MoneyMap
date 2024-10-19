# view_data.py

import streamlit as st
import pandas as pd
import numpy as np

st.title("Your Map to Success")
st.caption("Let's be real. Finances are tough. Don't worry, there's a map to financial freedom for all of us!")

showData = st.toggle("Show data", value=True)

if not showData:
    st.warning(
        """
    Oh no! Looks like you haven't added any data yet.
    Head over to the "Input Data" page to get started!

    (Trust me, it's worth it)
    """
    )

    st.write(
        """
    Don't believe me? Here's a sneak peak into what you're missing out on:
    """
    )

    st.caption("Soon to be added images of what it will look like")
else:
    st.write(
        """
Your financial path may be uphill, so keep your eye on the goal: *Financial freedom*
"""
    )
    chart_data = pd.DataFrame(np.array([[0, 2000, 100], [1, 2000, 200], [2, 2000, 300], [3, 2000, 400], [4, 2000, 500]]),
                              columns=['Months', 'Expenses', 'Current Savings'])

    st.line_chart(chart_data, x='Months')

    st.header("Years to Financial Freedom: 150 years")
    st.caption("""
    There are a lot of ways to define financial freedom, but here, we'll define it as having enough savings to cover your expenses, plus extra for emergencies, and of course, fun! Enough savings to last you the rest of your life.
             """)

    tab1, tab2, tab3, tab4 = st.tabs(["Savings", "Income", "Expenses", "Debt"])

    with tab1:
        st.write("Savings")
        st.write("This is where you can see your savings grow over time")
    with tab2:
        st.write("Income")
        st.write("This is where you can see your income grow over time")
    with tab3:
        st.write("Expenses")
        st.write("This is where you can see your expenses grow over time")
    with tab4:
        st.write("Debt")
        st.write("This is where you can see your debt shrink over time")
