# Streamlit - First steps
import pandas as pd
import streamlit as st
import sqlite3

# Layout
st.write("""
# Simple Air Pilot mockup

""")
st.sidebar.header("Airplane choice")

# Read sqlite query results into a pandas DataFrame
# con = sqlite3.connect("data/AirPilotUtilities.db")
con = sqlite3.connect("AirPilotUtilities.db")
df = pd.read_sql_query("SELECT * FROM CARDS", con)

brands = df['SINGLE ENGINE MANUFACTURER'].unique()
brand = st.sidebar.selectbox("Brand", brands)

models = df[df['SINGLE ENGINE MANUFACTURER'] == brand]['TYPE']
model = st.sidebar.selectbox("Model", models)

choices = f"**Brand:** :blue[{brand}] **Model:** :blue[{model}]"

st.markdown(choices)
# st.markdown('Streamlit is **_really_ cool**.')
# st.markdown("This text is :red[colored red], and this is **:blue[colored]** and bold.")
# st.markdown(":green[$\sqrt{x^2+y^2}=1$] is a Pythagorean identity. :pencil:")
