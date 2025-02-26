import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
import pandas as pd


# Configurando o Brave como navegador.
brave_path = r"C:\Users\luanl\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"
options = Options()
options.binary_location = brave_path

# Parametros e inicialização.
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Conectar ao site
driver.get("https://www.kabum.com.br/hardware/placa-de-video-vga")

# Navegando pelos itens
item_list = driver.find_elements(By.CSS_SELECTOR, 'main.sc-e3e74830-9.ebKsig article')

data = []
# Retornando descrição e preço de cada item.
for item in item_list:
    description = item.find_element(By.CSS_SELECTOR, 'article > a > div > button > div > h3 > span').text
    price = item.find_element(By.CSS_SELECTOR, 'article > a > div > div.sc-57f0fd6e-0.eZSbFZ.availablePricesCard > div.flex.items-center.gap-6.h-\[22px\].tablet\:h-\[28px\] > span').text
#    print(description, "\n", price)
    data.append({'Name':description, 'Price':price})

def dataToCSV(dataDict:dict, filename:str):
    compressed_data = {k: [v] for k, v in dataDict.items()}
    df = pd.DataFrame(compressed_data)
    df.to_csv(filename, mode="a", index=False, header=not os.path.exists(filename))

plan = [dataToCSV(item, "GPUitems.csv") for item in data] 

time.sleep(8)



