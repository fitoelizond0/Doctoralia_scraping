from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from bs4 import BeautifulSoup
import time  # Importa la biblioteca time para pausas

# Configura el webdriver. Asumiré que estás usando Chrome.
driver = webdriver.Chrome()

# Navega a la página web deseada para extraer las URLs.
url = "https://www.doctoralia.com.mx/buscar?q=Traumat%C3%B3logo&loc=Monterrey&filters%5Bspecializations%5D%5B0%5D=91&page=14"
driver.get(url)

# Encuentra los elementos que contienen las URLs.
url_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-id="address-context-cta"]')

# Utilizamos un conjunto para almacenar las URLs únicas.
unique_urls = set()

# Guarda las URLs en un archivo 'urls.txt'.
with open('urls.txt', 'w') as file:
    for element in url_elements:
        url = element.get_attribute('href')
        unique_urls.add(url)  # Agregamos la URL al conjunto
        file.write(url + '\n')

# Ahora procesamos las URLs guardadas y extraemos los números.
with open('doctoralia.txt', 'a') as output_file:  # Cambiamos 'w' a 'a'
    for url in unique_urls:  # Iteramos solo sobre URLs únicas
        # Navegar a la URL actual en la misma instancia del navegador
        driver.get(url)

        # Espera unos segundos para que la página se cargue completamente.
        time.sleep(3)

        # Busca nuevamente los elementos por su atributo `data-id`.
        all_data_ids = driver.find_elements(By.CSS_SELECTOR, '[data-id]')

        # Utilizamos un conjunto para almacenar y verificar los números únicos.
        unique_numbers = set()

        for element in all_data_ids:
            data_id_value = element.get_attribute('data-id')
            # Usamos una expresión regular para encontrar números de teléfono válidos.
            phone_numbers = re.findall(r'\d{8,}', data_id_value)
            for phone_number in phone_numbers:
                unique_numbers.add(phone_number)

        output_file.write(f"Resultados para {url}:\n")
        
        # Utiliza el conjunto unique_numbers para evitar duplicados.
        for number in unique_numbers:
            output_file.write(f"Teléfono: {number}\n")

print("Proceso completado. Los resultados se guardaron en 'doctoralia.txt'.")














