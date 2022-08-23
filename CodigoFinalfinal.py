#                       UNIVERSIDAD DEL VALLE DE GUATEMALA
#           FACULTAD DE INGENIERÍA - DEPARTAMENTO DE ING. ELECTRÓNICA
#          SISTEMAS DE TELECOMUNICACIONES 1 - ING. JOSÉ MANUEL MORALES
#
#----------------------------------------------------------------------------
# 
#
from optparse import IndentedHelpFormatter
from turtle import clear
import matplotlib.pyplot as plt
import networkx as nx
import requests
import json
from pyvis.network import Network
from cProfile import label
from itertools import chain,zip_longest
import random
from functools import reduce


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
print("\n")
print("\n")
print("*---------------- BIENVENIDO AL SISTEMA ----------------*\n")
ip = str(input("*- Ingrese su IP con formato Ejemplo 111.222.333.444./24 por favor: "))
print("*- Su ip registrada es: ",ip)
print("*- Extrayendo respuesta de RIPE NCC")
print("*----------- Fetcha y Hora inicial ------------- ")
año_in = str(input("*- Ingrese el año : "))
mes_in = str(input("*- Ingrese el mes : "))
dia_in = str(input("*- Ingrese el día : "))
hora_inicial = str(input("*- Ingrese la hora : "))

print("*----------- Fetcha y Hora Final --------------- ")
año_fin = str(input("*- Ingrese el año : "))
mes_fin = str(input("*- Ingrese el mes : "))
dia_fin = str(input("*- Ingrese el día : "))
hora_final = str(input("*- Ingrese la hora : "))
print("*----------------------------------------------- ")
asn = int(input("*- Ingrese el ASN hacia el cual desea buscar path por favor: "))


url_a = 'https://stat.ripe.net/data/bgplay/data.json?resource={}'.format(ip)
url_b = url_a + ("&starttime={}".format(año_in))
url_c = url_b + ("-{}".format(mes_in))
url_d = url_c + ("-{}".format(dia_in))
url_e = url_d + ("T{}".format(hora_inicial))
url_f = url_e + ('&endtime={}'.format(año_fin))
url_g = url_f + ("-{}".format(mes_fin))
url_h = url_g + ("-{}".format(dia_fin))
url_i = url_h + ("T{}".format(hora_final))
print("*- URL final: ", url_i)
resp = requests.get(url_i)
net = Network(height= "920px", width= "1865px")# crear un grafo
asn_total_paths = len(resp.json()['data']['initial_state'])

print("******************************************************************************\n")
print("*- Se han detectado: ",asn_total_paths," conexiones desde su red hacia el mundo.")


for i in range (asn_total_paths):
    a = resp.json()['data']['initial_state'][i]['path']
    asn_global.append(resp.json()['data']['initial_state'][i]['path'])
    asn_path_destiny_len = len(resp.json()['data']['initial_state'][i]['path'])   
    etiquetas= [str(x) for x in a]
    net.add_nodes(a, label=etiquetas)
    if ( resp.json()['data']['initial_state'][i]['path'][0] == asn):
        asn_match_EN = 1
        asn_path_len = asn_path_destiny_len
        asn_path_original = resp.json()['data']['initial_state'][i]['path']
    for j in range(1,len(a)):
        net.add_edge(a[j],a[j-1])
net.show('grafica_original.html')
        
print("******************************************************************************\n")        
if (asn_match_EN):
    print("*- Se ha encontrado un path hacia su asn indicado.")
    print("*- El recorrido tiene: ", asn_path_len, " asn's involucrados.")
    print("*- La ruta original hacia ese path es: ",asn_path_original)
else: print("*- No se encontró path hacia el asn indicado.")   
 
print("******************************************************************************\n")
 
asn_total_paths_events = len(resp.json()['data']['events'])  
print("*- Analizando cambio en las rutas de los anuncios de red.")

for k in range (asn_total_paths_events):
    if (resp.json()['data']['events'][k]['type'] == "A"):
        asn_total_path_changes = asn_total_path_changes + 1
        if (resp.json()['data']['events'][k]['attrs']['path'][0] == asn):
            asn_path_change_EN = 1
            asn_target_events_count = asn_target_events_count +1
            asn_path_changes.append(resp.json()['data']['events'][k]['attrs']['path'])
            if (resp.json()['data']['events'][k]['attrs']['path'] != asn_path_original):
                asn_path_changes_count = asn_path_changes_count +1

print("************************************************************************************************************\n")                
print("*- Se han detectado un total de: ", asn_total_path_changes, " cambios en el anuncio de las rutas a nivel global.")
print("*- Se han detectado un total de: ", asn_target_events_count," anuncios relacionados con el ASN: ",asn)
print("*- Se han detectado un total de: ", asn_path_changes_count, " cambios en el anuncio de ruta del ASN: ", asn)
print("************************************************************************************************************\n")

if (asn_path_change_EN):
    path_changes_len = len(asn_path_changes)
    for j1 in range (path_changes_len):
        net2 = Network( directed=True, height= "920px", width= "1865px")
        print("*- Reanuncio de path: ",j1+1,":", asn_path_changes[j1])
        
        for sd in range ((path_changes_len)-1):
            
            f=asn_path_changes[sd]
            etiquetas2= [str(x1) for x1 in f]
            net2.add_nodes(f, label=etiquetas2)
        for t in range(1,len(f)):
            net2.add_edge(f[t],f[t-1])
        net2.show('grafica'+str(j1)+'.html')
        f=clear
        etiquetas2=clear
        x1=clear
    
    
else: 
    print("*- No se detectaron cambios en la ruta del asn indicado.")
print("*- IMPRIMIENDO RUTAS DETECTADAS HACIA EL AS DESTINO")
asn_global_len = len(asn_global)
print("*- Generando diagrama de propagación de redes. ")












