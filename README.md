# TCV_P1_WebScraping
Práctica 1. Tipología y Ciclo de Vida de los Datos. Caso práctico de Web Scraping orientado a aprender a identificar los datos relevantes por un proyecto analítico y usar las herramientas de extracción de datos.

## Estructura del proyecto.  

* main.py: este archivo es el punto de entrada a la aplicación y desde donde se llaman al paquete principal 
* /src/scrapy.py: se implementa toda la logica del scraping la cual esta divida en 4 funciones.
  * control(): cuya responsabilidad es controlar que solo se pueda hacer scraping una vez al día.
  * get_nivel_1(): encargada de recuperar los datos del nivel 1
  * get_nivel_2(): encargada de recuperar los datos del nivel 2
  * create_csv(): encargada de escribir los datos capturados a un documento .csv guardado en el directorio /csv

## Publicación del dataset.

El dataset obtenido ha sido publicado en https://zenodo.org/ con DOI:[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6391607.svg)](https://doi.org/10.5281/zenodo.6391607)

## Autores.

**Francisco Javier Albarrán González**  
**Enrique Villalobos Torregrosa**