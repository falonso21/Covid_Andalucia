import Covid1
import Provincias.Almeria
import Provincias.Cadiz
import Provincias.Cordoba
import Provincias.Granada
import Provincias.Huelva
import Provincias.Sevilla
import Provincias.Malaga
import Provincias.Jaen


import streamlit as st
PAGES = {
    "Andalucía": Covid1,
    "Almería": Almeria,
    "Cádiz": Cadiz, 
    "Córdoba": Cordoba,
    "Granada": Granada,
    "Huelva": Huelva,
    "Jaén": Jaen,
    "Málaga": Malaga,
    "Sevilla": Sevilla
}
st.sidebar.title('Ir a')
selection = st.sidebar.selectbox("Seleccione una provincia o la comunidad en general:", list(PAGES.keys()))

#select_province = st.sidebar.selectbox(
#    "Elige una provincia",
#    ("Almería", "Cádiz","Córdoba", "Granada", "Huelva", "Jaén", "Málaga", "Sevilla")
#)

page = PAGES[selection]
page.app()