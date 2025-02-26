import requests 
from bs4 import BeautifulSoup
import re
import pandas as pd
import math

url = "https://www.kabum.com.br/hardware/placa-de-video-vga"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
items = soup.find('div', id="listingCount").get_text().strip()  
