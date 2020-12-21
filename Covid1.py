### Librerías necesarias
import warnings
warnings.filterwarnings("ignore")
from datetime import timedelta
import streamlit as st
from streamlit_folium import folium_static
from streamlit_echarts import st_pyecharts

from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import plotly.graph_objects as go

import pandas as pd
import plotly.express as px

import json

import folium

import pyecharts.options as opts

from pyecharts.charts import Calendar
from pyecharts.charts import Bar, Line, Scatter, EffectScatter
from pyecharts import options as opts
from pyecharts.globals import ThemeType

from covid_functions import *

import datetime

def app():


    st.title('Covid-19 en Andalucía😷')
    st.markdown('## Visores cartográficos')
    st.markdown('A continuación se presenta un visor cartográfico con los datos más recientes,\
        publicados por la [Junta de Andalucía](https://www.juntadeandalucia.es/institutodeestadisticaycartografia/badea/operaciones/consulta/anual/39409?CodOper=b3_2314&codConsulta=39409),\
        para cada provincia. Haciendo click en los marcadores podremos ver información acerca de nuevos casos, hospitalizaciones, ingresadosen UCI y fallecidos.')
    st.markdown('Además, de manera estática y gracias al gradiente de colores,\
            podemos rápidamente observar la diferencia de nuevos casos entre las diferentes provincias.')         


    ## Obtenemos los datos de hoy mediante una petición a la api
    Andalucia_df = scrapy_data()

    ## Datos acumulados
    Aux_acumulados = Andalucia_df[Andalucia_df.Territorio!='Andalucía']
    Aux_acumulados['Mes'] = [x.month for x in Aux_acumulados.Fecha]
    Provincias_acumulados = Aux_acumulados[['Territorio','Mes','Nuevos casos', 'Hospitalizados', 'UCI','Fallecidos']].groupby(['Territorio','Mes']).sum()
    Provincias_acumulados.reset_index(inplace=True)

    ## Datos de la comunidad
    Comunidad =  Andalucia_df[Andalucia_df.Territorio == 'Andalucía']
    Comunidad['Mes'] = [x.month for x in Comunidad.Fecha]
    Comunidad1 = Comunidad.groupby(['Mes']).sum().reset_index()

    ## Nos quedamos con los datos de la fehca más reciente en el momento de ejecución
    try:

        Andalucia_LastDate = Andalucia_df[Andalucia_df.Fecha == Andalucia_df.Fecha.max()]
        Andalucia_LastDate = Andalucia_LastDate[Andalucia_LastDate.Territorio != 'Andalucía']
        plot_map(Andalucia_LastDate)
    except IndexError:
        Andalucia_LastDate = Andalucia_df[Andalucia_df.Fecha == (Andalucia_df.Fecha.max()-timedelta(1))]
        Andalucia_LastDate = Andalucia_LastDate[Andalucia_LastDate.Territorio != 'Andalucía']
        plot_map(Andalucia_LastDate)

    st.markdown('En el visor de a continuación disponemos de la información a nivel municipal. Es importante mencionar que la Junta de Andalucía, \
        provee los datos diarios solamente a nivel provincial. Por lo tanto los datos que vemos reflejados en el siguiente mapa son los valores acumulados \
            desde el inicio de la pandemia.')
    ## Mapa con datos municipales
    towns_plot()

    options = ("Nuevos casos", "Hospitalizados","UCI",'Fallecidos')
    select_data1 = st.sidebar.radio(
        "¿Qué datos quieres ver en el histograma?",
        options
    )
    select_data2 = st.sidebar.radio(
        "¿Contra que dato?",
        tuple([x for x in options if x!=select_data1]),0)

    st.markdown('## Calendario de nuevos casos desde el inicio de la pandemia')
    st.markdown('El calendario interactivo que se muestra a continuación dispone de forma visual el avance la pandemia a lo largo\
        del tiempo en Andalucía. Además, no solo nos permite de un vistazo ver cuáles han sido los peores meses gracias al\
        la diferencia de colores, sino que también el posible ver el dato de nuevos casos para un día concreto simplemente pasando el ratón encima.')


    calendar_plot(Comunidad)

    st.markdown('## Evolución mensual')
    st.markdown('El siguiente diagrama de barras compara los datos que elijamos en la columna de la derecha mes a mes desde marzo hasta la actualizadad. \
        Permite o bien la elección del mes o bien ver todos seguidos presionando el botón de play.')

    #pyechart_comunidad_bar(Comunidad1, select_data1, select_data2)

#    st.markdown('## Datos desde el inicio de la pandemia')
#    st.markdown('En el siguiente gráfico de barras apiladas podemos ver el acumulado de los datos para cada provincia. \
#        El gráfico es interactivo y permite pasar el puntero por las diferentes barras y además podemos hacer zoom o seleccionar un recuadro que queramos ver específicamente.')
#
#    plotly_stacked(Provincias_acumulados)
#
#    select_province = st.sidebar.selectbox(
#        "Elige una provincia",
#        ("Almería", "Cádiz","Córdoba", "Granada", "Huelva", "Jaén", "Málaga", "Sevilla")
#    )
#    select_data = st.sidebar.radio(
#        "¿Qué dato quieres ver?",
#        ("Nuevos casos", "Hospitalizados","UCI",'Fallecidos')
#    )
#
#    st.markdown('## Histórico interactivo')
#    st.markdown('Seleccionando una provincia y un tipo de dato en la parte de la izquierda podremos ver su evolución histórica en la siguiente gráfica. Además, gracias a \
#        la barra inferior podremos movernos a lo largo del tiempo en los últimos meses para estudiar tendencias. Por último, situándonos en cualquier punto de la curva \
#            podemos ver exactamente el valor para una fecha dada.')
#
#    plotly_stacked(Andalucia_df)

    plot_timeline(Provincias_acumulados, select_data1, select_data2)

    st.markdown('## Datos acumulados')

    st.dataframe(Provincias_acumulados.groupby(['Territorio']).sum().drop(columns = ['Mes']))

    st.markdown('## Próximos avances')
    st.markdown('En las próximas semanas nos centraremos a incrementar el foco y tratar de hacer el mismo estudio a nivel municipal. También tenemos en mente\
        la elaboración de predicciones, así como el cruce con datos demográficos para estudiar variables como la incidencia. No obstante, ¡estamos abiertos a cualquier propuesta!.')


    # es divertido
    #st.balloons()

    About1 = st.sidebar.markdown('## 🤝 Sobre nosotros')

    About = st.sidebar.info('Somos dos amigos graduados en matemáticas por la Universidad de Cádiz. Posteriormente obtuvimos el Máster en Data Science & Big Data en Afi Escuela de Finanzas.')

    Contact = st.sidebar.markdown('## 📩 ¡Encuéntranos en LinkedIn!')

    Contact1 = st.sidebar.info('[Francisco Alonso Fernández](https://www.linkedin.com/in/franciscoalonsofernandez/) Data Scientist en [Future Space](https://www.futurespace.es/).')
    Contact2 = st.sidebar.info('[Javier Ángel Fernández](https://www.linkedin.com/in/javier-angel-fernandez/) Data Scientist en [IIC](https://www.iic.uam.es/).')