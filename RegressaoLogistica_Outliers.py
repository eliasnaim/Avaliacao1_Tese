# Importanto as bibliotecas

from scipy.optimize import curve_fit
from matplotlib import pyplot
import pandas as pd
import numpy as np
import requests
import warnings

 
# Definição da função
def objective(X_3, a, b, c, d):
	return a + (( b - a ) / ( 1 + np.exp (( c - X_3 ) / d )))


# Obtenção dos dados no OSM utilizando a API do OHSOME
    
OHSOME_API = "https://api.ohsome.org/v1"
metadata = requests.get(OHSOME_API+"/metadata").json()
TIME_MONTHLY = "2008-01-01/2022-07-01/P1M"

#lista das coordenadas

BBOX = {

}

def elements(agg,**params):
    res = requests.get(OHSOME_API+"/elements"+agg,params)
    return res

#Aplicacao do Experimento
    
chaves=[]
overflows_tot=[]

for chave, valor in BBOX.items():

    res = elements("/count", keys=None, values=None, bboxes=BBOX[chave], time=TIME_MONTHLY, types="way,node")


    body = res.json()
    df = pd.DataFrame(body['result'])
    df.timestamp = pd.to_datetime(df.timestamp)
# Obtenção das curvas de crescimento
    X = df.timestamp.values.astype(float).reshape(-1, 1)
    Y = df.value.values
    #X_3=(pd.to_timedelta(df.timestamp-df.timestamp[0], unit='d').dt.days)
    numeros = []
    for i in range(len(Y)):
        numeros.append(i)   
    numeros2 = np.array(numeros)
    X_3= numeros2
    Y_3=(np.array(Y))

    warnings.filterwarnings("error",category=RuntimeWarning)


    overflows = 0

    try:

        #regressão

        popt, _ = curve_fit(objective, X_3, Y_3, method="lm", maxfev=70000)
        a, b, c, d = popt

        pyplot.scatter(X_3, Y_3)

        x_line = X_3
        x_line2 = np.asarray(X_3)

        y_line = objective(x_line, a, b, c, d)
        figure = pyplot.plot(x_line2, y_line, 'green', color='red')
        figure = pyplot.gcf()
        pyplot.savefig(f"C:/Users/elias/Desktop/Aplicações_Tese_Resultados/Avaliação_01/Regressoes/{chave}.png")
        pyplot.clf()

    except:
        overflows += 1
    print(overflows)
    
    
#Saída dos Dados
    
saida=pd.DataFrame(overflows_tot,index=chaves)
saida.to_csv("C:/Users/elias/Desktop/Aplicações_Tese_Resultados/Avaliação_01/Overflow_txt/overflows.txt")
