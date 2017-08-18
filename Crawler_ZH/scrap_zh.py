# -*- coding: utf-8 -*-
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import time
import os
from numpy import array
import datetime
import numpy as np
def scrap_zh(total_paginas=1000,
             categoria=categorias[0],
             data_final = datetime.datetime.now().date() - datetime.timedelta(days=10)):
  ## Definir diretorio ##
  path = str(Path.home())+"/Documents/Python Scripts/Crawler_ZH"
  os.chdir(path)
  div_result = list()
  date = list()
  categorias = array(["ultimas-noticias"])
  for j in range(len(categorias)):
      i = 0
      url = "http://zh.clicrbs.com.br/rs/noticias/"+categorias[j]+"/?pagina="+str(i)
      page = requests.get(url)
      soup = BeautifulSoup(page.content, 'html.parser')
      div_noticias = soup.find(attrs={"class": "listagem"})
      div_data = div_noticias.find(attrs={"class":"box-titulo"})
      date_div = datetime.datetime.strptime(div_data.contents[0], "%d/%m/%Y").date()
      date.append(str(date_div))
      while datetime.datetime.strptime(date[len(date)-1],"%Y-%m-%d").date() >= data_final:
        try:
            url = "http://zh.clicrbs.com.br/rs/noticias/"+categoria+"/?pagina="+str(i)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            div_noticias = soup.find(attrs={"class": "listagem"})
            div_data = div_noticias.find(attrs={"class":"box-titulo"})
            if(len(div_data.contents)>0):
                date_div = datetime.datetime.strptime(div_data.contents[0], "%d/%m/%Y").date()
                date.append(str(date_div))
                print("Data "+str(date_div))
                div_result.append(div_noticias)
            i = i + 1
        except:
            i = i
  with open("./results/"+date[0]+"_"+date[len(date)-1]+"zeroHora.txt",
              "w", encoding="utf-8") as f:
        f.write(str(div_result))
        f.close()
  return(div_result)
## Inicio da Funcao ##
zh_scrap = scrap_zh()