from src import scrapy

if __name__ == "__main__":
    
     filename = "nivel_de_polen.csv"
     
     
     conjunto_datos = scrapy.links()
     scrapy.create_csv(filename,conjunto_datos)