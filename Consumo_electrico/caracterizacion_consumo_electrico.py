# -*- coding: utf-8 -*-
"""Caracterizacion_Consumo Electrico.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1M4rVHlh--1R2IgJL0Q-QOKludr79lxkJ

**Preprocesamiento de la base de datos de Consumo Electrico**

Este archivo consta de los codigos y conclusiones de:
* Se obtiene series de tiempo
* Caracerizacion de la base de datos

# Carga de Librerias y Datos

*Se importan los módulos necesarios para trabajar*
"""

#Pandas es utilizado para leer los set de datos
import pandas as pd
#Numpy es utilizado para generar las series de datos a graficar
import numpy as np
#Se importan modulos estadisticos para generar test de hipotesis, entre otros
from statsmodels.tsa.stattools import adfuller

"""*Se carga base de datos*"""

# Para acceder a los archivos del gdrive
from google.colab import drive
drive.mount('/content/gdrive/')

cd /content/gdrive/MyDrive/Tesis/Datos-2

df=pd.read_csv('df_EDA.csv',
                parse_dates={'dt':['Date','time']},
                infer_datetime_format=True,
                low_memory=False,
                index_col='dt')

df.info()

df.shape

## resampling of data over hour
df = df.resample('D').mean()
df.shape

"""#Caracterizar base de datos

Las caracteristicas a analizar son las siguientes:
* 1.Variables endógenas o exógenas
* 2.Variables univariantes o multivariantes
* 3.Serie continua o no continua
* 4.Serie estacionario o no estacionario
* 5.Serie desestructurada o estructurada
* 6.Complejidad

1.**Variables endógenas o exógenas**:

Para determinar estas variables, el investigador debe analizar y decidir cuales y cuantas existen. A continuación se expone la justificación y las elecciones: Se considera que la varible endogena corresponde a la variable objetivo "Global_active_power". Todas las demás corresponden a varibles exogenas. De esta manera, se tiene 1 variable endogena y 7 variables exogenas que son:

* Global_active_power
* Global_reactive_power
* Voltage
* Global_intensity
* Sub_metering_1
* Sub_metering_2
* Sub_metering_3
* other_consumption

2.**Variables univariantes o multivariantes:**

Para determinar estas variables, el investigador debe analizar y decidir cuales y cuantas existen. A continuación se expone la justificación y las elecciones: El problema claramente es multivariante, pero para ser más precisos, se utilizarán 7 variables de entrada y una variable de salida. De esta manera, es problema es multivariable en las entradas y univariante en la salida.

3.**Series con muestreo regular o irregular:**

Para determinar esta caracteristica, el investigador debe analizar y decidir si la serie es continua o no. A continuación se expone la justificación y la elección: Se considera que la serie claramente tiene un muestre regular, ya que no existen mediciones faltantes, segun el EDA realizado.

4.**Serie estacionario o no estacionario:**

Comprobar la estacionariedad de este problema, se realiza la prueba estadistica "Augmented Dickey-Fuller Test (ADF)". El nivel de significancia usado sera de 1%. De esta manera, se contabiliza cuantas series son estacionarias y cuantas no, de tal manera que si si la mayoria de las series son estacionaria, el problema se considera estacionario, analogo para el caso de no estacionariedad

Prueba Dickey Fuller

* H0 = serie de tiempo posee raíz unitaria y no es estacionaria.

* H1 = serie de tiempo no posee raíz unitaria y es estacionaria.
si el valor P en la prueba Dickey Fuller es menor que el nivel de significación (0.01) se rechaza la hipótesis nula.
"""

stat, p, lags, obs, crit, t = adfuller(df.Global_active_power)
  #print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
  print('Probably not Stationary')
else:
  print('Probably Stationary')

"""**insight**: Se conluye por el test que es una serie estacionaria


---

5.**Serie desestructurada o estructurada:**


6.**Complejidad**
"""

pip install MFDFA

from MFDFA import MFDFA
from MFDFA import fgn

# Seleccione una banda de retrasos, que son enteros
lag = np.array([1,2,3,4,5,6,7,8,9,10,12,14,18,20,25,30,35,40])

resul=[]

#Seleccione una lista de poderes q
q = [1, 2, 5, 8, 10]

#El orden del ajuste del polinomio
order = 2

#MFDFA:
lag, dfa = MFDFA(df.Global_active_power.values, lag = lag, q = q, order = order)
H = np.polyfit(np.log(lag[:]), np.log(dfa[:]),1)[0]
mediaAux = round(np.mean(H),2)
print(f"El MFDFA  es: {mediaAux}")

"""**insight**: Conplejidad de la serie de tiempo es de 1.09%


---
"""