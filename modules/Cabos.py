# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from flask import jsonify
# from Biblioteca import *

class Cabo:
    def __init__(self):
        self.cabo = None
        self.S  = None
        self.d  = None
        self.E  = None
        self.p1 = None
        self.at = None
        self.esticamento = None
        self.T_min = None
        self.T_eds = None
        self.T_operacao = None

        self.df = pd.read_csv('./data/Dados_Cabos.csv',encoding='utf-8')
        self.df.index = pd.RangeIndex(start=1,stop=len(self.df)+1,step=1)
        self.columns = list(self.df.columns)
        # self.buscar_cabo()
        pass

    def set_temperaturas(self,T_min,T_eds,T_operacao=75):
        self.T_min = T_min
        self.T_eds = T_eds
        self.T_operacao = T_operacao
        pass
    
    def get_temperaturas(self):
        print(f"T_min: {self.T_min}")
        print(f"T_eds: {self.T_eds}")
        print(f"T_ope: {self.T_operacao}")
        return "ok"
    
    def set_cabo(self,index):
        self.cabo = self.df.loc[index,'Tag']
        self.buscar_cabo()
        return self.cabo


    def buscar_cabo(self): #Busca o condutor fornecido o nome(Não funciona para 850MCM)
        df_filtrado = self.df.query('Tag == @self.cabo').reset_index(drop=True)
        df_filtrado.index = pd.RangeIndex(start=1,stop=len(df_filtrado)+1,step=1)
        self.S  = df_filtrado.loc[1,self.columns[4]]
        self.d  = df_filtrado.loc[1,self.columns[5]]
        self.p1 = df_filtrado.loc[1,self.columns[6]]/1000 #kg/m to kg/km
        self.E  = df_filtrado.loc[1,self.columns[7]]
        self.at = df_filtrado.loc[1,self.columns[8]]
        return df_filtrado 
        pass 

    def dados_esticamento(self, T01, A): #Retorna T02 para todas as temperaturas fornecidas

        t1 = self.T_eds
        # define a temperatura do esticamento inicial como na temperatura EDS

        t2 = list(np.linspace(self.T_min,self.T_eds+16,12))
        t2.append(self.T_operacao)
        
        t2 = Add_Teds(t2, self.T_eds)
        
        
        Metodo_calculo = "Numpy" #Numpy ou Newton
        p2=self.p1               #p1=p2, desconsiderando pressão de vento(feature futura)

        T02 = []
    
        for t in t2: #Calcula T02 para cada t
            a=1
            b=(self.E*self.S*self.p1**2*A**2)/(24*T01**2)+self.E*self.S*self.at*(t-t1)-T01
            c=0
            d=-((self.E*self.S*p2**2*A**2)/24)
            if Metodo_calculo == "Newton":
                T02.append(Newton(a,b,c,d))
                pass
            if Metodo_calculo == "Numpy":
                T02.append(Numpy_roots(a,b,c,d))
                pass
        T02 = [round(num,2) for num in T02] #Arredonda para 2 casas decimais

        self.esticamento = pd.DataFrame({'Temperatura':t2,'T01':T01,'T02':T02})
        self.esticamento.Name = "Dados de esticamento para o cabo "+self.cabo+"\nVao de " + '{:.2f}'.format(A)+" metros."
        # return self.esticamento
        pass

    def tracao_final(self,t2):
        df = self.esticamento
        df_T02 = df.loc[df['Temperatura'] == t2].reset_index(drop=True)
        T02 = df_T02.loc[0,"T02"]
        return T02


def Numpy_roots(a,b,c,d):#Metodo de calculo do Numpy
    coef = [a,b,c,d]
    raizes = np.roots(coef)
    raizes_reais = raizes[np.logical_and(raizes.real > 0, raizes.imag == 0)]
    return np.real(raizes_reais[0])
    pass

def Newton(a,b,c,d):#Metodo de calculo usando Newton Raphson
    x0=1
    i = 0
    MF = 1.0
    while (MF > 10**(-13)):
        F = a*x0**3 + b*x0**2 + c*x0 + d
        dF = 3*a*x0**2 + 2*b*x0 + c
        if dF == 0.0:
            x1 = x0 - F/(dF + 10**(-13))
        else:
            x1 = x0 - F/dF
        F = a*x1**3 + b*x1**2 + c*x1 + d
        MF = abs(F)
        i=i+1
        x0=x1
        if i > 100:
            #print ("Não convergiu")
            break
    # print(f"Convergiu em {i}")
    return x0
    pass

def Add_Teds(lista, T_eds):
    # Busca o valor mais próximo ao Teds e o converte em EDS
    valor_proximo = None
    diferenca_minima = float('inf')

    for valor in lista:
        diferenca = abs(valor - T_eds)
        if diferenca < diferenca_minima:
            diferenca_minima = diferenca
            valor_proximo = valor
    for i in range(len(lista)):
        if lista[i] == valor_proximo:
            lista[i]=T_eds  
    return lista
    


if __name__ == "__main__":

    t_min = 16
    t_eds = 22
    t_ope = 75
    vao = 100
    T01 = 300

    condutor = Cabo()
    # print(condutor.df)
    # condutor.set_cabo(1)
    # print(condutor.__dict__)
    # print(jsonify(condutor.__dict__))
    
    # condutor.set_temperaturas(t_min,t_eds,t_ope)
    # condutor.dados_esticamento(T01,vao) 
    # print(condutor.cabo)
    # # print(condutor.esticamento.Name)
    # # print(condutor.esticamento)
    # condutor.get_temperaturas()



