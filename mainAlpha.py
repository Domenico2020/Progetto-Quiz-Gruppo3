#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 14:59:38 2020

@author: Giulio Iannello
"""

    import json
    import argparse
    import toml
    import numpy as np
    from os.path import join
    import pandas as pd
    import datetime
    import time
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--params", help="Complete path to toml file containing parameters",
                        type=str, default='./parameters.toml')
    
    parser.add_argument("-i", "--input_data", help="Complete path to the file containing data (log)",
                        type=str, default='./file_di_test/Test-risposte date.json')
    
    parser.add_argument("-i1", "--input_data1", help="Complete path to the file containing data (utenti)",
                        type=str, default='./file_di_test/tabellaID.json')
    
    parser.add_argument("-o1", "--Data1", help="Complete path il file input_data.json", 
                        type=str, default='./PythonExport.xlsx')
    
    args = parser.parse_args()
    
    with open(args.params, 'r') as paramsFile:
        params = toml.loads(paramsFile.read())
        print(params)
    
    #Creo il DataFrame
    
    
    # legge la lista dei log in formato json e memorizzarla in una lista di liste
    f1 = open(join(params['input']['InDir'], params['input']['InFile']))
    fin = f1.read()
    data = json.loads(fin)[0]
    f1.close()
    
    # legge la tabella delle corrispondenze (utente, ID unico) già assegnate
    f1 = open(join(params['input']['InDir'], params['input']['IdFile']))
    fin = f1.read()
    d = json.loads(fin)
    start = time.perf_counter_ns()
    # legge la lista dei Quiz
    fin1=open(args.input_data,'r')
    text1=fin1.read()
    data1=json.loads(text1)[0]
    
    finI=open(args.input_data1,'r')
    textI=finI.read()
    dataI=json.loads(textI)

df=pd.DataFrame(data1, columns=['Cognome', 'Nome', ' ', 'INDB_MAT_2020',
                               '!Email', 'Esito Prova', 'Data In', 'Data Out', 'Time', 
                               'Voto', 'Domanda 2', 'Domanda 3',
                               'Domanda 4', 'Domanda 5', 'Domanda 6',
                               'Domanda 7', 'Domanda 8', 'Domanda 9',
                               'Domanda 10'])
DDN=dataI.keys()
DataT=list(DDN)
NC=dataI.values()
DataCripto=list(NC)
df1=pd.DataFrame(DataT, columns=['Nome',])
df2=pd.DataFrame(DataCripto, columns=['UC'])
df['Nome Cognome'] = df['Nome'] + ' ' + df['Cognome']
NomeC= df['Nome Cognome']
df1['UC']=df2['UC']

DataT1=list(NomeC)
#ESPORTARE NOME COGNOME IN LISTA MATCH CON DATAI ANONIMIZZIAMO L'OUTPUT CREIAMO
#DATA FRAME E METTIAMO NELLA COLONNA UC ED ELIMINIAMO LE COLONNE 0 1 20



# assegna un ID unico a ciascun nuovo utente (aggiornando la tabella)
# ed elimina il campo “utente coinvolto”
#cont = max([int(id) for id in d.values()]) + 1

for i in range(len(DataT1)):
    if  DataT1[i]  in dataI:
        dataI[DataT1[i]] = dataI.values()
        #cont += 1
    data1[i][1] = d[data1[i][1]]
    #data[i].pop(2)
    data1[i][2] = 'uc'

elapsed = time.perf_counter_ns() - start
print('*** elapsed ***', elapsed / 1000000000.0)
#with open('Outfile1.xlsx', 'w') as outfile: 
#    json.dump(outstr1, outfile)

#user_features.to_excel(args.outstr1)