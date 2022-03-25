import os
from unittest import result
import requests
import csv
from datetime import  date
from bs4 import BeautifulSoup
#from bs4 import BeautifulSoup

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
              print(link.get('href'))

       for value in lista.find_all('a'):
              provincias.append(value.text.strip())
       
       for note in lista.find_all('span'):
              nota_global.append(note.text.strip())

       print(r.headers['Content-Type'])
       #return provincias, nota_global


def create_csv(filename):
       
       #currentDir = os.path.dirname(__file__)
       filePath = os.path.join('csv/', filename)
       
       with open(filePath, 'w+', newline='', encoding='UTF-8') as csvFile:
              fecha = date.today()
              writer = csv.writer(csvFile)
              writer.writerow(['fecha_extraccion','provincia', 'nota_global'])
              for x, priceElement in enumerate(provincias):
                     writer.writerow([fecha,priceElement, nota_global[x]])