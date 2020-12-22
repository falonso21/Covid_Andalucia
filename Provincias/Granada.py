### Librerías necesarias
import warnings
warnings.filterwarnings("ignore")

import streamlit as st
from streamlit_folium import folium_static
from streamlit_echarts import st_pyecharts

from covid_functions import *

import plotly.graph_objects as go

def app():

    st.title('Covid-19 en Granada😷')
    st.markdown('La provincia granadina se trata, según los datos proporcionados por la Junta de Andalucía, de la segunda más damnificada por el coronavirus en Andalucía, solo por detrás de la capital Sevilla. \
        De hecho, a lo largo de los meses ha presentado datos muy similares a Sevilla, con la diferencia de que la capital acusó antes la llegada de la segunda ola. También resulta curioso que \
            Málaga superaba en casos a Granada durante la primera etapa de la pandemia, pero en esta segunda ola la provincia de la Costa del Sol parece haberse estabilizado.')
    st.markdown('## Mapa de los municipios con datos acumulados')
    st.markdown('En el siguiente mapa vemos los datos de la provincia de Granada a nivel municipal que provee la [Junta de Andalucía](https://www.juntadeandalucia.es/institutodeestadisticaycartografia/badea/informe/anual?CodOper=b3_2314&idNode=42348).\
         Es importante recalcar que estos son datos acumulados desde el inicio de la pandemia.')
    url = "https://www.juntadeandalucia.es/institutodeestadisticaycartografia/intranet/admin/rest/v1.0/consulta/38667"
    lista_acumulados = ['Granada','Granada Sur','Granada (distrito)','Metropolitano de Granada','Granada Nordeste']
    granada_df = json_to_df(url,lista_acumulados)
    granada_df = granada_df.fillna(0)
    plot_province_map('Granada', granada_df, 37.1, -3.6, 8)      
    st.markdown('## Tendencias y comparación')
    st.markdown('En la siguiente gráfica se muestra la evolución de los diferentes datos para la provincia de Granada. \
        Se añade también una línea que representa la media para dicho dato seleccionado. De manera extra, se da la opción de comparar los datos de Almería con los de cualquier otra provincia andaluza a seleccionar.') 
    st.markdown('Por último, añadir que el gráfico es interactivo por lo que permite: el estudio de tendencias en un rango temporal más o menos prolongado, obtener el para un momento puntual arrastrando el ratón sobre la gráfica, \
            hacer _zoom in_ y _zoom out_...')    


    ## Obtenemos los datos de hoy mediante una petición a la api
    Andalucia_df = scrapy_data()

    ## Datos de la comunidad    
    Granada =  Andalucia_df[Andalucia_df.Territorio == 'Granada']
    #Almería['Mes'] = [x.month for x in Almería.Fecha]
#
    options = ("Nuevos casos", "Hospitalizados","UCI",'Fallecidos')
    select_data1 = st.sidebar.radio(
        "¿Qué datos quieres ver?",
        options
    )
    options_province = ("No", "Almería","Cádiz", "Córdoba", "Huelva", "Jaén", "Málaga", "Sevilla")
    select_data2 = st.sidebar.radio(
        "¿Quieres comparar los datos con otra provincia?",
        options_province
    )
    
    time_line_plot(Andalucia_df, select_data1, 'Granada' , select_data2)
    st.markdown('En adición a ello, podemos ver a continuación un [gráfico de violín](https://en.wikipedia.org/wiki/Violin_plot#:~:text=A%20violin%20plot%20is%20a,by%20a%20kernel%20density%20estimator.). \
    En este gráfico al igual que antes podemos comparar un tipo de dato entre dos provincias. Su utilidad reside en que de un solo vistazo podemos hacernos una idea tanto de la distribución como de los estadísticos básicos. \
        Además, se trata de nuevo de un gráfico interactivo que permite obtener información arrastrando el ratón por los diferentes elementos del mismo.')
    violin_chart(Andalucia_df, select_data1, 'Granada' , select_data2)
    st.markdown('## Últimos datos de la provincia')
    st.markdown('A continuación se presenta una tabla con los datos de los diez días mas recientes,\
        publicados por la [Junta de Andalucía](https://www.juntadeandalucia.es/institutodeestadisticaycartografia/badea/operaciones/consulta/anual/39409?CodOper=b3_2314&codConsulta=39409),\
        para la provincia granadina.')


    st.dataframe(Granada.head(10).reset_index(drop=True))

    About1 = st.sidebar.markdown('## 🤝 Sobre nosotros')

    About = st.sidebar.info('Somos dos amigos graduados en matemáticas por la Universidad de Cádiz. Posteriormente obtuvimos el Máster en Data Science & Big Data en Afi Escuela de Finanzas.')

    Contact = st.sidebar.markdown('## 📩 ¡Encuéntranos en LinkedIn!')

    Contact1 = st.sidebar.info('[Francisco Alonso Fernández](https://www.linkedin.com/in/franciscoalonsofernandez/) Data Scientist en [Future Space](https://www.futurespace.es/).')
    Contact2 = st.sidebar.info('[Javier Ángel Fernández](https://www.linkedin.com/in/javier-angel-fernandez/) Data Scientist en [IIC](https://www.iic.uam.es/).')