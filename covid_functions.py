import warnings
warnings.filterwarnings("ignore")

import streamlit as st
from streamlit_folium import folium_static
from streamlit_echarts import st_pyecharts

from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import plotly.express as px

import json

import folium

import pyecharts.options as opts

from pyecharts.charts import Calendar
from pyecharts.charts import Bar, Line, Scatter, EffectScatter, Timeline
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts

import datetime

########## DATA
@st.cache
def scrapy_data():
    """Función encargada de extraer los datos por provincia y fecha de Covid.

    Returns
    -------
    DataFrame
        DataFrame con los datos históricos por fecha y por provincia.
    """

    url = "https://www.juntadeandalucia.es/institutodeestadisticaycartografia/intranet/admin/rest/v1.0/consulta/39409"
    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload, verify=False)
    my_data = response.json()

    ## Pasamos los datos del json a un DataFrame

    fecha = []
    territorio = []
    confirmados_pdia = []
    hospitalizados = []
    uci = []
    fallecidos = []

    for index in range(len(my_data['data'])):
        fecha += [my_data['data'][index][0]['des']]
        territorio += [my_data['data'][index][1]['des']]
        confirmados_pdia += [my_data['data'][index][3]['format']]
        hospitalizados += [my_data['data'][index][5]['format']]
        uci += [my_data['data'][index][6]['format']]
        fallecidos += [my_data['data'][index][7]['format']]
        
    Andalucia_df = pd.DataFrame({'Fecha':fecha,'Territorio':territorio, 'Nuevos casos':confirmados_pdia,\
                'Hospitalizados':hospitalizados,'UCI':uci, 'Fallecidos':fallecidos})
    Andalucia_df[['Nuevos casos', 'Hospitalizados', 'UCI','Fallecidos']] = Andalucia_df[['Nuevos casos', 'Hospitalizados', 'UCI','Fallecidos']].applymap(lambda x: x.replace('.',''))
    Andalucia_df[['Nuevos casos', 'Hospitalizados', 'UCI','Fallecidos']] = Andalucia_df[['Nuevos casos', 'Hospitalizados', 'UCI','Fallecidos']].applymap(lambda x: float(x))
    Andalucia_df['Fecha'] = pd.to_datetime(Andalucia_df['Fecha'], format='%d/%m/%Y')

    return Andalucia_df

def json_to_df(url, lista_datos_acumulados):
    """Función para extraer datos por municipio por provincia.
    Esta función habrá que ejecutarla 8 veces (1 vez por provincia).

    Parameters
    ----------
    url : string
        _URL del json de cada provincia con los datos municipales.
    lista_datos_acumulados : list
        lista con los datos acumulados que salen en la tabla de la página de la junta.

    Returns
    -------
    DataFrame
        Dataframe con los datos de la provincia con los municipios como índice.
    """
    payload = {}
    headers = {}
    
    data = []
    response = requests.request("GET", url, headers=headers, data = payload,verify=False)
    df = response.json()
    
    columnas = [x['des'] for x in df['measures']]
    indice = [x[0]['des'] for x in df['data']]
    
    for i in range(len(df['data'])):
        aux = [x['val'] for x in df['data'][i] if 'val' in x.keys()]
        tup = tuple(aux)
        data.append(tup)
    data = pd.DataFrame(data,columns=columnas)
    data['indice'] = indice
    data = data[-data['indice'].isin(lista_datos_acumulados)].reset_index(drop=True)
    data = data.set_index(['indice'])
    return data.applymap(lambda x : float(x) if x!='' else np.nan)
    return data


########## PLOTS 


def plot_map(datos):
    """[summary]

    Parameters
    ----------
    datos : [type]
        [description]
    """


    with open('Andalucia_GeoJSON.geojson',encoding="utf-8") as f:
        geo = json.load(f, encoding="utf-8")

    ## Se corrige un pequeño fallo con la tilde de Almería

    geo['features'][0]['properties']['texto']='Almería'


    m = folium.Map(location=[37, -4.8], zoom_start=6.5)
    
    folium.Choropleth(
        geo_data=geo,
        name='choropleth',
        data=datos,
        columns=['Territorio','Nuevos casos'],
        key_on='feature.properties.texto',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        ## Nota: Fernando sabe de sobra que Hernández lleva tilde, pero el decode de Folium da problemas
        legend_name ='Created by: Francisco Alonso').add_to(m)
    
    folium.LayerControl().add_to(m)
    
    ## Cádiz
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([36.5, -6.1], popup='<h3> C&aacutediz: </h3>'+'<p>'+str(datos[datos.Territorio == 'Cádiz']['Fecha'].tolist()[0])[:-9]+'</p>'\
                +'<p> Nuevos casos: '+str(datos[datos.Territorio == 'Cádiz']['Nuevos casos'].tolist()[0])+'</p>'\
                +'<p> Hospitalizados: '+str(datos[datos.Territorio == 'Cádiz']['Hospitalizados'].tolist()[0])+'</p>'\
                +'<p> UCI: '+str(datos[datos.Territorio == 'Cádiz']['UCI'].tolist()[0])+'</p>'\
                +'<p> Fallecidos: '+str(datos[datos.Territorio == 'Cádiz']['Fallecidos'].tolist()[0])+'</p>',
                icon=icon).add_to(m)
        
    ## Sevilla
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([37.3, -5.9], popup='<h3> Sevilla: </h3>'+'<p>'+str(datos[datos.Territorio == 'Sevilla']['Fecha'].tolist()[0])[:-9]+'</p>'\
                +'<p> Nuevos casos: '+str(datos[datos.Territorio == 'Sevilla']['Nuevos casos'].tolist()[0])+'</p>'\
                +'<p> Hospitalizados: '+str(datos[datos.Territorio == 'Sevilla']['Hospitalizados'].tolist()[0])+'</p>'\
                +'<p> UCI: '+str(datos[datos.Territorio == 'Sevilla']['UCI'].tolist()[0])+'</p>'\
                +'<p> Fallecidos: '+str(datos[datos.Territorio == 'Sevilla']['Fallecidos'].tolist()[0])+'</p>',
                icon=icon).add_to(m)
        
    ## Huelva
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([37.6, -6.8], popup='<h3> Huelva: </h3>'+'<p>'+str(datos[datos.Territorio == 'Huelva']['Fecha'].tolist()[0])[:-9]+'</p>'\
                +'<p> Nuevos casos: '+str(datos[datos.Territorio == 'Huelva']['Nuevos casos'].tolist()[0])+'</p>'\
                +'<p> Hospitalizados: '+str(datos[datos.Territorio == 'Huelva']['Hospitalizados'].tolist()[0])+'</p>'\
                +'<p> UCI: '+str(datos[datos.Territorio == 'Huelva']['UCI'].tolist()[0])+'</p>'\
                +'<p> Fallecidos: '+str(datos[datos.Territorio == 'Huelva']['Fallecidos'].tolist()[0])+'</p>',
                icon=icon).add_to(m)
        
    ## Córdoba
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([37.8, -4.7], popup='<h3> C&oacute;rdoba: </h3>'+'<p>'+str(datos[datos.Territorio == 'Córdoba']['Fecha'].tolist()[0])[:-9]+'</p>'\
                +'<p> Nuevos casos: '+str(datos[datos.Territorio == 'Córdoba']['Nuevos casos'].tolist()[0])+'</p>'\
                +'<p> Hospitalizados: '+str(datos[datos.Territorio == 'Córdoba']['Hospitalizados'].tolist()[0])+'</p>'\
                +'<p> UCI: '+str(datos[datos.Territorio == 'Córdoba']['UCI'].tolist()[0])+'</p>'\
                +'<p> Fallecidos: '+str(datos[datos.Territorio == 'Córdoba']['Fallecidos'].tolist()[0])+'</p>',
                icon=icon).add_to(m)
    
    ## Jaén
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([37.7, -3.7], popup='<h3> Ja&eacute;n: </h3>'+'<p>'+str(datos[datos.Territorio == 'Jaén']['Fecha'].tolist()[0])[:-9]+'</p>'\
                +'<p> Nuevos casos: '+str(datos[datos.Territorio == 'Jaén']['Nuevos casos'].tolist()[0])+'</p>'\
                +'<p> Hospitalizados: '+str(datos[datos.Territorio == 'Jaén']['Hospitalizados'].tolist()[0])+'</p>'\
                +'<p> UCI: '+str(datos[datos.Territorio == 'Jaén']['UCI'].tolist()[0])+'</p>'\
                +'<p> Fallecidos: '+str(datos[datos.Territorio == 'Jaén']['Fallecidos'].tolist()[0])+'</p>',
                icon=icon).add_to(m)
    
    ## Málaga
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([36.8, -4.5], popup='<h3> M&aacute;laga: </h3>'+'<p>'+str(datos[datos.Territorio == 'Málaga']['Fecha'].tolist()[0])[:-9]+'</p>'\
                +'<p> Nuevos casos: '+str(datos[datos.Territorio == 'Málaga']['Nuevos casos'].tolist()[0])+'</p>'\
                +'<p> Hospitalizados: '+str(datos[datos.Territorio == 'Málaga']['Hospitalizados'].tolist()[0])+'</p>'\
                +'<p> UCI: '+str(datos[datos.Territorio == 'Málaga']['UCI'].tolist()[0])+'</p>'\
                +'<p> Fallecidos: '+str(datos[datos.Territorio == 'Málaga']['Fallecidos'].tolist()[0])+'</p>',
                icon=icon).add_to(m)
    
    ## Granada
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([37.1, -3.5], popup='<h3> Granada: </h3>'+'<p>'+str(datos[datos.Territorio == 'Granada']['Fecha'].tolist()[0])[:-9]+'</p>'\
                +'<p> Nuevos casos: '+str(datos[datos.Territorio == 'Granada']['Nuevos casos'].tolist()[0])+'</p>'\
                +'<p> Hospitalizados: '+str(datos[datos.Territorio == 'Granada']['Hospitalizados'].tolist()[0])+'</p>'\
                +'<p> UCI: '+str(datos[datos.Territorio == 'Granada']['UCI'].tolist()[0])+'</p>'\
                +'<p> Fallecidos: '+str(datos[datos.Territorio == 'Granada']['Fallecidos'].tolist()[0])+'</p>',
                icon=icon).add_to(m)
    
    ## Almería
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([37, -2.3], popup='<h3> Almer&iacute;a: </h3>'+'<p>'+str(datos[datos.Territorio == 'Almería']['Fecha'].tolist()[0])[:-9]+'</p>'\
                +'<p> Nuevos casos: '+str(datos[datos.Territorio == 'Almería']['Nuevos casos'].tolist()[0])+'</p>'\
                +'<p> Hospitalizados: '+str(datos[datos.Territorio == 'Almería']['Hospitalizados'].tolist()[0])+'</p>'\
                +'<p> UCI: '+str(datos[datos.Territorio == 'Almería']['UCI'].tolist()[0])+'</p>'\
                +'<p> Fallecidos: '+str(datos[datos.Territorio == 'Almería']['Fallecidos'].tolist()[0])+'</p>',
                icon=icon).add_to(m)
    
    folium_static(m)




def pyechart_comunidad_bar(df, data1, data2):
    """Plot comparing those two charasteristics.

    Parameters
    ----------
    df : DataFrame
        [description]
    data1 : Series
        Column to plot between "nuevos casos", "hospitalizados", "UCI" y "fallecidos"
    data2 : Series
        Column to plot between "nuevos casos", "hospitalizados", "UCI" y "fallecidos"
    """


    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.ESSOS))
        .add_xaxis(['FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV'])
        .add_yaxis(data1, df[data1].tolist())
        .add_yaxis(data2, df[data2].tolist())
        .set_global_opts(
                title_opts = opts.TitleOpts(title="Covid Andalucía", subtitle="Datos desde el inicio de la pandemia"),
                xaxis_opts= opts.AxisOpts(
                    splitline_opts=opts.SplitLineOpts(is_show=True)
                    ),
                yaxis_opts= opts.AxisOpts(
                    splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=0))
                    ),
                toolbox_opts = opts.ToolboxOpts(is_show = True, orient='vertical', pos_left='95%'), 
                datazoom_opts= [opts.DataZoomOpts(range_start=10, range_end=80,is_zoom_lock=False)],
            )
        .set_series_opts(
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max", name="MAX"), opts.MarkPointItem(type_="min", name="MIN"),]),
            markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="AVG")]),
            label_opts=opts.LabelOpts(is_show=False)
        )
        )
    st_pyecharts(bar)


def calendar_plot(df):
    """[summary]

    Parameters
    ----------
    df : [type]
        [description]
    """

    #begin = datetime.date(2020, 2, 9)
    #end = datetime.date(2020,11,11)
    begin = df.Fecha.min()
    end = df.Fecha.max()

    c = (
        Calendar(init_opts=opts.InitOpts(width="1000px", height="300px"))
        .add(
            series_name="",
            yaxis_data=[[str(x),y] for x,y in zip(df.Fecha, df['Nuevos casos'])],
            calendar_opts=opts.CalendarOpts(
                pos_top="120",
                pos_left="30",
                pos_right="30",
                range_="2020",
                yearlabel_opts=opts.CalendarYearLabelOpts(is_show=False),
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(pos_top="20", pos_left="center", title="2020: Evolución del Covid19 en Andalucía"),
            visualmap_opts=opts.VisualMapOpts(
                max_=df['Nuevos casos'].max(), min_=0, orient="horizontal", is_piecewise=False
            ),
        )
    )   
    st_pyecharts(c)


def plotly_stacked(df):
    """[summary]

    Parameters
    ----------
    df : [type]
        [description]
    """

    fig1 = px.bar(Provincias_acumulados, x="Territorio", y=["Nuevos casos", "Hospitalizados", "UCI", "Fallecidos"], title="Datos acumulados desde el inicio de la pandemia",\
        color_discrete_sequence=['#BE5A54', '#FF7733', '#FFA833', '#FFF367'])

    st.plotly_chart(fig1,height=110,width=300)


def time_line_plot(df, select_data, province1, province2):
    """[summary]

    Parameters
    ----------
    df : [type]
        [description]
    select_data : [type]
        [description]
    province1 : [type]
        [description]
    province2 : [type]
        [description]
    """
    df1 =df[df.Territorio == province1]
    if province2 == 'No':
        chart_title = 'Histórico de ' + select_data.lower() + ' en  ' + province1
        fig = go.Figure()
        fig.add_trace(go.Scatter(
                        x=df1['Fecha'],
                        y=df1[select_data],
                        name=select_data+ ' en ' + province1,
                        line_color='red',
                        opacity=0.8))
        fig.add_trace(go.Scatter(
                        x=df1['Fecha'],
                        y=df1[select_data].mean()*np.ones(len(df1['Fecha'])),
                        name='Media de ' +  select_data.lower() + ' en ' + province1,
                        mode='markers',
                        marker={"size": 2},
                        line_color='red',
                        opacity=0.5))
        # Use date string to set xaxis range
        fig.update_layout(title_text=chart_title,
                        xaxis_rangeslider_visible=True,
                        legend=dict(
                        orientation="h",
					    yanchor="top",
					    y=1.2,
					    xanchor="left",
					    x=0.01))
        #fig.show()
        #col1, col2 = st.beta_columns([1, 1])
        #
        #col1.subheader("Evolución")
        #col1.plotly_chart(fig,height=0,width=0)
        #
        #col2.subheader("Últimos datos")
        #col2.dataframe(Aux.head(10).reset_index(drop=True))
        st.plotly_chart(fig,height=110,width=300)
    else:
        df2 =  df[df.Territorio == province2]
        chart_title = 'Histórico de ' + select_data.lower() + ' en  ' + province1 + ' y ' + province2
        fig = go.Figure()
        fig.add_trace(go.Scatter(
                        x=df1['Fecha'],
                        y=df1[select_data],
                        name=select_data+ ' en ' + province1,
                        line_color='red',
                        opacity=0.8))
        fig.add_trace(go.Scatter(
                        x=df1['Fecha'],
                        y=df1[select_data].mean()*np.ones(len(df1['Fecha'])),
                        name='Media de ' +  select_data.lower()+ ' en ' + province1,
                        mode='markers',
                        marker={"size": 2},
                        line_color='red',
                        opacity=0.5))
        fig.add_trace(go.Scatter(
                        x=df2['Fecha'],
                        y=df2[select_data],
                        name=select_data+ ' en ' + province2,
                        line_color='blue',
                        opacity=0.4))
        fig.add_trace(go.Scatter(
                        x=df2['Fecha'],
                        y=df2[select_data].mean()*np.ones(len(df2['Fecha'])),
                        name='Media de ' +  select_data.lower()+ ' en ' + province2,
                        mode='markers',
                        marker={"size": 2},
                        line_color='blue',
                        opacity=0.2))
        # Use date string to set xaxis range
        fig.update_layout(title_text=chart_title,
                        xaxis_rangeslider_visible=True,
                        legend=dict(
                        orientation="h",
					    yanchor="top",
					    y=1.25,
					    xanchor="left",
					    x=0.01))
        #fig.show()
        #col1, col2 = st.beta_columns([1, 1])
        #
        #col1.subheader("Evolución")
        #col1.plotly_chart(fig,height=0,width=0)
        #
        #col2.subheader("Últimos datos")
        #col2.dataframe(Aux.head(10).reset_index(drop=True))
        st.plotly_chart(fig,height=210,width=500)

def plot_timeline(df, data1 = 'Nuevos casos', data2 = 'Hospitalizados'):
    """[summary]

    Parameters
    ----------
    df : [type]
        [description]
    data1 : str, optional
        [description], by default 'Nuevos casos'
    data2 : str, optional
        [description], by default 'Hospitalizados'
    """
    tl = Timeline()
    calendar_dict = {
    1:'Ene',
    2:'Feb',
    3:'Mar',
    4:'Abr',
    5:'May',
    6:'Jun',
    7:'Jul',
    8:'Ag',
    9:'Sep',
    10:'Oct',
    11:'Nov',
    12:'Dic'
}
    for i in range(3, df.Mes.max()+1):
        bar = (
            Bar()
            .add_xaxis(pd.unique(df.Territorio).tolist())
            .add_yaxis(data1, df[df.Mes == i][data1].tolist())
            .add_yaxis(data2, df[df.Mes == i][data2].tolist())
            .set_global_opts(
                title_opts=opts.TitleOpts("Covid19 mes a mes"),
                graphic_opts=[
                    opts.GraphicGroup(
                        graphic_item=opts.GraphicItem(
                            rotation=JsCode("Math.PI / 4"),
                            bounding="raw",
                            right=100,
                            bottom=110,
                            z=100,
                        ),
                    )
                ],
            )
        )
        tl.add(bar,calendar_dict[i])
    st_pyecharts(tl)
   