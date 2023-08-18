# -*- coding: utf-8 -*-
"""Analisis de Resultados.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RBcsdQjMF_V90q8dsTuMQnyUIANcj6Mg

#Carga de datos y librerias
"""

#Pandas es utilizado para leer los set de datos
import pandas as pd
#Numpy es utilizado para generar las series de datos a graficar
import numpy as np
#Seaborn es utilizado para generar los gráficos
import seaborn as sns
import matplotlib.pyplot as plt
#Se importan modulos estadisticos para generar test de hipotesis, entre otros
from sklearn.preprocessing import StandardScaler,MinMaxScaler
#Módulos implementa funciones que evalúan el error de predicción para propósitos específicos
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_absolute_percentage_error as mape
from sklearn.metrics import mean_squared_error as mse

#Dividir arreglos o matrices en subconjuntos aleatorios de tren y prueba
from sklearn.model_selection import train_test_split

#Biblioteca de Redes Neuronales
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential,model_from_json
from keras.layers import Dropout, LSTM, Dense, Activation,Input
from tensorflow.keras.optimizers import SGD, Adam, RMSprop
from keras.callbacks import EarlyStopping, ModelCheckpoint

from hyperopt import Trials, STATUS_OK, tpe, hp, fmin, space_eval
from sklearn.model_selection import cross_val_score, KFold, cross_val_predict, TimeSeriesSplit
import time

pip install scikit-posthocs --quiet

# Para acceder a los archivos del gdrive
from google.colab import drive
drive.mount('/content/gdrive/')

cd /content/gdrive/MyDrive/Tesis/Datos-ConsumoElectrico/Resultados_csv

"""#Analsisis de Error de cada modelo"""

result_mlp=pd.read_csv('results_MLP_CE.csv',index_col=0)
result_gru=pd.read_csv('results_GRU_CE.csv',index_col=0)
result_lstm=pd.read_csv('results_LSTM_CE.csv',index_col=0)
result_cnn=pd.read_csv('results_CNN_CE.csv',index_col=0)
result_transformer=pd.read_csv('results_Transformer_CE.csv',index_col=0)
result_svr=pd.read_csv('results_SVR_CE.csv',index_col=0)
result_elm=pd.read_csv('results_ELM_CE.csv',index_col=0)

print(result_mlp.shape)
print(result_gru.shape)
print(result_lstm.shape)
print(result_cnn.shape)
print(result_transformer.shape)
print(result_svr.shape)
print(result_elm.shape)

"""##ELM"""

result_elm = result_elm.sort_values(by='MSE', ascending=True)
print("Top 5 mejores resultados")
result_elm.head(5)

"""##SVR"""

result_svr = result_svr.sort_values(by='MSE', ascending=True)
print("Top 5 mejores resultados")
result_svr.head(5)

"""##MLP"""

result_mlp = result_mlp.sort_values(by='MSE', ascending=True)
print("Top 5 mejores resultados")
result_mlp.head(5)

"""##GRU"""

result_mlp = result_gru.sort_values(by='MSE', ascending=True)
print("Top 5 mejores resultados")
result_mlp.head(5)

"""##LSTM"""

result_lstm = result_lstm.sort_values(by='MSE', ascending=True)
print("Top 5 mejores resultados")
result_lstm.head(5)

"""##CNN"""

result_cnn= result_cnn.sort_values(by='MSE', ascending=True)
print("Top 5 mejores resultados")
result_cnn.head(5)

"""##Transformer"""

result_transformer= result_transformer.sort_values(by='MSE', ascending=True)
print("Top 5 mejores resultados")
result_transformer.head(5)

"""#Se verifica normalidad de los errores de test"""

from scipy.stats import shapiro
import numpy as np
from scipy.stats import friedmanchisquare
from scikit_posthocs import posthoc_nemenyi
import scikit_posthocs as sp

def test_shapiro(data):
  stat, p = shapiro(data)
  print('stat=%.3f, p=%.3f' % (stat, p))
  if p > 0.05:
    print('Probably Gaussian')
    print("")
  else:
    print('Probably not Gaussian')
    print("")

print("Test de shapiro a Resutl MLP")
test_shapiro(result_mlp["MSE"])

print("Test de shapiro a Resutl ELM")
test_shapiro(result_elm["MSE"])

print("Test de shapiro a Resutl SVR")
test_shapiro(result_svr["MSE"])

print("Test de shapiro a Resutl GRU")
test_shapiro(result_gru["MSE"])

print("Test de shapiro a Resutl LSTM")
test_shapiro(result_lstm["MSE"])

print("Test de shapiro a Resutl CNN")
test_shapiro(result_cnn["MSE"])

print("Test de shapiro a Resutl transformer")
test_shapiro(result_transformer["MSE"])

def grafico_distribucion(data):
  plt.subplots(figsize=(7,3))
  sns.histplot(x=data,kde=True,color="blue",bins=30)
  plt.tight_layout()
  plt.show()

grafico_distribucion(result_mlp["MSE"])
grafico_distribucion(result_cnn["MSE"])
grafico_distribucion(result_lstm["MSE"])
grafico_distribucion(result_transformer["MSE"])
grafico_distribucion(result_gru["MSE"])
grafico_distribucion(result_svr["MSE"])
grafico_distribucion(result_elm["MSE"])

"""## Test de Friedman

"""

# Convertir los datos en un array 2D
data = np.array([result_lstm["MSE"],result_svr["MSE"],result_elm["MSE"], result_cnn["MSE"],result_gru["MSE"],result_mlp["MSE"],result_transformer["MSE"]])

# Realizar el test de Friedman
statistic, p_value = friedmanchisquare(*data)
print('stat=%.3f, p=%.3f' % (statistic, p_value))
nivel_significancia = 0.05
# Verificar si se rechaza o no la hipótesis nula
if p_value < nivel_significancia:
    print("Se rechaza la hipótesis nula. Hay diferencias significativas entre las medianas de los grupos.")
else:
    print("No se rechaza la hipótesis nula. No hay diferencias significativas entre las medianas de los grupos.")

"""kruskal"""

from scipy.stats import kruskal
# Convertir los datos en un array 2D
data = np.array([result_lstm["MSE"],result_svr["MSE"],result_elm["MSE"], result_cnn["MSE"],result_gru["MSE"],result_mlp["MSE"],result_transformer["MSE"]])

# Realizar el test de Friedman
statistic, p_value = kruskal(*data)
print('stat=%.3f, p=%.3f' % (statistic, p_value))
nivel_significancia = 0.05
# Verificar si se rechaza o no la hipótesis nula
if p_value < nivel_significancia:
    print("Se rechaza la hipótesis nula. Hay diferencias significativas entre las medianas de los grupos.")
else:
    print("No se rechaza la hipótesis nula. No hay diferencias significativas entre las medianas de los grupos.")

"""## post-hoc 1"""



# Combinar los datos en un DataFrame
data_mse = pd.DataFrame({'LSTM':result_lstm["MSE"],"SRV":result_svr["MSE"], "ELM":result_elm["MSE"], 'CNN':result_cnn["MSE"], 'MLP': result_mlp["MSE"],'GRU': result_gru["MSE"],'Transformer':result_transformer["MSE"]})
data_time = pd.DataFrame({'LSTM':result_lstm["time"],"SRV":result_svr["time"], "ELM":result_elm["time"], 'CNN':result_cnn["time"], 'MLP': result_mlp["time"],'GRU': result_gru["time"],'Transformer':result_transformer["time"]})

posthoc_df = sp.posthoc_mannwhitney([result_lstm["MSE"],result_svr["MSE"],result_elm["MSE"],result_cnn["MSE"],result_mlp["MSE"],result_gru["MSE"],result_transformer["MSE"]], p_adjust = 'bonferroni')
group_names= ["LSTM", "SRV","ELM","CNN","MLP","GRU","Transformer"]
posthoc_df.columns= group_names
posthoc_df.index= group_names
posthoc_df.style.applymap(lambda x: "background-color:violet" if x<0.05 else "background-color: white")

sp.posthoc_nemenyi_friedman(data_mse.T.T)

data_mse.describe()

data_time.describe()