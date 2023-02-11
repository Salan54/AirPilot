# Streamlit - First steps
import pandas as pd
import streamlit as st
import sqlite3

# Page wide
st.set_page_config(layout="wide")

# Fonctions
@st.cache_data
def load_data():
    # Read sqlite query results into a pandas DataFrame
    # con = sqlite3.connect("data/AirPilotUtilities.db")
    con = sqlite3.connect("AirPilotUtilities.db")
    df = pd.read_sql_query("SELECT * FROM CARDS", con)
    return df

def cvzPer1000ft(VZinit_MaxRate, VZCeiling_MaxRate, ClimbCeilingCalculation):
    return (VZinit_MaxRate - VZCeiling_MaxRate) / (ClimbCeilingCalculation / 1000)

def appLdg5(AppConsumption60_55):
    return AppConsumption60_55 * 5 / 60

def appLdg10(AppConsumption60_55):
    return AppConsumption60_55 * 10 / 60

def appLdg15(AppConsumption60_55):
    return AppConsumption60_55 * 15 / 60

# Load data
df = load_data()

# Layout
st.write("""
# Simple Air Pilot mockup

""")
st.sidebar.header("Airplane choice")

brands = df['SINGLE ENGINE MANUFACTURER'].unique()
brand = st.sidebar.selectbox("Brand", brands)

models = df[df['SINGLE ENGINE MANUFACTURER'] == brand]['TYPE']
model = st.sidebar.selectbox("Model", models)

choices = f"**Brand:** :blue[{brand}] **Model:** :blue[{model}]"

st.markdown(choices)
# st.markdown('Streamlit is **_really_ cool**.')
# st.markdown("This text is :red[colored red], and this is **:blue[colored]** and bold.")
# st.markdown(":green[$\sqrt{x^2+y^2}=1$] is a Pythagorean identity. :pencil:")

dfSelected = df.loc[(df['SINGLE ENGINE MANUFACTURER'] == brand) & (df['TYPE'] == model)]
# Boolean to resize the dataframe, stored as a session state variable
st.checkbox("Use container width", value=False, key="use_container_width")
# Workaround: mixed types int and str => Source: https://github.com/streamlit/streamlit/issues/4094 (add .astype(str) to convert all values to str)
df2 = dfSelected.reset_index(drop=True).squeeze().astype(str)
st.dataframe(df2, use_container_width=st.session_state.use_container_width)
cvz1000 = cvzPer1000ft(dfSelected['VZ INIT - MAX RATE'], dfSelected['VZ CEILING - MAX RATE'], dfSelected['CLIMB CEILING CALCULATION'])
st.write('CVZ / 1000 ft : ',cvz1000.values[0])
appLdg5V = appLdg5(dfSelected['APP CONSUMPTION - 60% / 55%'])
st.write('APP+LDG 5     : ', appLdg5V.values[0])
appLdg10V = appLdg10(dfSelected['APP CONSUMPTION - 60% / 55%'])
st.write('APP+LDG 10    : ', appLdg10V.values[0])
appLdg15V = appLdg15(dfSelected['APP CONSUMPTION - 60% / 55%'])
st.write('APP+LDG 15    : ', appLdg15V.values[0])
