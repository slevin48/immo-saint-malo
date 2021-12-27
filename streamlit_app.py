import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import folium_static
import folium
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import immo
import requests as rq

# search from API
@st.cache
def load_data(postcode):
    # json_data = immo.dvf_commune(postcode)
    r = rq.get('http://api.cquest.org/dvf?code_postal='+str(postcode))
    json_data = r.json()
    df = immo.parse_dvf2(json_data)
    df.date_mutation = pd.to_datetime(df.date_mutation).dt.date
    return df

st.sidebar.title("Enter search parameters")

postcode = st.sidebar.text_input("Postcode","35400")
st.sidebar.write('''
(For Paris: enter 750XX, 
with XX the arrondissement)
''')

# postcode = 35288
df = load_data(postcode)

price = st.sidebar.slider("Select a price range",0,1000000,(400000,600000))

since = st.sidebar.date_input("Search from",datetime.datetime.strptime('2014-01-01','%Y-%m-%d'))

df1 = df[(df.valeur_fonciere>price[0]) & (df.valeur_fonciere<price[1]) & (df.date_mutation>since)]

st.sidebar.write(str(len(df1))+" results")

fig, ax = plt.subplots()
ax.hist(df1.prixm2) 

st.sidebar.write(fig)

# Body

st.title("🏠 Immo Saint Malo")

if st.checkbox("Display results list",False):
    # streamlit doesn't render category dtypes
    st.write(df1.astype('object'))

st.markdown("**Data source:** [https://app.dvf.etalab.gouv.fr/](https://app.dvf.etalab.gouv.fr/)")

# if st.checkbox("Display map",True):
if st.checkbox("Display results map",True):
    map1 = immo.mapplot2(df1)
    folium_static(map1)
#     st.map(df1)