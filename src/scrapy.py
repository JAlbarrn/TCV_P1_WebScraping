import os

import pandas as pd
import requests
import csv
from unittest import result
from datetime import  datetime

from bs4 import BeautifulSoup

enlaces = []
provincias = []
nota_global = []

def links():
       
       domain ='https://www.eltiempo.es'
       sub_domain='/polen'
       #Obtenemos el data Source
       ##url = 'https://www.eltiempo.es/polen~ROW_NUMBER_6~~TEMP_UNIT_c~~WIND_UNIT_kmh~'
       r = requests.get(domain+sub_domain)
       nivel_1 = BeautifulSoup(r.text, "html.parser")

       results = nivel_1.find("section", {"class" : "block_full lazyloadcontent row_box row_number_6"})
       result2 = results.get('data-content-src')

       #acceso al nivel 1
       re_1 = requests.get(domain+result2)
       nivel_2 = BeautifulSoup(re_1.text, "html.parser")
       lista = nivel_2.ul
       #links para el nivel 2
       for link in lista.find_all('a'):
       #       print(link.get('href'))
              enlaces.append(link.get('href'))

       for value in lista.find_all('a'):
              provincias.append(value.text.strip())
       
       for note in lista.find_all('span'):
              nota_global.append(note.text.strip())

       #unimos nobmre de provincia, nivel y enlace en un df a modo de diccionario y para facilitar la grabación
       df_n1 = {'Provincia': provincias, 'Calidad_polen': nota_global, 'Enlace_provincia': enlaces}
       df_n1 = pd.DataFrame(df_n1)

       print(r.headers['Content-Type'])


       #bucle por provincias = enlaces
       df_acumulado = pd.DataFrame(columns=('Enlace_provincia', 'Planta', 'Nivel_polen'))

       for prov in enlaces:

              polenes = []
              nota_polen=[]

              #re_2 = requests.get(domain+enlaces[prov])
              re_2 = requests.get(domain+prov)
              nivel_3 = BeautifulSoup(re_2.text, "html.parser") 
       
              results3 = nivel_3.find("section", {"class" : "block_thirds_left lazyloadcontent row_box row_number_5"})
              result4 = results3.get('data-content-src')
              re_p = requests.get(domain+result4)
              nivel_4 = BeautifulSoup(re_p.text, "html.parser")

              lista2 = nivel_4.table

              for link in lista2.find_all('a'):
                     print (link.get('href'))

              for value in lista2.find_all('a'):
                     polenes.append(value.text.strip())

              for note in lista2.find_all('span'):
                     nota_polen.append(note.text.strip())

              #construimos la estructura con los datos leídos para su posterior grabación
              df_n2 = {'Enlace_provincia': prov, 'Planta': polenes, 'Nivel_polen': nota_polen}
              df_n2 = pd.DataFrame(df_n2)

              #eliminamos los registros sin datos
              df_n2 = df_n2[df_n2["Nivel_polen"] != "null"] 

              #guardamos los niveles de polen de los típos de planta de la provincia en exploración
              df_acumulado=df_acumulado.append(df_n2)

       #finalizamos uniendo los dataframe de los niveles explorados
       completo = pd.merge(df_n1, df_acumulado,how='inner', on='Enlace_provincia')

       return completo



def create_csv(filename,datos):
       
       #currentDir = os.path.dirname(__file__)
       filePath = os.path.join('csv/', filename)
       
 #      with open(filePath, 'w+', newline='', encoding='UTF-8') as csvFile:
 #             fecha = date.today()
 #             writer = csv.writer(csvFile)
 #             writer.writerow(['fecha_extraccion','provincia', 'nota_global','polen','nivel_polen'])
 #             for x, priceElement in enumerate(provincias):
 #                    for y, planta in enumerate(polenes):
 #                           writer.writerow([fecha,priceElement, nota_global[x],planta, nota_polen[y]])
       now = datetime.now()
       dia = now.strftime('%d/%m/%Y')
       hora= now.strftime('%H:%M:%S')
       datos['Dia']=dia
       datos['Hora']=hora

       datos.to_csv(filePath, sep=',', index=False, header=False, mode = 'a', encoding = 'UTF-8',  columns=('Dia','Hora', 'Provincia', 'Calidad_polen', 'Planta','Nivel_polen'))
