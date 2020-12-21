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
parser.add_argument("-o", "--user_feature", help="Complete path to the file containing data output(.json)", 
                    type=str, default='user_feature2.0.json')
parser.add_argument("-o1", "--out_data1", help="Complete path il file input_data.json", 
                    type=str, default='PythonExport2.0.xlsx')
args = parser.parse_args()

with open(args.params, 'r') as paramsFile:
    params = toml.loads(paramsFile.read())
    print(params)

# legge la lista dei log in formato json e memorizzarla in una lista di liste
f1 = open(join(params['input']['InDir'], params['input']['InFile']))
fin = f1.read()
data = json.loads(fin)[0]
f1.close()

# legge la tabella delle corrispondenze (utente, ID unico) già assegnate
f1 = open(join(params['input']['InDir'], params['input']['IdFile']))
fin = f1.read()
d = json.loads(fin)

# legge la lista dei Quiz
fin1=open(args.input_data,'r')
text1=fin1.read()
data1=json.loads(text1)[0]
# legge la lista degli Utenti che hanno svolto il Quiz
finI=open(args.input_data1,'r')
textI=finI.read()
dataI=json.loads(textI)

#Crazione del DataFrame secondo le varie entità delle colonne
df=pd.DataFrame(data1, columns=['Cognome', 'Nome', '', 'INDB_MAT_2020',
                               '!Email', 'Esito Prova', 'Data In', 'Data Out', 'Time', 
                               'Voto', 'Domanda 1', 'Domanda 2',
                               'Domanda 3', 'Domanda 4', 'Domanda 5',
                               'Domanda 6', 'Domanda 7', 'Domanda 8',
                               'Domanda 9'])

#Creo delle liste dal Dizionario importato in precedenza Utente e Anonimizzazione
DDN=dataI.keys()
NC=dataI.values()

#Creo le liste
DataT=list(DDN)
DataCripto=list(NC)

#Creo il DataFrame di Utenti presenti
df1=pd.DataFrame(DataT, columns=['Nome',])
df2=pd.DataFrame(DataCripto, columns=['UC'])

#Le colonne 0 1 vengono unite compongono la colonna 20 per matchare l' anonimizzazione
df['Nome Cognome'] = df['Nome'] + ' ' + df['Cognome']

#Creo la serie di nome e cognome da poi andare ad eleborare
NomeC = df['Nome Cognome']
df1['UC'] = df2['UC']

DataT1=list(NomeC)

#Anonimizzazione DataFrame
df['Nome'] = np.nan
df['Cognome'] = np.nan
df['!Email'] = np.nan

#Prendo in DataFrame degli Utenti elimino il primo record ovvero l'utente che estrae i dati
#df1.drop([0], inplace=True)
df1 = df1[df1.Nome != "Giulio Iannello"]
df1 = df1[df1.Nome != "-"]
#df1 = df1.drop([0,12])
#[12] == 'nome cognome' = '-'
#df1 = df1.drop([12])
#Modifico gli indici
df1 = df1.reset_index()
df1 = df1.drop('index',axis=1)
#Ordino per Data di inizio cosi da avere l' anonimizzazione ordinata in sequenza
sorted_df = df.sort_values(by='Data In')
#df[''] = df[''] stesso index
sorted_df['Nome Cognome'] = df1['UC']

# assegna un ID unico a ciascun nuovo utente (aggiornando la tabella)
# ed elimina il campo “utente coinvolto”

#cont = max([int(id) for id in d.values()]) + 1
#for i in range(len(data)):
#    if data[i][1] not in d:
#        d[data[i][1]] = str(cont).zfill(params['input']['CodeLength'])
#        cont += 1
#    data[i][1] = d[data[i][1]]
    #data[i].pop(2)
#    data[i][2] = 'uc'

user_features=pd.DataFrame(sorted_df, columns= ['Cognome', 'Nome', '', 'INDB_MAT_2020',
                               '!Email', 'Esito Prova', 'Data In', 'Data Out', 'Time', 
                               'Voto', 'Domanda 1', 'Domanda 2',
                               'Domanda 3', 'Domanda 4', 'Domanda 5',
                               'Domanda 6', 'Domanda 7', 'Domanda 8',
                               'Domanda 9', 'Nome Cognome'])

#salvo file Excel

user_features.to_excel(args.out_data1)

# salvo file .json

user_features.to_json(args.user_feature, orient='columns')                                                        

# # salva su file la lista dei log anonimizzata
# outstr = json.dumps(data, indent=params['input']['IndentJSON'])
# f2 = open(join(params['output']['OutDir'], params['output']['OutFile']), 'w')
# f2.write(outstr)
# f2.close()

# # salva su file la tabella utente-ID man mano che generra gli ID
# outstr = json.dumps(d, indent=params['input']['IndentJSON'])
# f3 = open(join(params['input']['InDir'], params['input']['IdFile']), 'w')
# f3.write(outstr)
# f3.close()
