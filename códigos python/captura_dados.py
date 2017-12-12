import csv
import requests
import MySQLdb
from datetime import datetime
import time

#configura conexao com o banco de dados
mydb = MySQLdb.connect(host='0.0.0.0',
    user='',
    passwd='',
    db='')

#configura a url do arquivo csv
CSV_URL = 'http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/csv/onibus.cfm'



while True:

    #inicia o cursor
    cursor = mydb.cursor()

    with requests.Session() as s:
        download = s.get(CSV_URL)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

        #apaga a primeira linha com o cabecalho
        my_list.pop(0)

        #lista a ultima data inserida no bd
        sql = "select max(dataHora) as dataHora from coleta"
        cursor.execute(sql)
        ultima_data_inserida = ''
        
        for d in cursor:
            ultima_data_inserida = d[0]
        

        for row in my_list:
            #trata a data para o formato do banco de dados
            data_arquivo = datetime.strptime(row[0], '%m-%d-%Y %H:%M:%S')

            if (data_arquivo > ultima_data_inserida):
                row[0] = data_arquivo
                sql = "insert into coleta (dataHora,ordem,linha,latitude,longitude,velocidade,datacoleta) values (%s,%s,%s,%s,%s,%s,now())"
                cursor.execute(sql,row)
                mydb.commit()

    cursor.close()

    # programa o script para parar em 21/10/2017
    data_fim = datetime(2017,10,21)
    agora = datetime.now()

    if data_fim < agora :
        break

    print ("Rodou em: " + str(agora))

    #faz um pause no script 
    uma_hora = 60 * 60 #60 minutos
    time.sleep(uma_hora)