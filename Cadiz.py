### Librerías necesarias
import warnings
warnings.filterwarnings("ignore")

import streamlit as st
from streamlit_folium import folium_static
from streamlit_echarts import st_pyecharts

from covid_functions import *

import plotly.graph_objects as go

def app():

    st.title('Covid-19 en Cádiz😷')
    st.markdown('La provincia gaditana se trata, según los datos proporcionados por la Junta de Andalucía, de la cuarta más damnificada por el coronavirus en Andalucía. \
        Únicamente Sevilla, Granada y Málaga presentan peores datos absolutos. Es remarcable que junto con la capital, Sevilla, y otras provincias costeras como Málaga o Almería, fue de las primeras \
            en acusar la llegada de la segunda ola. Esto puede deberse al turismo nacional que a consecuencia del Covid19 ha decidido veranear en las costas andaluzas.')         
    st.markdown('## Tendencias y comparación')
    st.markdown('En la siguiente gráfica se muestra la evolución de los diferentes datos para la provincia de Cádiz. \
        Se añade también una línea que representa la media para dicho dato seleccionado. De manera extra, se da la opción de comparar los datos de Almería con los de cualquier otra provincia andaluza a seleccionar.') 
    st.markdown('Por último, añadir que el gráfico es interactivo por lo que permite: el estudio de tendencias en un rango temporal más o menos prolongado, obtener el para un momento puntual arrastrando el ratón sobre la gráfica, \
            hacer _zoom in_ y _zoom out_...')      


    ## Obtenemos los datos de hoy mediante una petición a la api
    Andalucia_df = scrapy_data()

    ## Datos de la comunidad    
    Cádiz =  Andalucia_df[Andalucia_df.Territorio == 'Cádiz']
    #Almería['Mes'] = [x.month for x in Almería.Fecha]
#
    options = ("Nuevos casos", "Hospitalizados","UCI",'Fallecidos')
    select_data1 = st.sidebar.radio(
        "¿Qué datos quieres ver?",
        options
    )
    options_province = ("No", "Almería","Córdoba", "Granada", "Huelva", "Jaén", "Málaga", "Sevilla")
    select_data2 = st.sidebar.radio(
        "¿Quieres comparar los datos con otra provincia?",
        options_province
    )
    
    time_line_plot(Andalucia_df, select_data1, 'Cádiz' , select_data2)
    st.markdown('## Últimos datos de la provincia')
    st.markdown('A continuación se presenta una tabla con los datos de los diez días mas recientes,\
        publicados por la [Junta de Andalucía](https://www.juntadeandalucia.es/institutodeestadisticaycartografia/badea/operaciones/consulta/anual/39409?CodOper=b3_2314&codConsulta=39409),\
        para la provincia gaditana.')


    st.dataframe(Cádiz.head(10).reset_index(drop=True))

    About1 = st.sidebar.markdown('## 🤝 Sobre nosotros')

    About = st.sidebar.info('Somos dos amigos graduados en matemáticas por la Universidad de Cádiz. Posteriormente obtuvimos el Máster en Data Science & Big Data en Afi Escuela de Finanzas.')

    Contact = st.sidebar.markdown('## 📩 ¡Encuéntranos en LinkedIn!')

    Contact1 = st.sidebar.info('[Francisco Alonso Fernández](https://www.linkedin.com/in/franciscoalonsofernandez/) Data Scientist en [Future Space](https://www.futurespace.es/).')
    Contact2 = st.sidebar.info('[Javier Ángel Fernández](https://www.linkedin.com/in/javier-angel-fernandez/) Data Scientist en [IIC](https://www.iic.uam.es/).')