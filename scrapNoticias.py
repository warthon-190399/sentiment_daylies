#%% funcion extractora del contenido de articulo
def article_content(url):
    try:
        print("Obteniendo contenido del artículo en:", url)
        response = requests.get(url)
        print("Parseando el contenido...")
        soup = BeautifulSoup(response.content, "html.parser")
        print("Extrayendo el texto del artículo...")
        article_text = soup.get_text()
        print("Contenido del artículo obtenido exitosamente.")
        return article_text
    
    except Exception as e:
        print("Error al obtener el contenido del artículo:", e)
        return None
#%% Scraper del grupo el comercio
import pandas as pd
import requests
from bs4 import BeautifulSoup

all_titulos = []
all_urls = []
all_fechas = []

for page_number in range(6,0,-1):
    url = f'https://peru21.pe/buscar/caso+rolex/todas/descendiente/{page_number}/'
    response = requests.get(url)

    if response.status_code == 200:

        soup = BeautifulSoup(response.content, 'html.parser') #parseamos el html

        #determinamos el titulo y el link de la noticia (href)
        titles = soup.find_all('a', class_="story-item__title")

        #determinamos los datos de tipo fecha
        dates = soup.find_all('p', class_='story-item__date')

        #extraemos la informacion de cada articulo
        for title, date in zip(titles, dates):
            all_titulos.append(title.text.strip())

           #all_urls.append(title["href"]) #si los urls ya contienen el dominio activas esta linea nomas
            
            # Agregar el prefijo "https://" a la URL
            url_prefix = "https://peru21.pe" #en estos caso concateno el dominio al url
            all_urls.append(url_prefix + title['href'])
            all_fechas.append(date.text.strip())
# Crear un DataFrame con la información recolectada
df = pd.DataFrame({
    'Titulo': all_titulos,
    'URL': all_urls,
    'Fecha': all_fechas
})
# Obtener el contenido de los artículos y agregarlo al DataFrame
df["Contenido"] = df["URL"].apply(article_content)
df.to_csv("peru21.csv", index=False)
#%%willax
import pandas as pd
import requests
from bs4 import BeautifulSoup
# Listas para almacenar los datos de todas las páginas
all_titulos = []
all_urls = []
all_fechas = []

#Iterar de acuerdo al numero de paginas
for page_number in range(6, 0, -1):
    url = f'https://willax.pe/result-search?result=Caso%20Rolex&page={page_number}'

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        #Encontramos los enclaces
        enlaces = soup.find_all("a", class_="col-md-4 mb-4 mb-xl-4 mb-lg-4 mb-md-4 mb-sm-5 mb-xs-5")

        #iteramos sobre los enlaces y extraemos la información
        for enlace in enlaces:
            #extraemos los titulos
            titulo_tag = enlace.find('p', class_='m-0 text-black m-0 p-0 mt-1')
            if titulo_tag:
                titulo = titulo_tag.find('b').text.strip()
            else:
                titulo = "No se encontró el título"
            all_titulos.append(titulo)

            #extraemos los enlaces
            url = enlace['href'] #en este caso no es necesario colocar el dominio
            all_urls.append(url)

            #Extraemos las fechas
            fecha_tag = enlace.find('span', class_='text-muted post-date')
            fecha = fecha_tag.text.strip() if fecha_tag else "No se encontró la fecha"
            all_fechas.append(fecha)
    else:
        print("Error al obtener la página:", response.status_code)

# Crear el DataFrame con todos los datos recopilados
df = pd.DataFrame({
    'Título': all_titulos,
    'URL': all_urls,
    'Fecha': all_fechas
})

df["Contenido"] = df["URL"].apply(article_content)
df.to_csv('willax.csv', index=False)
# %% RPP
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://rpp.pe/buscar")

search_box = driver.find_element(By.ID, "search-input-main") #id del buscador de noticias

search_box.clear()
search_box.send_keys("caso rolex") #noticias a buscar
search_box.send_keys(Keys.RETURN)
time.sleep(5)

all_titulos = []
all_urls = []
all_fechas = []

results = driver.find_elements(By.XPATH, "//div[@class='news__data']")

#iteramos sobre los resultados
for result in results:
    #extraemos titulo
    title_element = result.find_element(By.XPATH, ".//h2[@class='news__title']/a")
    title = title_element.text
    url = title_element.get_attribute("href")
    
    #Extraemos fechas
    date_element = result.find_element(By.XPATH, ".//time")
    date = date_element.get_attribute("data-x")
    
    print("Título:", title)
    print("URL:", url)
    print("Fecha:", date)
    print("-----------------")

    all_titulos.append(title)
    all_urls.append(url)
    all_fechas.append(date)

driver.quit()

df = pd.DataFrame({
    "Titulo":all_titulos,
    "URL":all_urls,
    "Fecha":all_fechas
})
df["Contenido"] = df["URL"].apply(article_content)
df.to_csv("rpp.csv", index=False)
# %% Latina
import requests
from bs4 import BeautifulSoup

all_titulos = []
all_urls = []
all_fechas = []
for page_number in range(16, 0, -1):
    url = f"https://latinanoticias.pe/page/{page_number}?s=caso+rolex&post_type=post"
    response = requests.get(url)
    html_content = response.text

    # Analizar el HTML con BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Encontrar todos los elementos de artículo
    articles = soup.find_all("article", class_="item-news")

    # Iterar sobre los artículos y extraer la información
    for article in articles:
        # Extraer el título y el URL del artículo
        title = article.find("h4", class_="title-news").text.strip()
        url = article.find("a", href=True)["href"]
        
        # Extraer la fecha
        date = article.find("time", class_="date-news").text.strip()
        
        # Imprimir la información
        print("Título:", title)
        print("URL:", url)
        print("Fecha:", date)
        print("----------")

        all_titulos.append(title)
        all_urls.append(url)    
    
        all_fechas.append(date)
        
df = pd.DataFrame({
    'Titulo': all_titulos,
    'URL': all_urls,
    'Fecha': all_fechas
})
# Obtener el contenido de los artículos y agregarlo al DataFrame
df["Contenido"] = df["URL"].apply(article_content)
df.to_csv("latina.csv", index=False)
