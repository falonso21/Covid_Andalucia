import Covid1
import Provincias.Almeria as Almeria
import Provincias.Cadiz as Cadiz
import Provincias.Cordoba as Cordoba
import Provincias.Granada as Granada
import Provincias.Huelva as Huelva
import Provincias.Sevilla as Sevilla
import Provincias.Malaga as Malaga
import Provincias.Jaen as Jaen


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