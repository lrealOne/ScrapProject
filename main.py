import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


# Configurando o Brave como navegador.
brave_path = r"C:\Users\luanl\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"
options = Options()
options.binary_location = brave_path
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

# Parametros e inicialização.
service = Service(ChromeDriverManager().install()) 
driver = webdriver.Chrome(service=service, options=options)


data = []
page = 1
# Retornando descrição e preço de cada item.
while True:
    try:
        driver.get(f"https://www.kabum.com.br/hardware/placa-de-video-vga?page_number={page}&page_size=20&facet_filters=&sort=most_searched")
    except:
        print("Over")

    time.sleep(3)
    
    try:
        print(f"Página {page}")

        # Tempo de carregamento..
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'main.sc-e3e74830-9.ebKsig article'))
        )

        # Scrap
        item_list = driver.find_elements(By.CSS_SELECTOR, 'main.sc-e3e74830-9.ebKsig article')

        # Scroll até o botão e clica nele
        ahead = driver.find_element(By.XPATH, "//*[@id='listingPagination']/ul/li[13]/a")
        driver.execute_script("arguments[0].scrollIntoView(true);", item_list[-1])
        
        # Extraindo...
        for item in item_list:
            try:
                description = item.find_element(By.CSS_SELECTOR, 'article > a > div > button > div > h3 > span').text
                try:
                    price = item.find_element(By.CSS_SELECTOR, r'article > a > div > div.sc-57f0fd6e-0.eZSbFZ.availablePricesCard > div.flex.items-center.gap-6.h-\[22px\].tablet\:h-\[28px\] > span').text
                    print(description, "-", price)
                except:
                    print(description, "-", "Unavailable")
                    price = "Unavailable"
                data.append({'Name': description, 'Price': price})
            except Exception as e:
                print(f"!!ERRO!! \n Item: {e}")

        time.sleep(10)

        # Próxima pagina
        page += 1
        driver.refresh()

        # Tempo de carregamento..
        WebDriverWait(driver, 10).until(
            EC.staleness_of(item_list[0])  # Aguarda os itens antigos sumirem
        )
        
    except:
        print("Fim.")
        break


def dataToCSV(dataDict:dict, filename:str):
    compressed_data = {k: [v] for k, v in dataDict.items()}
    df = pd.DataFrame(compressed_data)
    df.to_csv(filename, mode="a", index=False, header=not os.path.exists(filename))

plan = [dataToCSV(item, "GPUitems.csv") for item in data.sort()] 

time.sleep(8)
driver.quit()


