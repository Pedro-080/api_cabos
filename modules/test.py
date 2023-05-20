import numpy as np
T_min=16
T_eds=22
T_operacao=75


t2 = list(np.linspace(T_min,T_eds+16,12))
t2.append(T_operacao)


# for t in t2:
#     diferenca = abs(t - T_eds)
#     diferenca_minima = float('inf')
#     if diferenca < diferenca_minima:
#         diferenca_minima = diferenca
#         valor_proximo = t
        
# print(valor_proximo)
    


def Add_Teds(lista, valor_busca):
    # Busca o valor mais próximo ao Teds e o converte em EDS
    valor_proximo = None
    diferenca_minima = float('inf')

    for valor in lista:
        diferenca = abs(valor - valor_busca)
        if diferenca < diferenca_minima:
            diferenca_minima = diferenca
            valor_proximo = valor
    for i in range(len(lista)):
        if lista[i] == valor_proximo:
            lista[i]=valor_busca  
    return lista
    

# Exemplo de uso

valor_busca = T_eds
t2 = [round(elemento, 2) for elemento in t2]
print(t2)
lista = Add_Teds(t2, valor_busca)
print(lista)
# print(f"Valor mais próximo encontrado: {valor_proximo}")
