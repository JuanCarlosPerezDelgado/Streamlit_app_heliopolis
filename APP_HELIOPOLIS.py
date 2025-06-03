from datetime import datetime, timedelta,date         
import pandas as pd
import matplotlib.pyplot as plt     
import numpy as np
import streamlit as st
from time import sleep
import streamlit_option_menu
from streamlit_option_menu import option_menu
import plotly.express as px
import webbrowser


from simulador import simulador_grafico

st.set_page_config(layout="wide")

with st.sidebar:

    menu= option_menu(menu_title=None,  
        options=['Laboratorio Virtual','Datos en Histórico'],
        icons=['bi bi-info-circle', 'bi bi-cloud-arrow-down', 'bi bi-database-down', 'gear','bi bi-chat-dots'],
        default_index=0,
         styles={'container': {'padding': '5px', 'background-color': '#ffffff'},
        'icon': {'color': 'orange', 'font-size': '18px'},
        'nav-link': {'font-size': '16px', 'text-align': 'left', 'margin': '0px'},
        'nav-link-selected': {'background-color': '#03617E'},})

if menu == 'Laboratorio Virtual':

    menu_herramientas = option_menu(
        menu_title=None,  
        options=['Entorno 360','Realidad Virtual','Información'],
        default_index=0,
        orientation='horizontal',
        styles={'container': {'padding': '5px', 'background-color': '#ffffff'},
        'icon': {'color': 'orange', 'font-size': '18px'},
        'nav-link': {'font-size': '16px', 'text-align': 'left', 'margin': '0px'},
        'nav-link-selected': {'background-color': '#03617E'}})

    if menu_herramientas == 'Entorno 360':
        st.components.v1.iframe("https://juancarlosperezdelgado.github.io/Imagenes_heliopolis/index.html", width=2000, height=1000)

    elif menu_herramientas == 'Realidad Virtual':
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2,col3 = st.columns(3)
        with col1:
            pass
        with col2:
            st.image("visionqr.png", width=390)
        with col3:
            pass
        col1, col2,col3,col4,col5 = st.columns(5)
        with col1:
            pass
        with col2:
            pass
        with col3:
            st.markdown("""
            <a href="https://drive.google.com/file/d/12fkcycl8dFucg56aM2eVkWmaMkI_Nzfx/view?usp=drive_link" target="_blank">
            <button style='padding: 0.6em 1.5em;
                   background-color: #03617E;
                   color: white;
                   border: none;
                   border-radius: 5px;
                   font-size: 17px;
                   font-weight: bold;
                   cursor: pointer;'>
                Descargar Archivo VR
            </button>
            </a>
            """, unsafe_allow_html=True)
        with col4:
            pass
        with col5:
            pass
    elif menu_herramientas == 'Información':
        pass

elif menu == 'Datos en Histórico':
    df_ensayo_0=pd.read_excel('Ensayo0C.xlsx',index_col=0,parse_dates=True)
    df_ensayo_menos5=pd.read_excel('Ensayo-5C.xlsx',index_col=0,parse_dates=True)
    df_ensayo_menos10=pd.read_excel('Ensayo-10C.xlsx',index_col=0,parse_dates=True)

    df_ensayo_0=df_ensayo_0.interpolate()
    df_ensayo_0=df_ensayo_0.bfill()
    df_ensayo_0=df_ensayo_0.round(2)

    df_ensayo_menos5=df_ensayo_menos5.interpolate()
    df_ensayo_menos5=df_ensayo_menos5.bfill()
    df_ensayo_menos5=df_ensayo_menos5.round(2)

    df_ensayo_menos10=df_ensayo_menos10.interpolate()
    df_ensayo_menos10=df_ensayo_menos10.bfill()
    df_ensayo_menos10=df_ensayo_menos10.round(2)

    col1, col2, col3 = st.columns(3)
    with col1:
        ensayo_seleccionado = st.selectbox('Ensayos disponibles',['Ensayo a 0°C','Ensayo a -5°C','Ensayo a -10°C'])
        if ensayo_seleccionado == 'Ensayo a 0°C':
            st.session_state.ensayo_seleccionado = df_ensayo_0
        elif ensayo_seleccionado == 'Ensayo a -5°C':
            st.session_state.ensayo_seleccionado = df_ensayo_menos5
        elif ensayo_seleccionado == 'Ensayo a -10°C':
            st.session_state.ensayo_seleccionado = df_ensayo_menos10
    with col2:
        tipo_grafico_diferido = st.multiselect('Tipo de gráfico',['Scada','Gráfico de líneas (temperaturas, presiones, relés, consumo)','Diagramas PH-TS','Gráfico de líneas (COP)'],default=['Gráfico de líneas (temperaturas, presiones, relés, consumo)'])
        st.session_state.tipo_grafico_diferido = tipo_grafico_diferido
    with col3:
        velocidad_reproduccion = st.number_input('Velocidad de reproducción (segundos)',0.0,60.0,1.0)
        st.session_state.velocidad_reproduccion = velocidad_reproduccion

    if st.button('Simular'):
        
        simulador_grafico(st.session_state.ensayo_seleccionado,st.session_state.tipo_grafico_diferido,st.session_state.velocidad_reproduccion)
    

    #['Rele compresor', 'Rele desescarche', 'Rele on/off',
    #   'Potencia compresor', ' Temperatura salida aire evaporador',
    #   'Temperatura entrada aire condensador',
    #   'Temperatura salida aire condensador', 'Temperatura descarga compresor',
    #   'Temperatura entrada  valvula expansion',
    #   'Temperatura entrada bandeja condensados',
    #   'Temperatura salida bandeja condensados',
    #   'Temperatura entrada aire evaporador',
    #   'Temperatura aspiracion compresor', 'Temperatura salida condensador',
    #   'Presion alta', 'Presion baja']
