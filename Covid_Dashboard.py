### Librerías necesarias

import streamlit as st
from streamlit_folium import folium_static

from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import plotly.graph_objects as go

import pandas as pd
import plotly.express as px

import json

import folium


st.title('Covid-19 en Andalucía😷')
st.markdown('## Visor cartográfico')
st.markdown('A continuación se presenta un visor cartográfico con los datos más recientes,\
     publicados por la [Junta de Andalucía](https://www.juntadeandalucia.es/institutodeestadisticaycartografia/badea/operaciones/consulta/anual/39409?CodOper=b3_2314&codConsulta=39409),\
     para cada provincia. Haciendo click en los marcadores podremos ver información acerca de nuevos casos, hospitalizaciones, ingresadosen UCI y fallecidos.')
st.markdown('Además, de manera estática y gracias al gradiente de colores,\
         podemos de un vistazo observar la diferencia de nuevos casos entre las diferentes provincias.')         


## Obtenemos los datos de hoy mediante una petición a la api
url = "https://www.juntadeandalucia.es/institutodeestadisticaycartografia/intranet/admin/rest/v1.0/consulta/39409"
payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)
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

## Pasamos la columna Fecha a tipo fecha

Andalucia_df['Fecha'] = pd.to_datetime(Andalucia_df['Fecha'], format='%d/%m/%Y')

## Datos acumulados
Aux_acumulados = Andalucia_df[Andalucia_df.Territorio!='Andalucía']
Aux_acumulados[['Nuevos casos', 'Hospitalizados', 'UCI','Fallecidos']] = Aux_acumulados[['Nuevos casos', 'Hospitalizados', 'UCI','Fallecidos']].apply(pd.to_numeric)
Provincias_acumulados = Aux_acumulados[['Territorio','Nuevos casos', 'Hospitalizados', 'UCI','Fallecidos']].groupby(['Territorio']).sum()
Provincias_acumulados.reset_index(inplace=True)

## Nos quedamos con los datos de la fehca más reciente en el momento de ejecución
Andalucia_LastDate = Andalucia_df[Andalucia_df.Fecha == Andalucia_df.Fecha[0]]
Andalucia_LastDate = Andalucia_LastDate[Andalucia_LastDate.Territorio != 'Andalucía']

with open('Andalucia_GeoJSON.geojson',encoding="utf-8") as f:
    geo = json.load(f, encoding="utf-8")

## Se corrige un pequeño fallo con la tilde de Almería

geo['features'][0]['properties']['texto']='Almería'

Andalucia_LastDate["Nuevos casos"] = pd.to_numeric(Andalucia_LastDate["Nuevos casos"])


## Función para pintar el mapa

def plot_map(datos):
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

plot_map(Andalucia_LastDate)

st.markdown('## Datos desde el inicio de la pandemia')
st.markdown('En el siguiente gráfico de barras apiladas podemos ver el acumulado de los datos para cada provincia. \
    El gráfico es interactivo y permite pasar el puntero por las diferentes barras y además podemos hacer zoom o seleccionar un recuadro que queramos ver específicamente.')

fig1 = px.bar(Provincias_acumulados, x="Territorio", y=["Nuevos casos", "Hospitalizados", "UCI", "Fallecidos"], title="Datos acumulados desde el inicio de la pandemia",\
    color_discrete_sequence=['#BE5A54', '#FF7733', '#FFA833', '#FFF367'])

##px.colors.qualitative.Set2 esta paleta podría valer
    
st.plotly_chart(fig1,height=110,width=300)

select_province = st.sidebar.selectbox(
    "Elige una provincia",
    ("Almería", "Cádiz","Córdoba", "Granada", "Huelva", "Jaén", "Málaga", "Sevilla")
)
select_data = st.sidebar.radio(
    "¿Qué dato quieres ver?",
    ("Nuevos casos", "Hospitalizados","UCI",'Fallecidos')
)

st.markdown('## Histórico interactivo')
st.markdown('Seleccionando una provincia y un tipo de dato en la parte de la izquierda podremos ver su evolución histórica en la siguiente gráfica. Además, gracias a \
    la barra inferior podremos movernos a lo largo del tiempo en los últimos meses para estudiar tendencias. Por último, situándonos en cualquier punto de la curva \
        podemos ver exactamente el valor para una fecha dada.')


Aux = Andalucia_df[Andalucia_df.Territorio == select_province]
chart_title = 'Histórico de ' + select_data.lower() + ' en  ' + select_province
fig = go.Figure()
fig.add_trace(go.Scatter(
                x=Aux['Fecha'],
                y=Aux[select_data],
                name=select_data,
                line_color='red',
                opacity=0.8))

# Use date string to set xaxis range
fig.update_layout(title_text=chart_title,
                 xaxis_rangeslider_visible=True)
#fig.show()


#col1, col2 = st.beta_columns([1, 1])
#
#col1.subheader("Evolución")
#col1.plotly_chart(fig,height=0,width=0)
#
#col2.subheader("Últimos datos")
#col2.dataframe(Aux.head(10).reset_index(drop=True))


st.plotly_chart(fig,height=110,width=300)

st.markdown('## Últimos 10 días')
st.markdown('Finalmente, aquí mostramos una tabla de los últimos diez días para la provincia que hayamos seleccionado.')

st.dataframe(Aux.head(10).reset_index(drop=True))

st.markdown('## Próximos avances')
st.markdown('En las próximas semanas nos centraremos a incrementar el foco y tratar de hacer el mismo estudio a nivel municipal. También tenemos en mente\
    la elaboración de predicciones, así como la elaboración de gráficas que comparen territorios dos a dos. No obstante, ¡estamos abiertos a cualquier propuesta!.')


About1 = st.sidebar.markdown('## 🤝 Sobre nosotros')

About = st.sidebar.info('Somos dos amigos graduados en matemáticas por la Universidad de Cádiz. Posteriormente obtuvimos el Máster en Data Science & Big Data en Afi Escuela de Finanzas.')

Contact = st.sidebar.markdown('## 📩 ¡Encuéntranos en LinkedIn!')

Contact1 = st.sidebar.info('[Francisco Alonso Fernández](https://www.linkedin.com/in/franciscoalonsofernandez/) Data Scientist en [Future Space](https://www.futurespace.es/).')
Contact2 = st.sidebar.info('[Javier Ángel Fernández](https://www.linkedin.com/in/javier-angel-fernandez/) Data Scientist en [IIC](https://www.iic.uam.es/).')


