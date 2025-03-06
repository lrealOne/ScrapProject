import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

data = []
def ScrapeKBM():
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

    page = 25
    # Retornando descrição e preço de cada item.
    while True:
        time.sleep(3)

        # if page != 1:
        #     WebDriverWait(driver, 20).until(
        #         EC.staleness_of(item_list[0])  # Aguarda os itens antigos sumirem
        #     )

        try:
            driver.get(f"https://www.kabum.com.br/hardware/placa-de-video-vga?page_number={page}&page_size=20&facet_filters=&sort=most_searched")
        except:
            driver.quit()

        time.sleep(3)
        
        try:
            print(f"Página {page}")

            # Tempo de carregamento..
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'main.sc-e3e74830-9.ebKsig article'))
            )

            # Scrap
            item_list = driver.find_elements(By.CSS_SELECTOR, 'main.sc-e3e74830-9.ebKsig article')
            
            # Extraindo...
            for item in item_list:
                try:
                    model = item.find_element(By.CSS_SELECTOR, 'article > a > div > button > div > h3 > span').text
                    url = item.find_element(By.CSS_SELECTOR, 'article > a').get_attribute('href')
                    try:
                        price = item.find_element(By.CSS_SELECTOR, r'article > a > div > div.sc-57f0fd6e-0.eZSbFZ.availablePricesCard > div.flex.items-center.gap-6.h-\[22px\].tablet\:h-\[28px\] > span').text
                    except:
                        price = "Unavailable"
                    data.append({'Model': model, 'Price': price, 'URL': url})
                except Exception as e:
                    print(f"!!ERRO!! \n Item: {e}")

        
            # Próxima pagina
            page += 1
            time.sleep(5)
            driver.refresh()
            
        except:
            print("Fim.")
            break

    time.sleep(8)
    

ScrapeKBM()






    
