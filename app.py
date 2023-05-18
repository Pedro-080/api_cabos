from flask import Flask,request,redirect,jsonify
from modules.Cabos import Cabo
import pandas as pd
import json
import pytest
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app_version = 'pre-alpha 0.1'

app.config['vao']=100
app.config['tag']=None
app.config['t01']=300
app.config['t_min']=16
app.config['t_eds']=22
app.config['t_ope']=75


condutor = Cabo()

df = condutor.df

@app.get('/cabo') #Lista todos os condutores
@cross_origin()
def listar_cabos():
    json_data=[]                                    
    for idx,row in df.iterrows():
        # json_item = {"id":idx,"cabo":row['Tag']}
        json_item = {"id":idx,
                 "cabo":row['Tag'],
                 "area":row['ÁREA'],
                 "diametro":row['DIÂMETRO'],
                 "massa":row['MASSA_LINEAR'],
                 "elasticidade":row['MÓDULO_DE_ELASTICIDADE'],
                 "dilatacao": row['COEFICIENTE_DE_DILATAÇÃO_TÉRMICA'],
                 "ruptura": row["Carga_de_ruptura"]
                }
        json_data.append(json_item)
    cables = pd.io.json.dumps(json_data)
    return cables

@app.get('/cabo/<int:index>') #/cabo/3
@cross_origin()
def select_cabo(index):
    index-=1
    row = df.iloc[index]
    print(row)
    row_dict = row.to_dict()
    row_json = json.dumps(row_dict)
    return row_json

@app.get('/set_cabo/<int:index>') #/set_cabo/2
def set_cabo(index):
    # condutor.set_cabo(index)
    app.config['tag']=condutor.set_cabo(index)
    return condutor.cabo

@app.get('/set_vao') #/set_vao?vao=50.20
def set_vao(vao=0):
    #define a variavel global "vao" como entrada
    if vao == 0:
        app.config['vao'] = request.args.get('vao', default=0.0, type=float)
    else:
        app.config['vao'] = vao
    
    # variavel de teste
    meu_vao = app.config['vao']
    
    # retorna a variavel de teste meu_vao
    return f'Vao: {meu_vao}'

@app.get('/get_vao') #funcao de teste que retorna o valor global de "vao"
def get_vao():
    vao_global = app.config['vao']
    return vao_global

@app.get('/set_t01') #/set_t01?t01=230
def set_t01(t01=0):
      #define a variavel global "t01" como entrada
    if t01 == 0:
        app.config['t01'] = request.args.get('t01', default=0.0, type=float)
    else:
        app.config['t01'] = t01  
    
    # variavel de teste
    t01 = app.config['t01']
    
    # retorna a variavel de teste meu_vao
    return t01

@app.get('/get_t01') #funcao de teste que retorna o valor global de "t01"
def get_t01():
    t01_global = app.config['t01']
    return t01_global

@app.get('/set_tmin') #/set_tmin?tmin=50.20
def set_tmin(tmin=0):
    #define a variavel global "tmin" como entrada
    if tmin == 0:
        app.config['t_min'] = request.args.get('tmin', default=app.config['t_min'], type=float)
    else:
        app.config['t_min'] = tmin   
    
    # app.config['t_min'] = request.args.get('tmin', default=0.0, type=float)
    t_min = app.config['t_min']
    return t_min
    
@app.get('/set_teds') #/set_teds?teds=50.20
def set_teds(teds=0):
    #define a variavel global "teds" como entrada
    if teds == 0:
        app.config['t_eds'] = request.args.get('teds', default=app.config['t_eds'], type=float)
    else:
        app.config['t_eds'] = teds      
    
    t_eds = app.config['t_eds']
    return t_eds

@app.get('/set_tope') #/set_tope?tope=75
def set_tope(tope=0):
    #define a variavel global "tope" como entrada
    if tope == 0:
        app.config['t_ope'] = request.args.get('tope', default=app.config['t_ope'], type=float)
    else:
        app.config['t_ope'] = tope  
    
    t_ope = app.config['t_ope']
    return t_ope

@app.get('/load_temp') #carrega todas as temperaturas
def load_temp():
    t_min=app.config['t_min']
    t_eds=app.config['t_eds']
    t_ope=app.config['t_ope']
    condutor.set_temperaturas(t_min,t_eds,t_ope)
    return condutor.get_temperaturas()

@app.get('/cabo/<int:index>/load') #/cabo/2/load?vao=100&t01=200&tmin=16&teds=22&tope=75
@cross_origin()
def load(index):
    set_cabo(index)
    set_vao(request.args.get('vao',default=0.0, type=float))
    set_t01(request.args.get('t01',default=0.0, type=float))
    set_tmin(request.args.get('tmin',default=app.config['t_min'],type=float))
    set_teds(request.args.get('teds',default=app.config['t_eds'],type=float))
    set_tope(request.args.get('tope',default=app.config['t_ope'],type=float))
    
    load_temp()
    vao = get_vao()
    t01 = get_t01() 
    
    condutor.dados_esticamento(t01,vao)
    esticamento = condutor.esticamento.to_json(orient='records')  

    return esticamento



@app.get('/cabo/esticamento')
def esticamento():
    load_temp()
    vao=app.config['vao']
    t01=app.config['t01']
    print(t01)
    condutor.dados_esticamento(t01,vao)
    esticamento = condutor.esticamento.to_json(orient='records')
 
    # var_class = condutor.__dict__
    # variaveis = {k: v for k,v in var_class.items() if not isinstance(v, pd.DataFrame)}

    return esticamento


if __name__ =="__main__":   
    app.run()