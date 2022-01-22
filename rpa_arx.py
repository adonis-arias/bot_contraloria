#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 18:16:53 2021

@author: eaariash
"""


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from email.mime.multipart import MIMEMultipart
# from email.mime.application import MIMEApplication
from smtplib import SMTP
from email.mime.text import MIMEText
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


def seleccionar(driver, xpath, value):
    select = Select(driver.find_element_by_xpath(xpath))
    # # select by visible text
    # select.select_by_visible_text('Banana'()
    # select by value 
    select.select_by_value(value)


def hacer_click(driver, xpath, t=5):
    WebDriverWait(driver, t)\
                .until(EC.element_to_be_clickable((By.XPATH, xpath))).click()   


def escribir(driver, xpath, writer , t=5):
    WebDriverWait(driver, t)\
                .until(EC.element_to_be_clickable((By.XPATH, xpath))).send_keys(writer)   


def existe_elemento(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except Exception as err:
        print(err)
        return False


def obtener_texto(driver, xpath, t =5):
    try:
        elemento = WebDriverWait(driver, t)\
                        .until(EC.element_to_be_clickable((By.XPATH, xpath))).text   
    except:
        elemento = ""
    return elemento


def enviar_correo(html, destinatario, asunto, pdf_lpn, fecha, nombre_seller):
    
    msgText = MIMEText( html , 'html')
    
    mensaje = MIMEMultipart()
    mensaje["From"] = 'eaariash@falabella.com'
    mensaje["To"] = destinatario
    mensaje["Subject"]= asunto
    
    mensaje.attach(msgText)
    # filename = "lpn-" +  str(fecha) + '.pdf'
    
    # pdf = MIMEApplication(open(pdf_lpn, 'rb').read())
    # pdf.add_header('Content-Disposition', 'attachment', filename= filename)
    # mensaje.attach(pdf)
    
    smtp = SMTP("smtp.office365.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('eaariash@falabella.com', "F@l@bell@2021")
    smtp.send_message(mensaje)
    smtp.quit()

def limpiar_input(driver, xpath, t=5):
    WebDriverWait(driver, t)\
                .until(EC.element_to_be_clickable((By.XPATH,
                                               xpath))).clear()
            
def teclear_enter(driver, xpath, t=5):
    WebDriverWait(driver, t)\
                .until(EC.element_to_be_clickable((By.XPATH, 
                                    xpath))).send_keys("webdriver" + Keys.RETURN)
                
def scroll_abajo(driver, xpath, movimientos = 2, t = 5):
    for i in range(0,movimientos):
        WebDriverWait(driver, t)\
            .until(EC.element_to_be_clickable((By.XPATH, xpath))).send_keys("webdriver" + Keys.DOWN)
                    
