import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import unidecode
from PIL import Image
import time
#from dataprep.clean import clean_country

todos_streamings = pd.DataFrame()
tipos_graficos = ["Pyplot", "Seaborn"]

if 'tipo_grafico' not in st.session_state:
    st.session_state.tipo_grafico = "Pyplot"

if 'modulo_sistema' not in st.session_state:
    st.session_state.modulo_sistema = 'principal'

if 'quantidade_1' not in st.session_state:
    st.session_state.quantidade_1 = 10


def load_df_streamings():
    amazon = pd.read_csv('https://letscodeeleicao.s3.us-west-1.amazonaws.com/amazon_prime_titles.csv')
    netflix = pd.read_csv('https://letscodeeleicao.s3.us-west-1.amazonaws.com/netflix_titles.csv')
    disney = pd.read_csv('https://letscodeeleicao.s3.us-west-1.amazonaws.com/disney_plus_titles.csv')

    amazon.drop(['show_id'], axis=1, inplace=True)
    netflix.drop(['show_id'], axis=1, inplace=True)
    disney.drop(['show_id'], axis=1, inplace=True)

    global todos_streamings
    todos_streamings = pd.concat([netflix, amazon, disney])
    todos_streamings.cast.fillna('', inplace=True)
    todos_streamings.director.fillna('', inplace=True)
    todos_streamings.listed_in.fillna('', inplace=True)
    todos_streamings.country.fillna('', inplace=True)

    todos_streamings.title = todos_streamings.title.apply(lambda title: unidecode.unidecode(title))
    todos_streamings.director = todos_streamings.director.apply(lambda director: unidecode.unidecode(director))
    todos_streamings.cast = todos_streamings.cast.apply(lambda cast: unidecode.unidecode(cast))
    todos_streamings.listed_in = todos_streamings.listed_in.apply(lambda listed_in: unidecode.unidecode(listed_in))
    todos_streamings.country = todos_streamings.country.apply(lambda country: unidecode.unidecode(country))


def create_filter(container):
    if st.session_state.modulo_sistema == 'analise_1':
        container.subheader("Filtros")

        container.selectbox('Tipos de gráficos',
                            options=tipos_graficos,
                            key='tipo_grafico')

        container.slider('Quantidade de generos',
                         min_value=5,
                         max_value=15,
                         key='quantidade_1')


def create_sidebar():
    st.sidebar.title("Menu")

    st.sidebar.button("Principal",
                      key="id_principal",
                      on_click=change_module,
                      args=('principal',))

    st.sidebar.button("Equipe",
                      key="id_equipe",
                      on_click=change_module,
                      args=('equipe',))

    st.sidebar.button("1. Qual genero mais apareceu no geral",
                      key="id_analise1",
                      on_click=change_module,
                      args=('analise_1',))

    st.sidebar.button("2. Filmes por países",
                      key="id_analise2",
                      on_click=change_module,
                      args=('analise_2',))

    st.sidebar.button("3. Filmes por ano adicionados",
                      key="id_analise3",
                      on_click=change_module,
                      args=('analise_3',))

    st.sidebar.button("4. Gênero 2020/2021",
                      key="id_analise4",
                      on_click=change_module,
                      args=('analise_4',))

    st.sidebar.button("5. Média de duração dos filmes",
                      key="id_analise5",
                      on_click=change_module,
                      args=('analise_5',))

    st.sidebar.button("Encerramento",
                      key="id_encerramento",
                      on_click=change_module,
                      args=('encerramento',))


def principal():
    with st.container():
        st.empty()
        st.header("Plataformas de Streamings")
        image = Image.open('principal.jpg')
        st.image(image, caption="Netflix, Prime Vídeo, Disney+")

        st.subheader("Informações da Base de dados")
        st.text("""
            * Utilizamos três bases de dados, extraídas do site Kagle
            \n* São bases dos três principais serviços de streamings (Nettflix, Amazon Prime \ne Disney+)
            \n* Através das três bases coletadas utilizamos várias técnicas de 
            \nKDD (Knowledge Discovery in Databases - Extração de conhecimento)
            \n para criar uma base única, e que foi utilizada para nossas análises
        """)


def equipe():
    with st.container():
        st.empty()
        st.text("")
        st.header("Squad")
        st.subheader("⚡ Electus ⚡")
        image = Image.open('Equipe.png')
        st.image(image, caption="Equipe")


def analise_1():
    with st.container():
        global todos_streamings
        st.empty()
        st.header("1. Qual genero mais apareceu no geral")

        create_filter(st)

        generos = todos_streamings[["title", "listed_in"]].copy()
        generos = generos.listed_in.str.split(",").explode().fillna("Outros").str.strip()
        generos = generos.value_counts().reset_index()
        generos.columns = ["Gênero", "Quantidade de filmes"]
        generos = generos[:15]

        if st.session_state.quantidade_1 != None:
            generos = generos.head(st.session_state.quantidade_1)

        st.subheader("Dataframe")
        st.dataframe(generos)

        st.subheader("Gráfico")

        if st.session_state.tipo_grafico == "Pyplot":
            fig = px.bar(generos,
                         x="Quantidade de filmes",
                         y="Gênero",
                         orientation='h',
                         title='Quantidade de filmes por gênero')
            fig.update_yaxes(autorange="reversed")
            st.plotly_chart(fig)
        elif st.session_state.tipo_grafico == "Seaborn":
            fig, ax = plt.subplots()
            ax = sns.barplot(data=generos, x='Gênero', y='Quantidade de filmes', palette="flare")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=60)

            st.pyplot(fig)


def analise_2():
    with st.container():
        global todos_streamings
        st.empty()
        st.header("2. Filmes por países")

        create_filter(st)

        filmes_paises = todos_streamings[["title", "country"]].copy()
        filmes_paises = filmes_paises.country.str.split(",").explode().fillna("Outros").str.strip()
        filmes_paises = filmes_paises.value_counts().reset_index()
        filmes_paises.columns = ["País", "Quantidade de filmes"]
        filmes_paises = filmes_paises[1:11]
        #filmes_paises = clean_country(filmes_paises, 'País', output_format='alpha-3')
        filmes_paises['Pais_Text'] = filmes_paises['País'] + ' - ' + filmes_paises['Quantidade de filmes'].astype(str)
        filmes_paises.iloc[:, 0:2]

        st.subheader("Dataframe")
        st.dataframe(filmes_paises)

        st.subheader("Gráfico")

        fig = px.choropleth(filmes_paises,
                            locations="País_clean",
                            color="Pais_Text",
                            hover_name="Pais_Text")

        fig.update_layout(
            legend_title="País - Quantidade de Filmes"
        )
        st.plotly_chart(fig)


def analise_3():
    with st.container():
        pass


def analise_4():
    with st.container():
        pass


def analise_5():
    with st.container():
        pass


def encerramento():
    with st.container():
        st.empty()
        st.header('')
        st.text("")
        image = Image.open('encerramento.png')
        st.image(image, caption="Muito obrigado!")

        st.balloons()
        time.sleep(15)
        st.balloons()
        time.sleep(10)
        st.balloons()


def change_module(module='principal'):
    st.session_state.modulo_sistema = module


def main():
    create_sidebar()

    if len(todos_streamings) == 0:
        load_df_streamings()

    if st.session_state.modulo_sistema == 'principal':
        principal()
    elif st.session_state.modulo_sistema == 'equipe':
        equipe()
    elif st.session_state.modulo_sistema == 'analise_1':
        analise_1()
    elif st.session_state.modulo_sistema == 'analise_2':
        analise_2()
    elif st.session_state.modulo_sistema == 'analise_3':
        analise_3()
    elif st.session_state.modulo_sistema == 'analise_4':
        analise_4()
    elif st.session_state.modulo_sistema == 'analise_5':
        analise_5()
    elif st.session_state.modulo_sistema == 'encerramento':
        encerramento()


if __name__ == "__main__":
    main()
