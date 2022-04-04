from src import scrapy

if __name__ == "__main__":
    
     filename = "nivel_de_polen.csv"
     ejecucion = 0
     ejecucion = scrapy.control(filename)
     if ejecucion == 0:
          conjunto_datos = scrapy.get_nivel_2()
          scrapy.create_csv(filename,conjunto_datos)
     else:
          print ('[+] Se aborta la presente extracción de datos')