#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 10:32:40 2022

@author: eaariash
"""

import rpa_arx as r
# from selenium import webdriver
import mysql.connector
import pandas as pd
import time as t


PATH_DESCARGAS = r"/descargas"


# WEB_DRIVER = r'./chromedriver'

# options = webdriver.chrome.options.Options()
# options.use_chromium = True
# options.binary_location = r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# options.add_experimental_option("prefs", {
#   "download.default_directory": PATH_DESCARGAS,
#   "download.prompt_for_download": False,
#   "download.directory_upgrade": True,
#   "safebrowsing.enabled": True,
#   "profile.default_content_setting_values.automatic_downloads": 1,
# })


# # driver = Edge(executable_path = r'./msedgedriver', options=options)
# driver  = webdriver.Chrome(executable_path=WEB_DRIVER, options = options)



from msedge.selenium_tools import Edge, EdgeOptions

DRIVER = 'msedgedriver.exe'


options = EdgeOptions()
options.use_chromium = True
options.add_experimental_option("prefs", {
  "download.default_directory": r'/Users/eaariash/ingenieria/BOT-SVL/etiquetas_descargadas/',
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True,
  "profile.default_content_setting_values.automatic_downloads": 1,
})
driver = Edge(executable_path = 'msedgedriver.exe', options=options)



cnxn = mysql.connector.connect( host='localhost', 
                               user= 'root', 
                               passwd='', 
                               db='dsrp')

query = """
select CodPip from dsrp.tabla_pip tp
"""

df_pip = pd.read_sql(query,cnxn)

df_pip_example = df_pip[1000:30000]



url = "https://ofi5.mef.gob.pe/invierte/formato/verInversion/"

######## ESTRUCTURA SCRAP
def scrapear(url_scrap, driver, cod):

    driver.get(url_scrap)

    ##--> UNIDAD FORMULADORA
    
    departame_uf = r.obtener_texto(driver, '//*[@id="UC1_lblUFSector"]')
    pliego_uf = r.obtener_texto(driver,'//*[@id="UC1_lblUFPliego"]')
    nombre_uf = r.obtener_texto(driver, '//*[@id="UC1_lblUFNombre"]')
    personaResponsablePipMenor_uf = r.obtener_texto(driver, '//*[@id="UC1_lblUFFormular"]')
    personaResponsable_uf = r.obtener_texto(driver, '//*[@id="UC1_lblUFResponsable"]')
    
    ##--> UNIDAD EJECUTORA
    departamento_ue = r.obtener_texto(driver, '//*[@id="UC1_lblNiv1"]')
    provincia_ue = r.obtener_texto(driver, '//*[@id="UC1_lblNiv2"]')
    nombre_ue = r.obtener_texto(driver, '//*[@id="UC1_lblUENombre"]')
    personaRespoble_ue = r.obtener_texto(driver, '//*[@id="UC1_lblUEResponsable"]')
    organoTecnico_ue = r.obtener_texto(driver, '//*[@id="UC1_lblOrgResp"]')
    
    data_unidad_formuladora = {
        "codPip": cod,
        "departamento_uf":departame_uf,
        "pliego_uf":pliego_uf,
        "nombre_uf":nombre_uf,
        "personaResponsablePipMenor_uf":personaResponsablePipMenor_uf,
        "personaResponsable_uf":personaResponsable_uf
        }
    
    data_unidad_ejecutora = {
        "codPip":cod,
        "departamento_ue":departamento_ue,
        "provincia_ue":provincia_ue,
        "nombre_ue": nombre_ue,
        "personaRespoble_ue":personaRespoble_ue,
        "organoTecnico_ue":organoTecnico_ue
        }
    
    data = {
        "unidad_formuladora" : data_unidad_formuladora,
        "unidad_ejecutora":data_unidad_ejecutora
        }
    
    return data


df_uf= pd.DataFrame(columns=['codPip','departamento_uf', 'pliego_uf', 'nombre_uf', 'personaResponsablePipMenor_uf', 'personaResponsable_uf'])
df_ue = pd.DataFrame(columns=['codPip','departamento_ue', 'provincia_ue', 'nombre_ue', 'personaRespoble_ue', 'organoTecnico_ue'])



for cod in df_pip_example["CodPip"]:
    star_time = t.time()
    url_scrap = url + str(cod)
    print(url_scrap)
    data = scrapear(url_scrap, driver, cod)
    unidad_formuladora_line = data['unidad_formuladora']
    unidad_ejecutora_line = data['unidad_ejecutora']
    print(unidad_formuladora_line)
    print(unidad_ejecutora_line)
    df_ue = df_ue.append(unidad_ejecutora_line, ignore_index=True)
    df_uf = df_uf.append(unidad_formuladora_line, ignore_index=True)
    finish_time = t.time()
    print(finish_time - star_time)
    
ahora = str(int(t.time()))
name_uf = f'/tabla_unidad_formuladora_{ahora}.xlsx'
name_ue = f'/tabla_unidad_ejecutora_{ahora}.xlsx'
df_uf.to_excel("descargas" + name_uf)
df_ue.to_excel("descargas" + name_ue)




