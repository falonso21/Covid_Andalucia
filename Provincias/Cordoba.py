### Librerías necesarias
import warnings
warnings.filterwarnings("ignore")

import streamlit as st
from streamlit_folium import folium_static
from streamlit_echarts import st_pyecharts


from covid_functions import *

import plotly.graph_objects as go

def app():

    st.title('Covid-19 en Córdoba😷')
    st.markdown('La provincia cordobesa se trata, según los datos proporcionados por la Junta de Andalucía, de la cuarta más damnificada por el coronavirus en Andalucía. \
        Únicamente superada por Sevilla, Málaga y Granada. Resulta curiosa la escasez de datos y la baja incidencia en verano, siendo una de las provincias menos afectadas esos meses. Esto puede ser debido a las altas temperaturas alcanzadas en la provincia \
            en la época estival, además de que no es una zona especialmente turística en esa época del año.')
    st.markdown('## Mapa de los municipios con datos acumulados')

    url = "https://www.juntadeandalucia.es/institutodeestadisticaycartografia/intranet/admin/rest/v1.0/consulta/38666"
    lista_acumulados = ['Córdoba','Córdoba (distrito)','Córdoba Sur','Guadalquivir','Córdoba Norte']
    cordoba_df = json_to_df(url,lista_acumulados)
    cordoba_df = cordoba_df.fillna(0)
    plot_province_map('Córdoba', cordoba_df, 37.8, -4.7, 8)   

    st.markdown('## Tendencias y comparación')
    st.markdown('En la siguiente gráfica se muestra la evolución de los diferentes datos para la provincia de Córdoba. \
        Se añade también una línea que representa la media para dicho dato seleccionado. De manera extra, se da la opción de comparar los datos de Almería con los de cualquier otra provincia andaluza a seleccionar.') 
    st.markdown('Por último, añadir que el gráfico es interactivo por lo que permite: el estudio de tendencias en un rango temporal más o menos prolongado, obtener el para un momento puntual arrastrando el ratón sobre la gráfica, \
            hacer _zoom in_ y _zoom out_...')      
     


    ## Obtenemos los datos de hoy mediante una petición a la api
    Andalucia_df = scrapy_data()

    ## Datos de la comunidad    
    Córdoba =  Andalucia_df[Andalucia_df.Territorio == 'Córdoba']
    #Almería['Mes'] = [x.month for x in Almería.Fecha]
#
    options = ("Nuevos casos", "Hospitalizados","UCI",'Fallecidos')
    select_data1 = st.sidebar.radio(
        "¿Qué datos quieres ver?",
        options
    )
    options_province = ("No", "Almería","Cádiz", "Granada", "Huelva", "Jaén", "Málaga", "Sevilla")
    select_data2 = st.sidebar.radio(
        "¿Quieres comparar los datos con otra provincia?",
        options_province
    )
    
    time_line_plot(Andalucia_df, select_data1, 'Córdoba' , select_data2)
    st.markdown('## Últimos datos de la provincia')
    st.markdown('A continuación se presenta una tabla con los datos de los diez días mas recientes,\
        publicados por la [Junta de Andalucía](https://www.juntadeandalucia.es/institutodeestadisticaycartografia/badea/operaciones/consulta/anual/39409?CodOper=b3_2314&codConsulta=39409),\
        para la provincia cordobesa.')


    st.dataframe(Córdoba.head(10).reset_index(drop=True))

    About1 = st.sidebar.markdown('## 🤝 Sobre nosotros')

    About = st.sidebar.info('Somos dos amigos graduados en matemáticas por la Universidad de Cádiz. Posteriormente obtuvimos el Máster en Data Science & Big Data en Afi Escuela de Finanzas.')

    Contact = st.sidebar.markdown('## 📩 ¡Encuéntranos en LinkedIn!')

    Contact1 = st.sidebar.info('[Francisco Alonso Fernández](https://www.linkedin.com/in/franciscoalonsofernandez/) Data Scientist en [Future Space](https://www.futurespace.es/).')
    Contact2 = st.sidebar.info('[Javier Ángel Fernández](https://www.linkedin.com/in/javier-angel-fernandez/) Data Scientist en [IIC](https://www.iic.uam.es/).')