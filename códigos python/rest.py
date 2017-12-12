import numpy as np
from flask import Flask
from flask_cors import CORS, cross_origin
import pandas as pd
import MySQLdb
import urllib, json
from MySQLdb.converters import conversions
from MySQLdb.constants import FIELD_TYPE

#convertendo o tipo decimal do mysql para float ( gera erro caso tente fazer alguma conta usando decimal)
conversions[FIELD_TYPE.DECIMAL] = float
conversions[FIELD_TYPE.NEWDECIMAL] = float

#conexão com o banco
mydb = MySQLdb.connect(host='0.0.0.0',
    user='',
    passwd='',
    db='')

cursor = mydb.cursor()

#configurando o flask para gerar o REST e usando um módulo CORS para evitar o bloqueio do navegador
app = Flask(__name__)
CORS(app)


#método para calcular a distância entre pontos LAT/LONG
def distanciaKmLatLong(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km

@app.route("/datas")
def retornaDatas():
    query = "select distinct DATE_FORMAT(dataHora,'%d/%m/%Y') as data from onibus_db.ws_coleta order by 1"
    cursor.execute(query)

    df=pd.DataFrame([row for row in cursor.fetchall()])
    df.columns = [str(i[0]) for i in cursor.description]

    return df.to_json(orient='records')

@app.route("/linhas")
def retornaLinhas():
    query = "select distinct linha from onibus_db.ws_coleta order by 1"
    cursor.execute(query)

    df=pd.DataFrame([row for row in cursor.fetchall()])
    df.columns = [str(i[0]) for i in cursor.description]

    return df.to_json(orient='records')

@app.route("/horas/<data>/<linha>")
def retornaHoras(data, linha):
    query = "select distinct DATE_FORMAT(dataHora,'%H:00:00') as hora from onibus_db.ws_coleta where DATE_FORMAT(dataHora,'%d/%m/%Y') = '" + data.replace('-','/') + "' and linha = " + linha + " order by 1"
    
    cursor.execute(query)
    df=pd.DataFrame([row for row in cursor.fetchall()])
    df.columns = [str(i[0]) for i in cursor.description]
    
    return df.to_json(orient='records')

@app.route("/linha/<linha>")
@app.route("/linha/<linha>/<data>")
@app.route("/linha/<linha>/<data>/<hora>")
def retornaLinha(linha,data = None,hora = None):
    
    sqlData = "" 
    
    if(data != None):
        sqlData = " and DATE_FORMAT(dataHora,'%d/%m/%Y') = '" + data.replace('-','/') + "'"

    sqlHora = ""

    if(hora != None):
        sqlHora = " and DATE_FORMAT(dataHora,'%H:00:00') = '" + hora + "'"

    query = "select DATE_FORMAT(dataHora,'%d/%m/%Y %H:%i:%s') as dataFormatada, onibus_db.ws_coleta.* from onibus_db.ws_coleta where linha = " + linha + sqlData + sqlHora
    cursor.execute(query)

    df=pd.DataFrame([row for row in cursor.fetchall()])
    df.columns = [str(i[0]) for i in cursor.description]


    velocidadeMaxima = df.velocidade.max()

    df["legendaVelocidade"] = "baixo"
    df.loc[(df['velocidade'] > (velocidadeMaxima*30)/100) & (df['velocidade'] < (velocidadeMaxima*60)/100), "legendaVelocidade"] = "médio"
    df.loc[df['velocidade'] >= (velocidadeMaxima*60)/100,"legendaVelocidade"] = "alto"

    df["velocidadeMaxima"] = velocidadeMaxima

    return df.to_json(orient='records')

@app.route("/mediaVelocidadePorLinha/<linha>")
@app.route("/mediaVelocidadePorLinha/<linha>/<data>")
def mediaVelocidadePorLinha(linha, data = None): 

    groupByData = "data"
    sqlData = "DATE_FORMAT(dataHora,'%d/%m/%Y') as data"
    sqlWhereData = "" 
    
    if(data != None):
        groupByData = "dataHora"
        sqlData = "DATE_FORMAT(dataHora,'%H:%00:%00') as dataHora"
        sqlWhereData = " and DATE_FORMAT(dataHora,'%d/%m/%Y') = '" + data.replace('-','/') + "'"


    query = "select "+ sqlData +",linha,velocidade from onibus_db.ws_coleta where linha = " + linha + sqlWhereData
    cursor.execute(query)

    df=pd.DataFrame([row for row in cursor.fetchall()])
    df.columns = [str(i[0]) for i in cursor.description]

    dfVelocidade = df[[groupByData,"velocidade"]].groupby(groupByData).mean()
    dfVelocidade["velocidade"] = np.round(dfVelocidade.velocidade, decimals=2)

    return dfVelocidade.to_json()


@app.route("/quilometragemPorLinha/<linha>")
def quilometragemPorLinha(linha):
    
    query = "select DATE_FORMAT(dataHora,'%d/%m/%Y') as data,DATE_FORMAT(dataHora,'%d/%m/%Y %H:%i:%s') as dataHoraMinuto,linha,latitude,longitude from onibus_db.ws_coleta where linha = " + linha
    cursor.execute(query)

    df=pd.DataFrame([row for row in cursor.fetchall()])
    df.columns = [str(i[0]) for i in cursor.description]
    
        
    df['diferencaMinutos'] =  (pd.to_datetime(df.dataHoraMinuto,format='%d/%m/%Y %H:%M:%S') - pd.to_datetime(df.dataHoraMinuto.shift(),format='%d/%m/%Y %H:%M:%S')).dt.total_seconds()/60
    df['distancia'] =  distanciaKmLatLong(df.longitude.shift(), df.latitude.shift(),df.longitude, df.latitude)
    
    df.loc[df['diferencaMinutos'] > 15, "distancia"] = 0
    df = df[["data","distancia"]].groupby("data").sum()
    df["distancia"] = np.round(df["distancia"], decimals=2)

    return df.to_json()
