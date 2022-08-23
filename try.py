#                       UNIVERSIDAD DEL VALLE DE GUATEMALA
#           FACULTAD DE INGENIERÍA - DEPARTAMENTO DE ING. ELECTRÓNICA
#          SISTEMAS DE TELECOMUNICACIONES 1 - ING. JOSÉ MANUEL MORALES
#
#----------------------------------------------------------------------------
# 
#
import matplotlib.pyplot as plt
import networkx as nx
import requests
import json
from pyvis.network import Network
from cProfile import label


asn_path_original = []
asn_match_EN = 1
asn_path_len = 0
asn_total_path_changes = 0
asn_total_path_events = 0
asn_path_change_EN = 0
asn_path_changes = []
asn_path_changes_count = 0
asn_target_events_count = 0
asn_global = []
route_original = []
route_n = []
route_trans = []




import requests
import networkx as nx
import matplotlib.pyplot as plt

def Pair_Generator(AuxList):
    # Se genera la lista para la obtencion de la relación entre nodos
    PairList = []
    Aux2 = []
    for i in range(len(AuxList)-1):
        for j in range(len(AuxList[i])-1):
            PairList.append((AuxList[i][j+1], AuxList[i][j]))
    for element in PairList:
        if element not in Aux2:
            Aux2.append(element)
    return Aux2

net = Network(directed=True, height= "920px", width= "1865px")# crear un grafo
ip = '181.189.154.0/24&starttime=2022-08-22T00:00&endtime=2022-08-22T23:59' #'181.174.107.0/24'
url = 'https://stat.ripe.net/data/bgplay/data.json?resource={}'.format(ip)
resp = requests.get(url)
print (url)
asn_total_paths = len(resp.json()['data']['initial_state'])
print("******************************************************************************\n")
print("*- Se han detectado: ",asn_total_paths," conexiones desde su red hacia el mundo.")


asn = int(input("*- Ingrese el ASN hacia el cual desea buscar path por favor: "))



for i in range (asn_total_paths):
    #a = resp.json()['data']['initial_state'][i]['path']
    asn_global.append(resp.json()['data']['initial_state'][i]['path'])
    asn_path_destiny_len = len(resp.json()['data']['initial_state'][i]['path']) 

    if ( resp.json()['data']['initial_state'][i]['path'][0] == asn):
        asn_match_EN = 1
        asn_path_len = asn_path_destiny_len
        asn_path_original = resp.json()['data']['initial_state'][i]['path']

a = Pair_Generator(asn_global)
print(type(a))
for i in range (asn_path_destiny_len-1):
    etiquetas= [str(x) for x in a]
    net.add_nodes(a, label=etiquetas)
    for j in range(1,len(a)):
         net.add_edge(a[j],a[j-1])

net.show('grafica_original.html')

asn_total_paths = len(resp.json()['data']['initial_state'])



# print("******************************************************************************\n")        
# if (asn_match_EN):
#     print("*- Se ha encontrado un path hacia su asn indicado.")
#     print("*- El recorrido tiene: ", asn_path_len, " asn's involucrados.")
#     print("*- La ruta original hacia ese path es: ",asn_path_original)
# else: print("*- No se encontró path hacia el asn indicado.")   
 
# print("******************************************************************************\n")





# asn_total_paths_events = len(resp.json()['data']['events'])  

# for k in range (asn_total_paths_events):
#     if (resp.json()['data']['events'][k]['type'] == "A"):
#         asn_total_path_changes = asn_total_path_changes + 1
#         if (resp.json()['data']['events'][k]['attrs']['path'][0] == asn):
#             asn_path_change_EN = 1
#             asn_target_events_count = asn_target_events_count +1
#             asn_path_changes.append(resp.json()['data']['events'][k]['attrs']['path'])
#             if (resp.json()['data']['events'][k]['attrs']['path'] != asn_path_original):
#                 asn_path_changes_count = asn_path_changes_count +1

# print("************************************************************************************************************\n")                
# print("*- Se han detectado un total de: ", asn_total_path_changes, " cambios en el anuncio de las rutas a nivel global.")
# print("*- Se han detectado un total de: ", asn_target_events_count," anuncios relacionados con el ASN: ",asn)
# print("*- Se han detectado un total de: ", asn_path_changes_count, " cambios en el anuncio de ruta del ASN: ", asn)
# print("************************************************************************************************************\n")
# if (asn_path_change_EN):
#     path_changes_len = len(asn_path_changes)
#     for j1 in range (path_changes_len):
#         print("*- Reanuncio de path: ",j1+1,":", asn_path_changes[j1])    
# else: 
#     print("*- No se detectaron cambios en la ruta del asn indicado.")
# print("*- IMPRIMIENDO RUTAS DETECTADAS HACIA EL AS DESTINO")
# asn_global_len = len(asn_global)
# print("*- Generando diagrama de propagación de redes. ")






# for i in range (asn_total_paths):
#     a = resp.json()['data']['initial_state'][i]['path']
#     asn_destiny = resp.json()['data']['initial_state'][i]['path'][0]
#     asn_path_destiny_len = len(resp.json()['data']['initial_state'][i]['path'])
#     asn_global.append(resp.json()['data']['initial_state'][i]['path'])

#     etiquetas= [str(x) for x in a]
#     net.add_nodes(a, label=etiquetas)
#     if (asn_destiny == asn):
#             asn_match_EN = 1
#             asn_path_len = asn_path_destiny_len
#             asn_path_original = resp.json()['data']['initial_state'][i]['path']


#     for j in range(1,len(a)):
#         net.add_edge(a[j],a[j-1])       
    

# net.show('grafic0.html')
# if (asn_match_EN):
#     print("*- Se ha encontrado un path hacia su asn indicado.")
#     print("*- El recorrido tiene: ", asn_path_len, " asn's involucrados.")
#     print("*- La ruta original hacia ese path es: ",asn_path_original)
# else: print("*- No se encontró path hacia el asn indicado.")  

# from itertools import chain


    

# fixlist = [['ab'],['cd'],['e'],['f'],['c']]
# # Converts fixlist from a list of lists to a flat list, and removes duplicates with set
# fixlist  = list(set(list(chain.from_iterable(fixlist))))
# print(fixlist)

