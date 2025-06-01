from datetime import datetime         
import pandas as pd
import matplotlib.pyplot as plt     
import numpy as np
import streamlit as st
import altair as alt
from time import sleep
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont
import CoolProp.CoolProp as CP
from scipy.optimize import minimize_scalar
from scipy.optimize import minimize
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def simulador_grafico(ensayo_seleccionado,tipo_grafico_diferido,velocidad_reproduccion):
    df_ensayo=ensayo_seleccionado.copy()
    df_ensayo.loc[:,"Tiempo"] = range(len(ensayo_seleccionado))
    df_ensayo.loc[:,"Indice"] = ensayo_seleccionado.index.strftime('%H:%M')
    df_ensayo=df_ensayo.reset_index(drop=True)
    df_temperaturas=df_ensayo.loc[:,['Temperatura salida aire evaporador','Temperatura entrada aire condensador',
        'Temperatura salida aire condensador', 'Temperatura descarga compresor','Temperatura entrada  valvula expansion',
        'Temperatura entrada bandeja condensados','Temperatura salida bandeja condensados','Temperatura entrada aire evaporador',                            
        'Temperatura aspiracion compresor', 'Temperatura salida condensador','Tiempo','Indice']].copy()
    df_reles=df_ensayo.loc[:,['Rele compresor', 'Rele desescarche', 'Rele on/off','Tiempo','Indice']].copy()
    df_presiones=df_ensayo.loc[:,['Presion alta', 'Presion baja','Tiempo','Indice']].copy()
    df_consumo=df_ensayo.loc[:,['Potencia compresor','Tiempo','Indice']].copy()

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2,col3,col4,col5 = st.columns(5)
    with col1:
        pass
    with col2:
        pass
    with col3:
        tiempo=st.empty()
    with col4:
        pass
    with col5:
        pass

    if 'Scada' in tipo_grafico_diferido:
        st.markdown("<br>", unsafe_allow_html=True) 

        st.markdown("<p style='font-size: 17px;'><strong>Scada</strong></p>", unsafe_allow_html=True)
 
        imagen = Image.open("instalacion.PNG")
        draw = ImageDraw.Draw(imagen)
    
        posiciones = {
        'Rele compresor': (1080, 285),
        'Potencia compresor':(1200, 285),
        'Temperatura salida aire condensador':(520,25),
        'Temperatura entrada aire condensador': (520,150),
        'Temperatura salida aire evaporador':(755,453),
        'Temperatura entrada aire evaporador':(755,575),
        'Temperatura aspiracion compresor':(1020,350),
        'Presion baja':(1020,390),
        'Temperatura entrada bandeja condensados':(1020,110),
        'Presion alta':(1020,185),
        'Temperatura descarga compresor': (1020,225),
        'Temperatura salida bandeja condensados':(685,80),
        'Temperatura salida condensador': (345,110),
        'Temperatura entrada  valvula expansion':(345,240),
        'Rele desescarche':(840,605)

        }

        unidades = {
        'Rele compresor': 'on/off',
        'Potencia compresor':'W',
        'Temperatura salida aire condensador':'°C',
        'Temperatura entrada aire condensador':'°C',
        'Temperatura salida aire evaporador': '°C',
        'Temperatura entrada aire evaporador':'°C',
        'Temperatura aspiracion compresor':'°C',
        'Presion baja': 'bar',
        'Temperatura entrada bandeja condensados': '°C',
        'Presion alta': 'bar',
        'Temperatura descarga compresor': '°C',
        'Temperatura salida bandeja condensados':'°C',
        'Temperatura salida condensador': '°C',
        'Temperatura entrada  valvula expansion':'°C',
        'Rele desescarche': 'on/off'
        }

    # Crear un placeholder para la imagen en Streamlit
        imagen_placeholder = st.empty()


    if 'Gráfico de líneas (temperaturas, presiones, relés, consumo)' in tipo_grafico_diferido:
        st.markdown("<br>", unsafe_allow_html=True)
        chart_temperaturas = st.empty()  
        chart_presiones = st.empty() 
        chart_reles = st.empty() 
        chart_consumo = st.empty() 

    if 'Diagramas PH-TS' in tipo_grafico_diferido:
        st.markdown("<br>", unsafe_allow_html=True)
        diagrama = make_subplots(rows=1, cols=2, subplot_titles=("<b>P-H</b>", "<b>T-S</b>"))
        diagrama.update_annotations(font=dict(color='black', size=16))
        diagrama_placeholder = st.empty()

    if 'Gráfico de líneas (COP)' in tipo_grafico_diferido:
        st.markdown("<br>", unsafe_allow_html=True)
        chart_cop = st.empty()  



    lista_tiempo=df_ensayo["Indice"].tolist()
    for i in range(len(df_ensayo)):

        tiempo.markdown(f"""<div style="background-color: #e1f5fe;padding: 1rem;border-radius: 0.25rem;text-align: center;font-weight: 500;color: #01579b;">{f'Minuto: {i} - Hora: {lista_tiempo[i]}'}</div>""",unsafe_allow_html=True)

        if 'Gráfico de líneas (temperaturas, presiones, relés, consumo)' in tipo_grafico_diferido:
                
                df_actual_temperaturas = df_temperaturas.iloc[:i + 1]
                df_melted_temperaturas = df_actual_temperaturas.melt(id_vars=['Tiempo','Indice'], var_name='Variable', value_name='Valor')

                fig_temperaturas = px.line(
                    df_melted_temperaturas,
                    x='Tiempo',
                    y='Valor',
                    color='Variable',
                    labels={'Tiempo': 'Tiempo (minutos)', 'Valor': 'Valor'},
                    title='Gráfica de temperaturas',custom_data=['Indice'])
                fig_temperaturas.update_traces(
                    hovertemplate="Tiempo: %{x}<br>Valor: %{y}<br>Hora: %{customdata[0]}<br>Variable: %{fullData.name}<extra></extra>"
                )
                fig_temperaturas.update_layout(
                    width=None,
                    height=500,
                    legend=dict(orientation='h', yanchor='bottom', y=-0.4,title_font_color='black'),
                    xaxis=dict(showgrid=True, gridcolor='lightgray',range=[0,df_temperaturas['Tiempo'].max()],mirror=False,linecolor='black',tickfont=dict(color='black'),title=dict(text='Tiempo (minutos)', font=dict(color='black'))),
                    yaxis=dict(showgrid=True,gridcolor='lightgray',mirror=False,linecolor='black',tickfont=dict(color='black'),title=dict(text='Temperaturas (°C)', font=dict(color='black'))))
                chart_temperaturas.plotly_chart(fig_temperaturas)

                df_actual_presiones = df_presiones.iloc[:i + 1]
                df_melted_presiones = df_actual_presiones.melt(id_vars=['Tiempo','Indice'], var_name='Variable', value_name='Valor')

                fig_presiones = px.line(
                    df_melted_presiones,
                    x='Tiempo',
                    y='Valor',
                    color='Variable',
                    labels={'Tiempo': 'Tiempo (minutos)', 'Valor': 'Valor'},
                    title='Gráfica de presiones',custom_data=['Indice'])
                fig_presiones.update_traces(
                    hovertemplate="Tiempo: %{x}<br>Valor: %{y}<br>Hora: %{customdata[0]}<br>Variable: %{fullData.name}<extra></extra>"
                )
                fig_presiones.update_layout(
                    width=None,
                    height=500,
                    legend=dict(orientation='h', yanchor='bottom', y=-0.4,title_font_color='black'),
                    xaxis=dict(showgrid=True, gridcolor='lightgray',range=[0,df_temperaturas['Tiempo'].max()],mirror=False,linecolor='black',tickfont=dict(color='black'),title=dict(text='Tiempo (minutos)', font=dict(color='black'))),
                    yaxis=dict(showgrid=True,gridcolor='lightgray',mirror=False,linecolor='black',tickfont=dict(color='black'),title=dict(text='Presiones (bar)', font=dict(color='black'))))
                chart_presiones.plotly_chart(fig_presiones)

                df_actual_reles = df_reles.iloc[:i + 1]
                df_melted_reles = df_actual_reles.melt(id_vars=['Tiempo','Indice'], var_name='Variable', value_name='Valor')

                fig_reles = px.line(
                    df_melted_reles,
                    x='Tiempo',
                    y='Valor',
                    color='Variable',
                    labels={'Tiempo': 'Tiempo (minutos)', 'Valor': 'Valor'},
                    title='Gráfica de relés',custom_data=['Indice'])
                fig_reles.update_traces(
                    hovertemplate="Tiempo: %{x}<br>Valor: %{y}<br>Hora: %{customdata[0]}<br>Variable: %{fullData.name}<extra></extra>"
                )
                fig_reles.update_layout(
                    width=None,
                    height=500,
                    legend=dict(orientation='h', yanchor='bottom', y=-0.4,title_font_color='black'),
                    xaxis=dict(showgrid=True, gridcolor='lightgray',range=[0,df_temperaturas['Tiempo'].max()],mirror=False,linecolor='black',tickfont=dict(color='black'),title=dict(text='Tiempo (minutos)', font=dict(color='black'))),
                    yaxis=dict(showgrid=True,gridcolor='lightgray',tickvals=[0, 1], range=[-0.1, 1.1],mirror=False,linecolor='black',tickfont=dict(color='black'),title=dict(text='Valor', font=dict(color='black'))))
                chart_reles.plotly_chart(fig_reles)

                df_actual_consumo = df_consumo.iloc[:i + 1]
                df_melted_consumo = df_actual_consumo.melt(id_vars=['Tiempo','Indice'], var_name='Variable', value_name='Valor')

                fig_consumo = px.line(
                    df_melted_consumo,
                    x='Tiempo',
                    y='Valor',
                    color='Variable',
                    labels={'Tiempo': 'Tiempo (minutos)', 'Valor': 'Valor'},
                    title='Gráfica de consumo',custom_data=['Indice'])
                fig_consumo.update_traces(
                    hovertemplate="Tiempo: %{x}<br>Valor: %{y}<br>Hora: %{customdata[0]}<br>Variable: %{fullData.name}<extra></extra>"
                )
                fig_consumo.update_layout(
                    width=None,
                    height=500,
                    legend=dict(orientation='h', yanchor='bottom', y=-0.4,title_font_color='black'),
                    xaxis=dict(showgrid=True, gridcolor='lightgray',range=[0,df_temperaturas['Tiempo'].max()],mirror=False,linecolor='black',tickfont=dict(color='black'),title=dict(text='Tiempo (minutos)', font=dict(color='black'))),
                    yaxis=dict(showgrid=True,gridcolor='lightgray',mirror=False,linecolor='black',tickfont=dict(color='black'),title=dict(text='Consumo (W)', font=dict(color='black'))))
                chart_consumo.plotly_chart(fig_consumo)

        if 'Diagramas PH-TS' in tipo_grafico_diferido:
                
                tabla_propiedades=pd.DataFrame(columns=['Temperatura (°C)','Presión (bar)','Entalpía (kJ/Kg)','Entropía (kJ/Kg·K)'],index=['1','2','3','3*','4*','4','5'])

                diagrama.data = []

                #Curvas de saturación
                presion = np.linspace(CP.PropsSI('Propane', 'ptriple'), CP.PropsSI('Propane', 'pcrit') , 1000)
                h_liq = [CP.PropsSI('H', 'P', pi, 'Q', 0, "Propane")/1000 for pi in presion]  
                h_vap = [CP.PropsSI('H', 'P', pi, 'Q', 1, "Propane")/1000 for pi in presion]  
                s_liq = [CP.PropsSI('S', 'P', pi, 'Q', 0, "Propane")/1000 for pi in presion]  
                s_vap = [CP.PropsSI('S', 'P', pi, 'Q', 1, "Propane")/1000 for pi in presion]  
                T_liq = [CP.PropsSI('T', 'P', pi, 'Q', 0, "Propane")-273.15 for pi in presion]  
                T_vap = [CP.PropsSI('T', 'P', pi, 'Q', 1, "Propane")-273.15 for pi in presion]  

                tabla_propiedades.loc['1','Presión (bar)']=(df_ensayo.loc[i,'Presion baja']+1)
                tabla_propiedades.loc['1','Temperatura (°C)']=(CP.PropsSI("T", "P", tabla_propiedades.loc['1','Presión (bar)']*(10**5), "Q",1 , "Propane"))/1000
                tabla_propiedades.loc['1','Entalpía (kJ/Kg)']=(CP.PropsSI("H", "P", tabla_propiedades.loc['1','Presión (bar)']*(10**5), "Q",1 , "Propane"))/1000
                tabla_propiedades.loc['1','Entropía (kJ/Kg·K)']=(CP.PropsSI("S", "P", tabla_propiedades.loc['1','Presión (bar)']*(10**5), "Q",1 , "Propane"))/1000

                tabla_propiedades.loc['2','Presión (bar)']=(df_ensayo.loc[i,'Presion baja']+1)
                tabla_propiedades.loc['2','Temperatura (°C)']=df_ensayo.loc[i,'Temperatura aspiracion compresor']
                tabla_propiedades.loc['2','Entalpía (kJ/Kg)']=(CP.PropsSI("H", "P", tabla_propiedades.loc['2','Presión (bar)']*(10**5), "T",tabla_propiedades.loc['2','Temperatura (°C)']+273.15, "Propane"))/1000
                tabla_propiedades.loc['2','Entropía (kJ/Kg·K)']=(CP.PropsSI("S", "P", tabla_propiedades.loc['2','Presión (bar)']*(10**5), "T",tabla_propiedades.loc['2','Temperatura (°C)']+273.15, "Propane"))/1000
  
                tabla_propiedades.loc['3','Presión (bar)']=(df_ensayo.loc[i,'Presion alta']+1)
                tabla_propiedades.loc['3','Temperatura (°C)']=df_ensayo.loc[i,'Temperatura descarga compresor']
                tabla_propiedades.loc['3','Entalpía (kJ/Kg)']=(CP.PropsSI("H", "P", tabla_propiedades.loc['3','Presión (bar)']*(10**5), "T",tabla_propiedades.loc['3','Temperatura (°C)']+273.15, "Propane"))/1000
                tabla_propiedades.loc['3','Entropía (kJ/Kg·K)']=(CP.PropsSI("S", "P", tabla_propiedades.loc['3','Presión (bar)']*(10**5), "T",tabla_propiedades.loc['3','Temperatura (°C)']+273.15, "Propane"))/1000
  
                tabla_propiedades.loc['3*','Presión (bar)']=(df_ensayo.loc[i,'Presion alta']+1)
                tabla_propiedades.loc['3*','Temperatura (°C)']=(CP.PropsSI("T", "P", tabla_propiedades.loc['3*','Presión (bar)']*(10**5), "Q",1 , "Propane"))/1000
                tabla_propiedades.loc['3*','Entalpía (kJ/Kg)']=(CP.PropsSI("H", "P", tabla_propiedades.loc['3*','Presión (bar)']*(10**5), "Q",1 , "Propane"))/1000
                tabla_propiedades.loc['3*','Entropía (kJ/Kg·K)']=(CP.PropsSI("S", "P", tabla_propiedades.loc['3*','Presión (bar)']*(10**5), "Q",1 , "Propane"))/1000

                tabla_propiedades.loc['4*','Presión (bar)']=(df_ensayo.loc[i,'Presion alta']+1)
                tabla_propiedades.loc['4*','Temperatura (°C)']=(CP.PropsSI("T", "P", tabla_propiedades.loc['4*','Presión (bar)']*(10**5), "Q",0 , "Propane"))/1000
                tabla_propiedades.loc['4*','Entalpía (kJ/Kg)']=(CP.PropsSI("H", "P", tabla_propiedades.loc['4*','Presión (bar)']*(10**5), "Q",0 , "Propane"))/1000
                tabla_propiedades.loc['4*','Entropía (kJ/Kg·K)']=(CP.PropsSI("S", "P", tabla_propiedades.loc['4*','Presión (bar)']*(10**5), "Q",0 , "Propane"))/1000

                tabla_propiedades.loc['4','Presión (bar)']=(df_ensayo.loc[i,'Presion alta']+1)
                tabla_propiedades.loc['4','Temperatura (°C)']=df_ensayo.loc[i,'Temperatura salida condensador']
                tabla_propiedades.loc['4','Entalpía (kJ/Kg)']=(CP.PropsSI("H", "P", tabla_propiedades.loc['4','Presión (bar)']*(10**5), "T",tabla_propiedades.loc['4','Temperatura (°C)']+273.15, "Propane"))/1000
                tabla_propiedades.loc['4','Entropía (kJ/Kg·K)']=(CP.PropsSI("S", "P", tabla_propiedades.loc['4','Presión (bar)']*(10**5), "T",tabla_propiedades.loc['4','Temperatura (°C)']+273.15, "Propane"))/1000
  
                tabla_propiedades.loc['5','Presión (bar)']=(df_ensayo.loc[i,'Presion baja']+1)
                tabla_propiedades.loc['5','Temperatura (°C)']=tabla_propiedades.loc['1','Temperatura (°C)']
                tabla_propiedades.loc['5','Entalpía (kJ/Kg)']=tabla_propiedades.loc['4','Entalpía (kJ/Kg)']
                tabla_propiedades.loc['5','Entropía (kJ/Kg·K)']=(CP.PropsSI("S", "P", tabla_propiedades.loc['5','Presión (bar)']*(10**5), "H",tabla_propiedades.loc['5','Entalpía (kJ/Kg)']*1000, "Propane"))/1000
  
                # Diagrama P-h
                puntos_ciclo_ph={'x':[tabla_propiedades.loc['1','Entalpía (kJ/Kg)'],tabla_propiedades.loc['2','Entalpía (kJ/Kg)'],tabla_propiedades.loc['3','Entalpía (kJ/Kg)'],tabla_propiedades.loc['4','Entalpía (kJ/Kg)'],tabla_propiedades.loc['5','Entalpía (kJ/Kg)'],tabla_propiedades.loc['1','Entalpía (kJ/Kg)']],
                                 'y':[tabla_propiedades.loc['1','Presión (bar)'],tabla_propiedades.loc['2','Presión (bar)'],tabla_propiedades.loc['3','Presión (bar)'],tabla_propiedades.loc['4','Presión (bar)'],tabla_propiedades.loc['5','Presión (bar)'],tabla_propiedades.loc['1','Presión (bar)']]}

                diagrama.add_trace(go.Scatter(x=h_liq, y=(presion/1e5),mode='lines', name='Líquido saturado', line=dict(color='blue'),hovertemplate="Presión: %{y:.2f} bar<br>Entalpía: %{x:.2f} kJ/kg"), row=1, col=1)
                diagrama.add_trace(go.Scatter(x=h_vap, y=(presion/1e5),mode='lines', name='Vapor saturado', line=dict(color='red'),hovertemplate="Presión: %{y:.2f} bar<br>Entalpía: %{x:.2f} kJ/kg"), row=1, col=1) 
                diagrama.add_trace(go.Scatter(x=puntos_ciclo_ph['x'],y=puntos_ciclo_ph['y'],mode='lines+markers',name='Ciclo',line=dict(color='black', width=2, dash='solid'),marker=dict(size=7, color='black'),showlegend=True,hovertemplate="Presión: %{y:.2f} bar<br>Entalpía: %{x:.2f} kJ/kg"), row=1, col=1)

                diagrama.update_yaxes(title_text="Presión (bar)",range=[1, 50], row=1, col=1,showgrid=False,mirror=False,zeroline=False,linecolor='black',tickfont=dict(color='black'),title=dict(font=dict(color='black')))
                diagrama.update_xaxes(title_text="Entalpía (kJ/Kg)",range=[200, 750], row=1, col=1,showgrid=False,mirror=False,zeroline=False,linecolor='black',tickfont=dict(color='black'),title=dict(font=dict(color='black')))

                #presion_ticks=[0,10,20,30,40,50,60,70,80]
                #diagrama.update_yaxes(title_text="Presión (bar)", type="log",tickvals=presion_ticks,ticktext=[f"{p:.0f}" for p in presion_ticks],range=[np.log10(CP.PropsSI('CO2', 'ptriple')/1e5), np.log10(CP.PropsSI('CO2', 'pcrit')/1e5)], row=1, col=1)

                # Diagrama T-s
                puntos_ciclo_ts={'x':[tabla_propiedades.loc['1','Entropía (kJ/Kg·K)'],tabla_propiedades.loc['2','Entropía (kJ/Kg·K)'],tabla_propiedades.loc['3','Entropía (kJ/Kg·K)'],tabla_propiedades.loc['4','Entropía (kJ/Kg·K)'],tabla_propiedades.loc['5','Entropía (kJ/Kg·K)'],tabla_propiedades.loc['1','Entropía (kJ/Kg·K)']],
                                 'y':[tabla_propiedades.loc['1','Temperatura (°C)'],tabla_propiedades.loc['2','Temperatura (°C)'],tabla_propiedades.loc['3','Temperatura (°C)'],tabla_propiedades.loc['4','Temperatura (°C)'],tabla_propiedades.loc['5','Temperatura (°C)'],tabla_propiedades.loc['1','Temperatura (°C)']]}

                #puntos_ciclo_ts={'x':[tabla_propiedades.loc['1','Entropía (kJ/Kg·K)'],tabla_propiedades.loc['2','Entropía (kJ/Kg·K)'],tabla_propiedades.loc['3','Entropía (kJ/Kg·K)'],tabla_propiedades.loc['4','Entropía (kJ/Kg·K)'],tabla_propiedades.loc['5','Entropía (kJ/Kg·K)'],tabla_propiedades.loc['1','Entropía (kJ/Kg·K)']],
                #                 'y':[tabla_propiedades.loc['1','Temperatura (°C)'],tabla_propiedades.loc['2','Temperatura (°C)'],tabla_propiedades.loc['3','Temperatura (°C)'],tabla_propiedades.loc['4','Temperatura (°C)'],tabla_propiedades.loc['5','Temperatura (°C)'],tabla_propiedades.loc['1','Temperatura (°C)']]}

                diagrama.add_trace(go.Scatter(x=s_liq, y=T_liq,mode='lines', name='Líquido saturado', line=dict(color='blue'), showlegend=False,hovertemplate="Temperatura: %{y:.2f} °C<br>Entropía: %{x:.2f} kJ/Kg·K"), row=1, col=2)
                diagrama.add_trace(go.Scatter(x=s_vap, y=T_liq,mode='lines', name='Vapor saturado', line=dict(color='red'), showlegend=False,hovertemplate="Temperatura: %{y:.2f} °C<br>Entropía: %{x:.2f} kJ/Kg·K"), row=1, col=2)
                diagrama.add_trace(go.Scatter(x=puntos_ciclo_ts['x'],y=puntos_ciclo_ts['y'],mode='lines+markers',name='Ciclo',line=dict(color='black', width=2, dash='solid'),marker=dict(size=7, color='black'),showlegend=True,hovertemplate="Temperatura: %{y:.2f} °C<br>Entropía: %{x:.2f} kJ/Kg·K"), row=1, col=2)
        
                diagrama.update_yaxes(title_text="Temperatura (°C)",range=[-40, 100], row=1, col=2,showgrid=False,zeroline=False,mirror=False,linecolor='black',tickfont=dict(color='black'),title=dict(font=dict(color='black')))
                diagrama.update_xaxes(title_text="Entropía (kJ/Kg·K)",range=[0, 3], row=1, col=2,showgrid=False,zeroline=False,mirror=False,linecolor='black',tickfont=dict(color='black'),title=dict(font=dict(color='black')))

                # Ajustes finales
                diagrama.update_layout(height=600,width=1200,title_text="Diagramas del ciclo",title_font=dict(size=16,family='Arial'),hovermode="closest",showlegend=False)
                diagrama_placeholder.plotly_chart(diagrama, use_container_width=True,key=f"nombre_{i}")
        
        if 'Gráfico de líneas (COP)' in tipo_grafico_diferido:

            H2=(CP.PropsSI("H", "P", (df_ensayo.loc[i,'Presion baja']+1)*(10**5), "T",df_ensayo.loc[i,'Temperatura aspiracion compresor']+273.15, "Propane"))/1000
            H5=(CP.PropsSI("H", "P", (df_ensayo.loc[i,'Presion alta']+1)*(10**5), "T",df_ensayo.loc[i,'Temperatura salida condensador']+273.15, "Propane"))/1000
            H3=(CP.PropsSI("H", "P", (df_ensayo.loc[i,'Presion alta']+1)*(10**5), "T",df_ensayo.loc[i,'Temperatura descarga compresor']+273.15, "Propane"))/1000

            if df_ensayo.loc[i,'Rele compresor']!=0:
                df_ensayo.loc[i,'COP']=(H2-H5)/(H3-H2)
            else:
                df_ensayo.loc[i,'COP']=0

            df_actual_cop = df_ensayo.loc[:i + 1,['COP','Tiempo','Indice']]
            df_melted_cop = df_actual_cop.melt(id_vars=['Tiempo','Indice'], var_name='Variable', value_name='Valor')
            fig_cop = px.line(
                df_melted_cop,
                x='Tiempo',
                y='Valor',
                color='Variable',
                labels={'Tiempo': 'Tiempo (minutos)', 'Valor': 'Valor'},
                title='Gráfica de coeficientes de rendimiento del ciclo',custom_data=['Indice'])
            fig_cop.update_traces(
                hovertemplate="Tiempo: %{x}<br>Valor: %{y}<br>Hora: %{customdata[0]}<br>Variable: %{fullData.name}<extra></extra>"
            )
            fig_cop.update_layout(
                width=None,
                height=500,
                legend=dict(orientation='h', yanchor='bottom', y=-0.4,title_font_color='black'),
                xaxis=dict(showgrid=True, gridcolor='lightgray',range=[0,df_ensayo['Tiempo'].max()],mirror=False,linecolor='black',tickfont=dict(color='black'),title=dict(text='Tiempo (minutos)', font=dict(color='black'))),
                yaxis=dict(showgrid=True,gridcolor='lightgray',range=[0,3],mirror=False,linecolor='black',tickfont=dict(color='black'),title=dict(text='Valor', font=dict(color='black'))))
            chart_cop.plotly_chart(fig_cop)

        if 'Scada' in tipo_grafico_diferido:

            # Crear una copia de la imagen original
            imagen_actualizada = imagen.copy()
            draw = ImageDraw.Draw(imagen_actualizada)

            # Superponer los datos en la imagen
            font = ImageFont.truetype("letras/Tinos-Regular.ttf", size=30)
            for dato, (x, y) in posiciones.items():
                if dato in df_ensayo.columns and not pd.isna(df_ensayo[dato].iloc[i]):
                    valor = str(df_ensayo[dato].iloc[i])  # Lee el valor del Excel
                    unidad = unidades.get(dato, "")# Obtén la unidad correspondiente (o cadena vacía si no existe)
                    texto = f"{valor} {unidad}"  # Concatena el valor y la unidad
                else:
                    texto='--'
                draw.text((x, y), texto, fill="red", font=font)  # Dibuja el texto en la imagen

            # Mostrar la imagen actualizada en Streamlit
            imagen_placeholder.image(imagen_actualizada, caption="Instalación de R-290", use_container_width=True)












        sleep(velocidad_reproduccion)
        #chart_temperaturas = st.empty()  
        #chart_presiones = st.empty() 
        #chart_reles = st.empty() 
        #chart_consumo = st.empty() 