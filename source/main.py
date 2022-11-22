import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import tabula
from pathlib import Path
import requests
import pandas as pd

path = "../webdriver"
route_driver = os.environ["PATH"] + path
service = Service(executable_path=route_driver)
driver = webdriver.Chrome(service=service)

web = "http://boletin.precioscorabastos.com.co/"

driver.get(web)
time.sleep(2)
pdf_links = []

for pages in range(0,12):
   
    dates_prices =  driver.find_elements(by="xpath", value="//td/a[@class='fc-day-grid-event fc-h-event fc-event fc-start fc-end']")

    for dates in dates_prices:
        
        try:
            dates.click()    
                        
        except Exception as e:
            print(e)
        
        download_link = driver.find_element(by="xpath", value="//div/a[@class='eaelec-event-details-link']").get_attribute('href')
        pdf_links.append(download_link)
        close_window = driver.find_element(by="xpath", value="//i[@class='fas fa-times']")

        try:
            close_window.click()
        except Exception as e:
            print(e)

    num_page = driver.find_element(by="xpath", value="/html/body/div/div/div/div/div/div/section[3]/div/div/div/div/div/div/div/div/div[1]/div[1]/div[1]/div/button[1]")
    try:
        num_page.click()
    except Exception as e:
        print(e)
number_for_name = 0
for link in pdf_links:
    number_for_name += 1
    print(link)
    name_for_file = link.split("-")
    filename = Path(str(number_for_name)+".pdf")
    url_pdf = link
    response = requests.get(url_pdf)
    filename.write_bytes(response.content)  
    
driver.quit()

# Etapa en la que convertimos pdf a csv
# Read a PDF File

k = 1
for i in range(1,32):
    # Read a PDF File
    df = tabula.read_pdf(str(k), pages='all')[0]
    # convert PDF into CSV
    tabula.convert_into(str(k), str(k)+".csv", output_format="csv", pages='all')
    print(df)
    k += 1
