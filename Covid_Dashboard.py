import Covid1
import Almeria
import Cadiz
import Cordoba
import Granada
import Huelva
import Sevilla
import Malaga
import Jaen


import streamlit as st
PAGES = {
    "Andalucía": Covid1,
    "Almería": Almeria,
    "Cádiz": Cadiz, 
    "Córdoba": Cordoba,
    "Granada": Granada,
    'Huelva': Huelva,
    'Sevilla': Sevilla,
    'Jaén': Jaen,
    'Málaga': Malaga
}
st.sidebar.title('Ir a')
selection = st.sidebar.selectbox("Seleccione una provincia o la comunidad en general:", list(PAGES.keys()))

#select_province = st.sidebar.selectbox(
#    "Elige una provincia",
#    ("Almería", "Cádiz","Córdoba", "Granada", "Huelva", "Jaén", "Málaga", "Sevilla")
#)

page = PAGES[selection]
page.app()