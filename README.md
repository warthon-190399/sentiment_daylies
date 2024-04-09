# Análisis de Sentimiento del Caso Rolex
Este proyecto de análisis de sentimiento se centra en examinar la cobertura mediática del escándalo del "Caso Rolex" en los diarios peruanos. Utiliza técnicas de procesamiento de lenguaje natural (NLP) y visualización de datos para ofrecer una comprensión detallada del tono y la tendencia de las noticias relacionadas con este caso.

## Descripción del Proyecto
El análisis se lleva a cabo utilizando datos recopilados de múltiples fuentes de noticias peruanas. Estos datos incluyen el contenido de los artículos, la fecha de publicación y el diario correspondiente.

## Estructura del Proyecto
El proyecto consta de los siguientes componentes principales:

- Extracción de Datos (scrapNoticias.py): Se realiza la extracción de información relevante para el análisis de los artículos publicados por cada diario seleccionado utilizando BeautifulSoup, Requests y Selenium
- Análisis y Visualización (app.py): Se emplean librerías especializadas en análisis de sentimiento como NLTK o VaderSentiment, y se utiliza Plotly y Streamlit para la visualización de datos como gráficos de barras, gráficos de dispersión y gráficos de líneas. Estas visualizaciones ayudan a comprender la frecuencia de publicaciones, la polaridad del sentimiento y otras métricas relevantes.

## Requerimientos del Sistema
Para ejecutar este proyecto, se necesitan las siguientes bibliotecas de Python:

- beautifulsoup4==4.12.3
- matplotlib==3.7.1
- nltk==3.8.1
- pandas==2.0.1
- plotly==5.14.1
- Requests==2.31.0
- selenium==4.19.0
- streamlit==1.29.0
- vaderSentiment==3.3.2
- wordcloud==1.9.3

Dichas librerías se pueden instalar con el siguiente comando:
  pip install pandas plotly matplotlib streamlit wordcloud nltk vaderSentiment requests beautifulsoup selenium

## Ejecución del proyecto

Para ejecutar la aplicación de Streamlit, simplemente ejecute el siguiente comando en la terminal desde el directorio raíz del proyecto:

streamlit run app.py

Una vez ejecutado, la aplicación estará disponible en su navegador web local.

##  Créditos
- Desarrollador: Tato Warthon
- Fuente de Datos: Los datos fueron recopilados mediante técnicas de extracción web de fuentes de noticias peruanas.
- Metodología: El análisis se realizó utilizando técnicas de procesamiento de lenguaje natural y visualización de datos.










