#                       UNIVERSIDAD DEL VALLE DE GUATEMALA
#           FACULTAD DE INGENIERÍA - DEPARTAMENTO DE ING. ELECTRÓNICA
#   IE3035 - SISTEMAS DE TELECOMUNICACIONES 1 - ING. JOSÉ MANUEL MORALES
#                 
#----------------------------------------------------------------------------
#   Código presentado como trabajo para:
#           PROYECTO #1 - APLICACIÓN: PROPAGACIÓN DE REDES DE INTERNET
#
#   El código a continuación permite visualizar la dinámica de los anuncios
#   de red a travez de la propagación de anuncios a travéz de AS's a nivel
#   global. Por medio de una red específicada con una IP/24 se observará
#   los cambios (si existen o no) en los anuncios de red global. Se hace uso
#   de la API RIPE NCC. 
#
import matplotlib.pyplot as plt
import networkx as nx
import requests
import json

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


print("*- BIENVENIDO AL SISTEMA\n")
ip = str(input("*- Ingrese su IP con formato A.B.C.D/mascara por favor: "))
print("*- Su ip registrada es: ",ip)
print("*- Extrayendo respuesta de RIPE NCC")
año_in = str(input("*- Ingrese el año inical por favor: "))
mes_in = str(input("*- Ingrese el mes inical por favor: "))
dia_in = str(input("*- Ingrese el día inicial por favor: "))
hora_inicial = str(input("*- Ingrese la hora de inicio por favor: "))

año_fin = str(input("*- Ingrese el año final por favor: "))
mes_fin = str(input("*- Ingrese el mes final por favor: "))
dia_fin = str(input("*- Ingrese el día final por favor: "))
hora_final = str(input("*- Ingrese la hora de finalizacion por favor: "))


#stat.ripe.net/data/bgplay/data.json?resource=181.174.105.47/24&starttime=2021-08-28T07:00&endtime=2021-08-28T07:05



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

asn_total_paths = len(resp.json()['data']['initial_state'])

print("******************************************************************************\n")
print("*- Se han detectado: ",asn_total_paths," conexiones desde su red hacia el mundo.")

asn = int(input("*- Ingrese el ASN hacia el cual desea buscar path por favor: "))

for i in range (asn_total_paths):
    #asn_path.append[i] = resp.json()['data']['initial_state']['path']
    asn_destiny = resp.json()['data']['initial_state'][i]['path'][i-1]
    asn_global.append(resp.json()['data']['initial_state'][i]['path'])
    asn_path_destiny_len = len(resp.json()['data']['initial_state'][i]['path'])    
    #print('ASN No: ', asn_destiny,'\t Numero de saltos: ',asn_path_destiny_len)
    if (asn_destiny == asn):
        asn_match_EN = 1
        asn_path_len = asn_path_destiny_len
        asn_path_original = resp.json()['data']['initial_state'][i]['path']
        #for j in range (asn_path_len):
        #   asn_path_original.append() 
        
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
        #print('Cambio en el ASN No. ',resp.json()['data']['events'][k]['attrs']['path'][0])
        asn_total_path_changes = asn_total_path_changes + 1
        if (resp.json()['data']['events'][k]['attrs']['path'][0] == asn):
            asn_path_change_EN = 1
            asn_target_events_count = asn_target_events_count +1
            asn_path_changes.append(resp.json()['data']['events'][k]['attrs']['path'])
            if (resp.json()['data']['events'][k]['attrs']['path'] != asn_path_original):
                asn_path_changes_count = asn_path_changes_count +1
                
            
        
print("*- Se han detectado un total de: ", asn_total_path_changes, " cambios en el anuncio de las rutas a nivel global.")
print("*- Se han detectado un total de: ", asn_target_events_count," anuncios relacionados con el ASN: ",asn)
print("*- Se han detectado un total de: ", asn_path_changes_count, " cambios en el anuncio de ruta del ASN: ", asn)
print("*- \n")
if (asn_path_change_EN):
    #print("*- Se ha detectado un cambio en la ruta del asn indicado.")
    #print(asn_path_changes)
    path_changes_len = len(asn_path_changes)
    #print(path_changes_len)
    for j in range (path_changes_len):
        print("*- Reanuncio de path: ",j+2,":", asn_path_changes[j])    

else: 
    print("*- No se detectaron cambios en la ruta del asn indicado.")

print("*- IMPRIMIENDO RUTAS DETECTADAS HACIA EL AS DESTINO")
asn_global_len = len(asn_global)


"""
for m in range (asn_global_len):
        print("*- Anuncio de path: ",m,":", asn_global[m])
"""

print("*- Generando diagrama de propagación de redes. ")

G = nx.DiGraph()
for l in range (asn_global_len):
    route_trans.clear()
    route_original.clear()
    route_original = asn_global[l]
    asn_path_n_len = len(route_original)
    for n in range (asn_path_n_len):
        route_trans.append(route_original[asn_path_n_len-n-1])
    #print("*- Ruta: ",l+1, ": ",route_trans)
    nx.add_path(G,route_trans)

options = {
    'font_size': 0.5,
    'with_labels': 'True',
    'edge_color': 'blue',
    'node_color': 'cyan',
    'node_size': 5,
    'width': 0.01,
}
#nx.draw_networkx(G,**options)
#nx.draw(G,**options)
#nx.draw_spectral(G,**options)
nx.draw_kamada_kawai(G,**options)
#nx.draw_random(G,**options)
#nx.draw_circular(G,**options)
#nx.draw_networkx(G,**options)
#nx.draw_planar(G,**options)
plt.savefig("MAPA.png", dpi=1200)
plt.savefig("MAPA.pdf")
plt.show()

    
        

#print("*- ",route_n)  

"""
routes_n_len = len(route_n)
for p in range (routes_n_len):
    nx.add_path(G,route_n[p]) 
"""
"""
for o in range (asn_global_len):
        print("*- Anuncio de path: ",o,":", route_n[o])
"""

