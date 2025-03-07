import mysql
import mysql.connector
import os
from dotenv import load_dotenv
from data import gpu_scrape

load_dotenv()

def add(item):
    command = f"""
    INSERT INTO gpu (gpu_model, gpu_price, gpu_url)
    VALUES (%s, %s, %s);
    """

    try:
        with mysql.connector.connect(
            host= "127.0.0.1",
            user= os.environ.get("MYSQL_USER"),
            passwd= os.environ.get("MYSQL_PASS"),
            database= os.environ.get("MYSQL_DB")
        ) as connection:
            with connection.cursor() as cursor:

                data = (item.model,
                        item.price,
                        item.url)
                
                cursor.execute(command, data)

                connection.commit()
            
        print("Adicionado a KBM Scrape")
    except mysql.connector.Error as erro:
        print(f"Erro: {erro}")

for item in gpu_scrape:
    add(item)