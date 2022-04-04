import os
import pandas as pd
import requests
from datetime import  datetime
from bs4 import BeautifulSoup

enlaces = []
provincias = []
nota_global = []

def control(filename):
       abortando = 0
       filePath = os.path.join('csv/', filename)
       lectura = pd.read_csv(filePath)
       fecha = lectura.iloc[-1:]["Dia"]
       fecha = fecha.array
       now = datetime.now()
       dia = now.strftime('%d/%m/%Y')
       if dia == fecha:
              print ('[+] El proceso ya ha sido ejecutado en el día de hoy.')
              abortando = 1
       return(abortando)

def get_nivel_1():
       
       domain ='https://www.eltiempo.es'
       sub_domain='/polen'
       print('[+] Scraping en la web ', domain)
       # Obtenemos el data-source
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
              enlaces.append(link.get('href'))

       for value in lista.find_all('a'):
              provincias.append(value.text.strip())
       
       for note in lista.find_all('span'):
              nota_global.append(note.text.strip())

       #unimos nobmre de provincia, nivel y enlace en un df a modo de diccionario y para facilitar la grabación
       df_n1 = {'Provincia': provincias, 'Calidad_polen': nota_global, 'Enlace_provincia': enlaces}
       df_n1 = pd.DataFrame(df_n1)
      
       return df_n1, domain

def get_nivel_2():
       df_n1, domain  = get_nivel_1()
       #bucle por provincias = enlaces
       df_acumulado = pd.DataFrame(columns=('Enlace_provincia', 'Planta', 'Nivel_polen'))

       for prov in enlaces:

              polenes = []
              nota_polen=[]
              re_2 = requests.get(domain+prov)
              nivel_3 = BeautifulSoup(re_2.text, "html.parser")
              results3 = nivel_3.find("section", {"class" : "block_thirds_left lazyloadcontent row_box row_number_5"})
              result4 = results3.get('data-content-src')
              re_p = requests.get(domain+result4)
              nivel_4 = BeautifulSoup(re_p.text, "html.parser")

              lista2 = nivel_4.table

              for link in lista2.find_all('a'):
                     link.get('href')

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
              df_acumulado=pd.concat([ df_acumulado, df_n2 ])


       #finalizamos uniendo los dataframe de los niveles explorados
       completo = pd.merge(df_n1, df_acumulado,how='inner', on='Enlace_provincia')

       return completo



def create_csv(filename,datos):
       filePath = os.path.join('csv/', filename)
       now = datetime.now()
       dia = now.strftime('%d/%m/%Y')
       hora= now.strftime('%H:%M:%S')
       datos['Dia']=dia
       datos['Hora']=hora
       #comprueba si ya existe el csv para no añadir el encabezado
       if not os.path.isfile(filePath):
              datos.to_csv(filePath, sep=',', index=False, mode = 'a', encoding = 'UTF-8',  columns=('Dia','Hora', 'Provincia', 'Calidad_polen', 'Planta','Nivel_polen'))
       else:
              datos.to_csv(filePath, sep=',', index=False, header= False, mode = 'a', encoding = 'UTF-8',  columns=('Dia','Hora', 'Provincia', 'Calidad_polen', 'Planta','Nivel_polen'))
       
       print('[+] El proceso ha terminado satisfactoriamente.')
