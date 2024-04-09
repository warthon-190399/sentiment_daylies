import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.probability import FreqDist

st.set_page_config(
    page_title="Caso Rolex: Análisis de Sentimiento",
    page_icon=":newspaper:",
    layout="wide",
    initial_sidebar_state="expanded"
)

df_exten = pd.read_csv("consolidado.csv")
df_general = df_exten[~df_exten['Diario'].isin(['Correo', 'Gestion', 'Ojo', 'Peru21'])]

st.title("Análisis de Sentimiento del Caso Rolex")
st.write("¡Bienvenido al análisis de sentimiento de los diarios peruanos sobre el escándalo del Caso Rolex!")

st.sidebar.title("Panel de Selección")
st.sidebar.write("En este panel puedes seleccionar el diario de tu interés y también filtrar por fechas.")

options = ["Agrupado"] + df_exten["Diario"].unique().tolist()
selected_diario = st.sidebar.selectbox("Seleccione el diario de interés", options)

if selected_diario == "Agrupado":
    selected_df = df_general
else:
    selected_df = df_exten[df_exten["Diario"] == selected_diario]
#%% Grafica temporal

selected_df["Fecha"] = pd.to_datetime(selected_df["Fecha"])
selected_df["Dia"] = selected_df["Fecha"].dt.date
df_count = selected_df.groupby(["Dia"]).size().reset_index(name='Count')

# Crear el gráfico adecuado según la selección

st.subheader(f"Análisis de: {selected_diario}")
st.divider()

if selected_diario == "Agrupado":
    # Gráfico de densidad heatmap
    fig_density = px.density_heatmap(selected_df,
                                     x='Dia',
                                     y='Diario',
                                     template="plotly_dark",
                                     )
    fig_density.update_layout(
        title='Heatmap de Diarios y Días',
        xaxis=dict(title='Día'),
        yaxis=dict(title='Diario')
    )
    st.subheader("Frecuencia de Publicaciones")
    st.plotly_chart(fig_density, use_container_width=True)

else:
    fig_bar = px.bar(df_count,
                     x='Dia',
                     y='Count',
                     template="plotly_dark",
                     color_continuous_scale='Agsunset',
                     color="Count",
                     labels={'Count': 'Número de publicaciones'})
    fig_bar.update_layout(
        title=f'Publicaciones diarias de {selected_diario}',
        xaxis=dict(title='Día'),
        yaxis=dict(title='Número de publicaciones')
    )
    st.subheader("Frecuencia de Publicaciones")
    st.plotly_chart(fig_bar, use_container_width=True)

# Aquí van los cambios para el filtro de fecha
st.sidebar.write("Filtrar por fecha:")
start_date = st.sidebar.date_input("Desde", pd.to_datetime("2024-03-15"))
end_date = st.sidebar.date_input("Hasta", pd.to_datetime("2024-04-08"))

selected_df = selected_df[(selected_df["Fecha"] >= pd.to_datetime(start_date)) & (selected_df["Fecha"] <= pd.to_datetime(end_date))]

#%% Tokenizacion
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words("spanish"))

def preprocess_text(text):
    tokens = word_tokenize(text.lower(), language="spanish")
    cleaned_tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    return " ".join(cleaned_tokens)

selected_df["Contenido_Limpio"] =  selected_df["Contenido"].apply(preprocess_text)
#%% Diseño de Wordcloud
text = " ".join(selected_df["Contenido_Limpio"])
wordcloud = WordCloud(width=800,
                      height=400,
                      background_color='black').generate(text)
plt.figure(figsize=(15, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')

#%% Palabras comunes
tokens = word_tokenize(text)
frec = FreqDist(tokens)
most_c = frec.most_common(10)
df_most_c = pd.DataFrame(most_c, columns=["Palabra", "Frecuencia"])

fig_most_c = px.bar(df_most_c,
             x='Palabra',
             y='Frecuencia',
             color="Frecuencia",
             #title='Palabras más frecuentes en los artículos',
             template = "plotly_dark",
             labels={
                 'Palabra': 'Palabra',
                 'Frecuencia': 'Frecuencia'
                 },
             height=350,
             color_continuous_scale='Agsunset'
            )
fig_most_c.update_xaxes(tickangle=45)
#%% Función Polaridad
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment_vader(text):
    # Obtener el puntaje de sentimiento compuesto
    sentiment = analyzer.polarity_scores(text)
    return sentiment['compound']

# Aplicar la función de análisis de sentimientos a cada artículo
selected_df["Sentimiento_Vader"] = selected_df["Contenido"].dropna().apply(analyze_sentiment_vader)
#%%Definir el rango de polaridad
rango_polaridad = {
    "Muy Negativo": (-1, -0.5),
    "Negativo": (-0.5, 0),
    "Neutral": (-0.1, 0.1),
    "Positivo": (0, 0.5),
    "Muy Positivo": (0.5, 1)
}

# Función para asignar la categoría de polaridad a un valor
def nombre_polaridad(valor):
    for nombre, (inicio, fin) in rango_polaridad.items():
        if inicio < valor <= fin:
            return nombre

# Aplicar la función de polaridad y crear la columna "Categoria_Polaridad"
selected_df["Categoria_Polaridad"] = selected_df["Sentimiento_Vader"].apply(nombre_polaridad)

# Calcular el conteo de polaridad por diario
conteo_polaridad_diario = selected_df.groupby(['Diario', 'Categoria_Polaridad']).size().reset_index(name='Cantidad_Articulos')

# Crear el gráfico de barras agrupadas
fig_bar_polarG = px.bar(conteo_polaridad_diario,
                                   x='Categoria_Polaridad',
                                   y='Cantidad_Articulos',
                                   color='Diario',
                                   color_discrete_sequence=px.colors.qualitative.Alphabet_r,
                                   barmode='group',  # Agrupar las barras
                                   template="plotly_dark",
                                   height=350,
                                   title='Conteo de Polaridad por Diario',
                                   labels={'Categoria_Polaridad': 'Categoría de Polaridad', 'Cantidad_Articulos': 'Cantidad de Artículos'})


#%% Histograma Polaridad
fig_sentiment_vader = px.histogram(selected_df,
                                   x="Sentimiento_Vader",
                                   color="Diario",
                                   template="plotly_dark",
                                   color_discrete_sequence=px.colors.qualitative.Alphabet_r,
                                   title="Análisis de Sentimiento con VaderSentiment",
                                   labels={'Sentimiento_Vader': 'Polaridad del Sentimiento'}
                                   )
fig_sentiment_vader.update_layout(xaxis_title='Polaridad del Sentimiento',
                                  yaxis_title='Número de Artículos'
                                  )
#%% Fecha vs Sentimiento
selected_df['Contenido_Extension'] = selected_df['Contenido'].str.len()
fig_bubble = px.scatter(selected_df,
                        x='Fecha',
                        y='Sentimiento_Vader',
                        size='Contenido_Extension',
                        color='Diario',
                        template="plotly_dark",
                        color_discrete_sequence=px.colors.qualitative.Alphabet_r,
                        title='Longitud del Artículo, Polaridad del Sentimiento y Fecha',
                        labels={'Fecha': 'Hora de Publicación',
                                'Sentimiento_Vader': 'Polaridad del Sentimiento'})
fig_bubble.update_traces(marker=dict(opacity=0.8))
fig_bubble.update_layout(xaxis_title='Fecha de Publicación', yaxis_title='Polaridad del Sentimiento')
#%% Extension vs Sentimiento
fig_scatterExt = px.scatter(selected_df,
                            x='Sentimiento_Vader',
                            y='Contenido_Extension',
                            color="Diario",
                            title='Polaridad del Sentimiento vs. Longitud del Artículo',
                            template="plotly_dark",
                            color_discrete_sequence=px.colors.qualitative.Alphabet_r,
                            labels={'Sentimiento_Vader': 'Polaridad del Sentimiento',
                                    'Contenido_Extension': 'Longitud del Artículo'})
fig_scatterExt.update_traces(marker=dict(size=10, opacity=0.8)) 
fig_scatterExt.update_layout(hovermode='x unified')
#%%
df_sentimiento_promedio = selected_df.groupby(['Dia', 'Diario'])['Sentimiento_Vader'].mean().reset_index()

# Crear el gráfico de línea
fig_line = px.line(df_sentimiento_promedio,
                    x='Dia',  # Usar 'Dia' en lugar de 'dia'
                    y='Sentimiento_Vader',
                    color="Diario",
                    color_discrete_sequence=px.colors.qualitative.Alphabet_r,
                    title='Sentimiento Promedio por Día',
                    template="plotly_dark",
                    height=350,
                    labels={'Dia': 'Día', 'Sentimiento_Vader': 'Sentimiento Promedio'})  # Usar 'Dia' en lugar de 'dia

#%%Columnas y presentacion
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Análisis de Contenido de {selected_diario}")
    st.pyplot(plt.gcf())
    st.subheader(f"Análisis de Sentimiento de {selected_diario}")
    st.plotly_chart(fig_bar_polarG, use_container_width=True)
    st.plotly_chart(fig_sentiment_vader, use_container_width=True)
    st.plotly_chart(fig_scatterExt, use_container_width=True)
with col2:
    st.write("")
    st.write("")
    st.plotly_chart(fig_most_c, use_container_width=True)
    st.plotly_chart(fig_line, use_container_width=True)
    st.plotly_chart(fig_bubble, use_container_width=True)
    with st.expander("Acerca de:", expanded=False):
        st.write(
        """
        - :orange[**Realizado por:**] [Tato Warthon](https://github.com/warthon-190399).
        - :orange[**Fuente**]: Los datos fueron recopilados mediante el uso de técnicas de extracción web, que implican la obtención automatizada de información de sitios web seleccionados. Estos datos pueden incluir noticias, artículos o cualquier otro contenido relevante relacionado con el caso Rolex. Se aplicaron técnicas de procesamiento de lenguaje natural para analizar el sentimiento y las tendencias en el contenido extraído.
        - :orange[**Metodología**]: 
            - Seleccionar fuentes de información relevantes para el caso Rolex.
            - Implementar técnicas de extracción web para recopilar datos de estas fuentes.
            - Procesar y limpiar los datos para su análisis.
            - Aplicar análisis de sentimiento para evaluar la actitud y el tono de los textos.
            - Visualizar los resultados mediante gráficos interactivos y herramientas de análisis.
        """
    )







