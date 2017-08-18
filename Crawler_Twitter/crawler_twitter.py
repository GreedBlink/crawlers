# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 11:59:56 2017

@author: henrique.almeida
"""
from pathlib import Path
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from numpy import array
#import requests,fastavro
import glob
from datetime import date, timedelta
import re,time,datetime
contas = array(["Correio","Estadao","JornalOGlobo","Zerohora"])
dates = glob.glob(str(Path.home())+"/Documents/Python Scripts/Crawler_Twitter/results/*")
## If dates ..... ##
def crawler_twitter(contas=contas,
                    data_inicial="2017-08-01",
                    data_final="2017-07-28"):
    os.chdir(str(Path.home())+"/Documents/Python Scripts/Crawler_Twitter")
    remDr = webdriver.Chrome(str(Path.home())+"/Documents/SeleniumServer/chromedriver.exe")
    lista_li = list()
    conta_li = list()
    url_base = "https://twitter.com/search?f=tweets&vertical=default&q="
    for conta in contas:
        compl_url = "%20lang%3Apt%20from%3A"+conta+"%20since%3A"+data_final+"%20until%3A"+data_inicial
        url = url_base+compl_url
        remDr.get(url)
        page_size = len(remDr.page_source)
        remDr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)
        page_size_aux = len(remDr.page_source)
        while(page_size < page_size_aux):
            #time.sleep(0.8)
            page_size = len(remDr.page_source)
            remDr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.0)
            page_size_aux = len(remDr.page_source)
        page = remDr.page_source
        soup = BeautifulSoup(page, 'html.parser')
        li_tweets = soup.find_all(attrs={"class":"js-stream-item"})
        lista_li.append(li_tweets)
        conta_li.append(conta)
    if not os.path.exists("./results"):
        os.makedirs("./results")
    with open("./results/"+data_inicial+"_"+data_final+"tweets.txt",
              "w", encoding="utf-8") as f:
        f.write(str(li_tweets))
        f.close()
crawler_twitter()
