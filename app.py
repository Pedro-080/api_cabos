from flask import Flask
import pandas as pd
import json

app = Flask(__name__)
app_version = 'pre-alpha 0.1'

df = pd.read_csv('data/Dados_Cabos.csv')
#Cria o dataframe a partir do banco de dados csv

df.index = pd.RangeIndex(start=1,stop=len(df)+1,step=1)
#Reseta o index do dataframe para começar em 1

@app.get('/cabo')
def listar_cabos():
    json_data=[]                                    
    for idx,row in df.iterrows():
        json_item = {"id":idx,"cabo":row['Tag']}
        json_data.append(json_item)
    cables = pd.io.json.dumps(json_data)
    return cables

@app.get('/cabo/<int:index>')
def echo_string(index):
    index-=1
    row = df.iloc[index]
    print(row)
    row_dict = row.to_dict()
    row_json = json.dumps(row_dict)
    return row_json


app.run()