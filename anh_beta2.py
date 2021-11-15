echo "# streamlit-to-heroku-tutorial" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M master
git remote add origin https://github.com/your_username/your_repo_name.git
git push -u origin master



import streamlit as st
import pandas as pd
import numpy as np
import scipy
import plotly as px
import plotly_express as px
import plotly.graph_objects as go
import plotly.offline as py
import plotly.express as px
import math
import time
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import base64
import csv
import pylab as pl
import sys
from datetime import datetime
from plotly import tools
#import db


######################################################################################


#Título
#col1, mid, col2 = st.columns([5,5,60])
#with col1:
#st.image('ANH.png', width=300)
    #st.image('FCYT.png', width=40)
#with col2:
st.title('Agencia Nacional de Hidrocarburos')
st.header('Centro de Investigación Regulatorio Plural')

######################################################################################
#Barra lateral
st.sidebar.header("Datos de entrada")
#GEOMETRÍA DEL MOTOR
st.sidebar.subheader("Geometría del motor")
num_rc = (st.sidebar.number_input("Relación de compresión"))
num_lp = (st.sidebar.number_input("Carrera del pistón [m]"))
num_dp = (st.sidebar.number_input("Diámetro del cilindro [m]"))
num_lb = (st.sidebar.number_input("Longitud de biela [m]"))
num_nc = (st.sidebar.number_input("Nº de cilindros del motor"))
num_rac = (st.sidebar.number_input("Relación aire combustible"))

#CONSTANTES FÍSICAS
st.sidebar.subheader("Constantes físicas")
num_lambda = int(st.sidebar.number_input("Lambda"))
num_cgi = int(st.sidebar.number_input("Constante de los Gases Ideales [kJ/kg·K]"))
num_g = int(st.sidebar.number_input("Aceleración de la gravedad [m/s2]"))
num_temp_amb = int(st.sidebar.number_input("Temperatura ambiente [ºC]"))
num_pre_amb = int(st.sidebar.number_input("Presión ambiente [kPa]"))
num_cp = int(st.sidebar.number_input("Calor específico del aire a presión constante [kJ/kg·K]"))
num_cv = int(st.sidebar.number_input("Calor específico del aire a volumen constante [kJ/kg·K]"))

#VARIABLE INTERMITENTE
st.sidebar.subheader("Variable intermitente")
num_alt = (st.sidebar.number_input("Ingrese altitud [km]"))
#num_temp = int(st.sidebar.number_input("Temperatura [ºC]"))
#num_pre = int(st.sidebar.number_input("Presión [kPa]"))

#OTROS DATOS PARA EL FUNCIONAMIENTO DEL MOTOR
st.sidebar.subheader("Funcionamiento del motor")
num_poder_cal_comb = int(st.sidebar.number_input("Poder calorífico del combustible [kJ/kg]"))
num_rend_comb = int(st.sidebar.number_input("Rendimiento de la combustión"))
num_rend_mec = int(st.sidebar.number_input("Rendimiento mecanico"))
num_reg_giro_motor = int(st.sidebar.number_input("Regimen de giro del motor [RPM]"))
num_porc_res_comb = int(st.sidebar.number_input("Porcentaje de residuos de combustión"))
num_giro_nom_mot = int(st.sidebar.number_input("Giro nominal del motor [RPM]"))
option = st.sidebar.selectbox(
    'Seleccione los tiempos del motor',
     ('dos tiempos', 'cuatro tiempos'))

#VARIABLES FIJAS
st.sidebar.subheader("Variables fijas")
num_pres_nmar = int(st.sidebar.number_input("Presión a nivel del mar [kPa]"))
num_temp_nmar = int(st.sidebar.number_input("Temperatura a nivel del mar [ºC]"))

#TIPO DE ANÁLISIS QUE DESEA OBTENER
st.sidebar.subheader("Seleccione el tipo de análisis que desea obtener")

if st.sidebar.button('Geometría y dinámica del motor'):
    st.subheader('GEOMETRÍA Y DINÁMICA DEL MOTOR')
     
    #Resultados - Geometría
    r_dp=num_dp/2
    AreaPiston=(scipy.pi/4)*(r_dp*r_dp)
    st.write('Área de Pistón', AreaPiston)
    RBS=(num_dp/num_lp)
    st.write('Relación Diámetro del Cilindro con la Carrera del Pistón', RBS)
    RBM=(2*num_lb)/num_lp
    st.write('Relación Biela - Manivela', RBM)
    Vd=(scipy.pi/4)*(num_dp*num_dp)*(num_lp)
    st.write("Volumen desplazado", Vd)
    Vdtotal=num_nc*Vd
    st.write("Volumen desplazado total", Vdtotal)
    st.write("Relación de compresión", num_rc)
   
    #Up=2*num_lp*num_giro_nom_mot
    #st.write("Up", Up)
    if (num_rc<=1):
        Vc="No calculable"
        st.write("Volumen de la cámara de combustión o volumen muerto", Vc)
        VPMS=Vc
        st.write("Volumen en el punto muerto superior", VPMS)
        VPMI="No calculable"
        st.write("Volumen en el punto muerto inferior", VPMI)
    else:
        Vc=Vd/(num_rc-1)
        st.write("Volumen de la cámara de combustión o volumen muerto", Vc)
        VPMS=Vc
        st.write("Volumen en el punto muerto superior", VPMS)
        VPMI=Vc+Vd
        st.write("Volumen en el punto muerto inferior", VPMI)
    w=((2*scipy.pi)/60)*num_giro_nom_mot
    st.write("Velocidad angular del cigüeñal", w)
    

    #Resultados Dinámica del Pistón

    angulo=0
    r=num_lp/2
    lamb=r/num_lb
    with open('pos4.csv', 'w', newline='') as  f:
        writer = csv.writer(f)
        list=["angulo","posicion"]
        writer.writerow(list)
        while angulo<=360:
            angulo_doble=(2*angulo*math.pi)/180
            angulo_simple=(angulo*math.pi)/180
            Xp=r*(((lamb/4)*(1-math.cos(angulo_doble)))+(1-math.cos(angulo_simple)))
            #a=num_rc+i*50
            list=[angulo,Xp]
            #st.text(list)
            writer.writerow(list)
            angulo=angulo+1

    def load_data(nrows):
        data = pd.read_csv('pos4.csv', nrows=nrows)
        return data
    data_load_state = st.text('Loading data...')
    weekly_data = load_data(360)
    st.subheader('Posición del pistón')
    st.write(weekly_data)
    df=pd.DataFrame(weekly_data[:360], columns=['posicion'])
    #Bar Chart
    st.line_chart(df)
    
    #velocidad
    angulo1=0
    with open('velocidad1.csv', 'w', newline='') as  f:
        writer = csv.writer(f)
        list=["angulo","velocidad"]
        writer.writerow(list)
        while angulo1<=360:
            angulo_doble=(2*angulo1*math.pi)/180
            angulo_simple=(angulo1*math.pi)/180
            Vp=r*w*((lamb/2)*math.sin(angulo_doble)+math.sin(angulo_simple))
            #a=num_rc+i*50
            list=[angulo1,Vp]
            #st.text(list)
            writer.writerow(list)
            angulo1=angulo1+1

    def load_data(nrows):
        data = pd.read_csv('velocidad1.csv', nrows=nrows)
        return data
    data_load_state = st.text('Loading data...')
    weekly_data = load_data(360)
    st.subheader('Velocidad del pistón')
    st.write(weekly_data)
    df=pd.DataFrame(weekly_data[:360], columns=['velocidad'])
    #Bar Chart
    st.line_chart(df)
    #Gráficas
    
    #aceleracion
    angulo2=0
    with open('aceleracion1.csv', 'w', newline='') as  f:
        writer = csv.writer(f)
        list=["angulo","aceleracion"]
        writer.writerow(list)
        while angulo2<=360:
            angulo_doble=(2*angulo2*math.pi)/180
            angulo_simple=(angulo2*math.pi)/180
            Ap=-r*w*w*(math.cos(angulo_simple)+(lamb*math.cos(angulo_doble)))
            #a=num_rc+i*50
            list=[angulo2,Ap]
            #st.text(list)
            writer.writerow(list)
            angulo2=angulo2+1

    def load_data(nrows):
        data = pd.read_csv('aceleracion1.csv', nrows=nrows)
        return data
    data_load_state = st.text('Loading data...')
    weekly_data = load_data(360)
    st.subheader('Aceleracion del pistón')
    st.write(weekly_data)
    df=pd.DataFrame(weekly_data[:360], columns=['aceleracion'])
    #Bar Chart
    st.line_chart(df)


    
#################################################################################
#Resultados termodinámica del motor
if st.sidebar.button('Termodinámica del motor'):
    st.header('TERMODINÁMICA DEL MOTOR')
    #Gráficas
    RBM=(num_dp/num_lp)
    #=((2*num_lb)/num_lp)
    st.write('Relación Biela - Manivela', RBM)
    gravedad=9.8 #Unidades N/Kg
    Po=101.325 #Unidades kPa
    dens_aire0=1.2250
    R=287 #Unidades m2/s2K
    num_a=-6.5
    num_t0=298.15
    num_t1=num_t0+num_a*(num_alt)
    num_t2=num_t1-273.15
    st.write('La temperatura es', num_t2, 'ºC es a una altura de', num_alt, 'km')

    dens_aire=dens_aire0*((num_t1/num_t0)**(-1-(gravedad/(num_a*R)))) #Unidades kg/m3
    st.write('La densidad', dens_aire, 'kg/m3 es a una altura de', num_alt, 'km')
    alfa=(dens_aire*gravedad)/Po
    st.write('Valor de alfa =', alfa, '1/m')
    num_pres1=Po*math.exp(-alfa*num_alt)
    st.write('La presión', num_pres1, 'kPa es a una altura de', num_alt, 'km')
    
    Cp=1005

    

    #temp_comp=15+273.15
    #num_t1_g=num_t
    #st.write('Temperatura a la altura de', num_alt, 'es de', num_t1_g)



    col1, mid, col2 = st.columns([10,2,10])
    with col1: 
        #PROCESO DE ADMISIÓN
        st.subheader('1. PROCESO DE ADMISIÓN')
        #CALCULO DE LA PRESIÓN DE ADMISIÓN
        Pk=2*num_pres1*0.001 #MPa
        st.write('Presión Pk es', Pk, 'MPa')
        kn=3.25 #Coeficiente total que se encuentra entre el rango de 2.5 a 4 la formula es beta2+epsilon
        st.write('kn es igual a', kn)
        Wad=50 #Velocidad media del aire en los motores diesel está en el rango de 30 a 70 m/s
        st.write('La velocidad media del aire es', Wad, 'm/s')
        #Se debe seleccionar el coeficiente polintrópico de compresión del compresor 
        nk=1.5
        Tk=num_t1*((Pk/(num_pres1*0.001))**((nk-1)/nk))
        st.write('Tk es', Tk, 'K')
        dens_k=((28.96*Pk)/(8314*Tk))*(10**6)
        st.write('La densidad es', dens_k)
        Pa= Pk-(kn*((Wad**2)/2)*dens_k*(10**(-6)))
        st.write('Presión de admisión es', Pa, 'MPa')

        #CÁLCULO DE LA TEMPERATURA DE ADMISIÓN
        delta_t=2.5 #K
        Tr=800 #El valor está entre 700 a 900
        Epsilon_ta=num_rc #Valor asumido
        Pr=0.94*Pk #Presion de gases residuales la formula es (0.75 - 0.98)Pk
        st.write('Presión de gases residuales es', Pr)
        Yr=((Tk+delta_t)/Tr)*(Pr/((Epsilon_ta*Pa)-Pr))
        st.write('Coeficiente de gases residuales igual a', Yr)
        Ta=(Tk+delta_t+(Yr*Tr))/(1+Yr)
        st.write('Temperatura de admisión es', Ta, 'K')

        #CÁLCULO DEL VOLUMEN ESPECÍFICO DE ADMISIÓN
        Ua=28.8503 #Kg/kMol es la Masa molar del aire
        Va=0.008314* (Ta/(Ua*Pa))
        st.write('El volumen específico de admisión es', Va)
        
    with col2:
        #PROCESO DE COMPRESIÓN
        st.subheader('3. PROCESO DE COMPRESIÓN')
        #Cálculo de presión de compresión
        n1=1.35 #Coeficiente politrópico su valor está entre 1.32 - 1.39
        Pc=Pa*Epsilon_ta**n1
        st.write('La presión de compresión es', Pc, 'MPa')
        #Cálculo de temperatura de compresion
        Tc=Ta*Epsilon_ta**(n1-1)
        st.write('La temperatura de compresión es', Tc, 'K')
        #Cálculo del volumen específico de compresión
        Vc=Va/Epsilon_ta
        st.write('El volumen específico de compresión es', Vc, 'm3/kg')
        #Cálculo del volumen específoc instantáneo
        
        theta1=35
        theta=(theta1*math.pi)/180
        #V_ins=(Va/Epsilon_ta)*(((Epsilon_ta-1)/2)*(1+(1/RBM)-math.cos(theta)+(-1/RBM)*math.sqrt(1-(RBM*RBM)*((math.sin(theta))**2)))+1)
        #st.write('El volumen específico instantaneo es', V_ins)
        

    col1, mid, col2 = st.columns([10,2,10])
    with col1: 
        #PROCESO DE COMBUSTION
        st.subheader('3. PROCESO DE COMBUSTIÓN')
        alfa_comb=1.5
        mc=190
        gC=0.86
        gH=0.13
        gO=0.01
        Lo=(1/0.21)*((gC/12)+(gH/4)-(gO/32))
        st.write('Lo es igual a', Lo)
        M1=alfa_comb*Lo+(1/mc)
        st.write('Cantidad de mezcla es', M1, 'kmol/kg')
        MO=0.21*(alfa_comb-1)*Lo
        st.write('Existen ', MO, '[kmol/kg] de oxígeno')
        MN=0.79*alfa_comb
        st.write('Existen ', MN, '[Kmol/kg] de nitrógeno')
        MCO2=gC/12
        st.write('Existen ', MCO2, '[kmol/kg]  de anhidrido carbónico')
        MH2O=gH/2
        st.write('Existen ', MH2O, ' [kmol/Kg] de agua' )
        M2=MO+MN+MCO2+MH2O
        st.write('Cantidad de mezcla 2 es', M2, 'kmol/kg')
        delta_M=M2-M1
        Uo_max=1+(delta_M/M1)
        st.write('Coeficiente de variación molecular es', Uo_max, '[kmol/kg]')
        E_comb=1 #Efectividad de la combustion de un combustible es 1
        Hi=42500 #Poder calorífica inferior del combustible en este caso diesel
        qz=(E_comb*Hi)/(1+((1+Yr)*alfa_comb))
        st.write('Calor específico total de la combustión es', qz, '[kJ/kg]')
        E2=0.002*qz*(num_rc/Va)
        st.write('E2 es', E2)
        


        st.text('Presión')
        st.text('Temperatura')
        st.text('Volumen')
        st.text('Entropía')
        st.text('Presión media efectiva')
    with col2:
        #PROCESO DE ESCAPE
        st.subheader('4. PROCESO DE ESCAPE')
        st.text('Presión')
        st.text('Temperatura')
        st.text('Volumen')
        st.text('Entropía')
        st.text('Cantidad de calor extraído')
   


#################################################################################

if st.sidebar.button('Gráficas de simulación de motores diesel'):
    st.subheader('Gráficas de simulación de motores diesel')
    #Gráficas
    st.text('Potencia del motor')
    st.text("Potenciia al freno")
    st.text("Presión media efectiva")
    st.text('Consumo específico')
    #Resultados de Rendimiento
    st.text('Rendimiento térmico')
    st.text('Rendimiento volumétrico del aire')
    st.text('Eficiencia Carnot')
    st.text('Rendimiento de conversión de fuel')


    
    
if st.sidebar.button('Resumen de cálculos'):
    st.subheader('RESUMEN DE CÁLCULOS')
    st.text('sdhfdf ')

else:
    st.subheader('OBJETIVO DEL SIMULADOR')
    st.text('Apoyar en el cálculo termodinámico y de rendimiento de un motor diesel')
    st.subheader('CARACTERÍSTICAS DE UN MOTOR DIÉSEL')
    st.text('Entre sus principales características tenemos: 1. El proceso de combustión se inicia ')
    st.text('1. El proceso de combustión se inicia mediante un proceso de autoencendido de la ')
    st.text('   mezcla del combustible gracias a las altas temperaturas que se generan por la ') 
    st.text('   compresión del aire.')
    st.text('2. No existe una zona definida donde se produzca la combustión sino que aparece muchos')
    st.text('frentes de llamas que depende del chorro del combustible inyectado y del movimiento del')
    st.text('aire en la cámara de combustión.')
    st.text('3. La temperatura interna del cilindro está en el rango de 600ºC a 800ºC.')
    st.text('4. El motor está diseñado para soportar mayores relaciones de compresión que el motor')
    st.text('de gasolina.')
    
    st.subheader('FUNCIONAMIENTO DE UN MOTOR DIESEL')
    #   col1, mid, col2 = st.columns([15,1,15])
    #with col2: 
    st.markdown("![Alt Text](https://upload.wikimedia.org/wikipedia/commons/d/dc/4StrokeEngine_Ortho_3D_Small.gif)")
    #with col2: 
    #    st.markdown("![Alt Text](https://i.pinimg.com/originals/3c/ed/05/3ced057c6ac0f795a2cfefe06263bb30.gif)")
    st.text('1. ADMISIÓN es la etapa donde el pistón realiza un trayecto desde el punto muerto PMS')
    st.text('   al punto muerto inferior PMI. En ese momente las válvulas de admisión están abiertas') 
    st.text('   y las válvulas de escape cerradas.')
    st.text('2. COMPRESIÓN es la etapa donde las válvulas de admisión y escape se encuentran cerradas')
    st.text('y el pistón se desplaza desde el PMI al PMS comprimiendo el fluido dentro del cilindro.')
    st.text('En esta etapa se inyecta el combustible y se produce la combustión.')
    st.text('3. EXPANSIÓN es producto de la presión generada por los gases contenidos de las combustión')
    st.text('que provoca que el émbolo se desplace desde el PMS al PMI.')
    st.text('4. ESCAPE en esta etapa se abre la válvula de escape que se ubica en el PMI y el pistón')
    st.text('comienza a desplazarse hacia el PMS expulsando los gases quemados hacia el exterior.')
#n1=int(num_lambda)
#n2=int(num_cgi)
#sum=(n1+n2)*scipy.pi
#st.write("La",sum)
#st.write(scipy.pi)
#Apiston=(scipy.pi/4)*(num_dc*num_dc)
#st.write("Área del pistón", Apiston)
#BS=(num_dc/num_carr_p)
#st.write("BS", BS)
#r=num_carr_p/2
#st.write("r", r)
#Vd=(scipy.pi/4)*(num_dc*num_dc)*(num_carr_p)
#st.write("Volumen desplazado", Vd)
#Vdtotal=num_nc*Vd
#st.write("Volumen desplazado total", Vdtotal)
#Up=2*num_carr_p*num_giro_nom_mot
#st.write("Up", Up)
#Vc=Vd*(num_rc+1)
#st.write("Vc", Vc)
#VBDC=Vc+Vd
#st.write("VBDC", VBDC)
#VTDC=Vc
#st.write("VTDC", VTDC)
#w=((2*scipy.pi)/60)*num_giro_nom_mot
#st.write("w", w)
#Xp=r*math.cos(angulo(math.pi/3))+5
#st.write("Xp", Xp)
#ntermico=Wneto/qentrada
