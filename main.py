import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import unidecode
from PIL import Image
import time

todos_streamings = pd.DataFrame()
df_paises = pd.DataFrame()
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

    global df_paises
    df_paises = pd.read_csv('https://letscodeeleicao.s3.us-west-1.amazonaws.com/paises.csv', sep=";")

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
        global df_paises
        st.empty()
        st.header("2. Filmes por países")

        create_filter(st)

        filmes_paises = todos_streamings[["title", "country"]].copy()
        filmes_paises = filmes_paises.country.str.split(",").explode().fillna("Outros").str.strip()
        filmes_paises = filmes_paises.value_counts().reset_index()
        filmes_paises.columns = ["País", "Quantidade de filmes"]
        filmes_paises = filmes_paises.merge(df_paises, how='left', left_on='País', right_on='Pais')
        filmes_paises['Pais_Text'] = filmes_paises['País'] + ' - ' + filmes_paises['Quantidade de filmes'].astype(str)
        filmes_paises.dropna(inplace=True)

        st.subheader("Dataframe")
        st.dataframe(filmes_paises.iloc[:, 0:2])

        st.subheader("Gráfico")

        fig = px.choropleth(filmes_paises,
                            locations="Pais_clean",
                            color="Pais_Text",
                            hover_name="Pais_Text")

        fig.update_layout(
            legend_title="País - Quantidade de Filmes"
        )
        st.plotly_chart(fig)


def analise_3():
    with st.container():
        global todos_streamings
        st.empty()
        st.header("3. Filmes por ano adicionados")

        create_filter(st)

        streamings_anos = todos_streamings[["title", "date_added"]].copy()
        streamings_anos = streamings_anos.date_added.str.split(expand=True)[2].fillna("Sem ano").value_counts()
        streamings_anos = streamings_anos.reset_index()
        streamings_anos.columns = ["Ano", "Quantidade de filmes"]
        streamings_anos = streamings_anos[streamings_anos.Ano != 'Sem ano']

        # if st.session_state.quantidade_1 != None:
        #    generos = generos.head(st.session_state.quantidade_1)

        st.subheader("Dataframe")
        st.dataframe(streamings_anos)

        st.subheader("Gráfico")

        # if st.session_state.tipo_grafico == "Pyplot":
        #     fig = px.bar(generos,
        #                  x="Quantidade de filmes",
        #                  y="Gênero",
        #                  orientation='h',
        #                  title='Quantidade de filmes por gênero')
        #     fig.update_yaxes(autorange="reversed")
        #     st.plotly_chart(fig)
        # elif st.session_state.tipo_grafico == "Seaborn":
        #     fig, ax = plt.subplots()
        #     ax = sns.barplot(data=generos, x='Gênero', y='Quantidade de filmes', palette="flare")
        #     ax.set_xticklabels(ax.get_xticklabels(), rotation=60)
        #
        #     st.pyplot(fig)


def analise_4():
    with st.container():
        global todos_streamings
        st.empty()
        st.header("4. Gênero 2020/2021")

        create_filter(st)

        genero_por_ano = todos_streamings[["release_year", "listed_in"]].copy()
        genero_por_ano.set_index('release_year', inplace=True)
        genero_por_ano = genero_por_ano.listed_in.str.split(",").explode().str.strip()
        genero_por_ano = genero_por_ano.reset_index()
        genero_por_ano = genero_por_ano[genero_por_ano["release_year"] >= 2020]
        genero_por_ano['Quantidade de filmes'] = 1

        genero_por_ano_2020 = genero_por_ano[genero_por_ano['release_year'] == 2020]
        genero_por_ano_2020 = genero_por_ano_2020.reset_index()
        genero_por_ano_2020['release_year'] = 'Ano 2020'
        genero_por_ano_2020 = genero_por_ano_2020.groupby(['release_year', 'listed_in'])['Quantidade de filmes'].sum()
        genero_por_ano_2020 = genero_por_ano_2020.to_frame().head(10).sort_values('Quantidade de filmes',
                                                                                  ascending=False)

        genero_por_ano_2021 = genero_por_ano[genero_por_ano['release_year'] == 2021]
        genero_por_ano_2021 = genero_por_ano_2021.reset_index()
        genero_por_ano_2021['release_year'] = 'Ano 2021'
        genero_por_ano_2021 = genero_por_ano_2021.groupby(['release_year', 'listed_in'])['Quantidade de filmes'].sum()
        genero_por_ano_2021 = genero_por_ano_2021.to_frame().head(10).sort_values('Quantidade de filmes',
                                                                                  ascending=False)

        genero_por_ano = pd.concat([genero_por_ano_2020, genero_por_ano_2021])
        genero_por_ano = genero_por_ano.reset_index()
        genero_por_ano.columns = ['Ano', 'Gênero', 'Quantidade de filmes']
        genero_por_ano.set_index(['Ano', 'Gênero'])

        # if st.session_state.quantidade_1 != None:
        #    generos = generos.head(st.session_state.quantidade_1)

        st.subheader("Dataframe")
        st.dataframe(genero_por_ano)

        st.subheader("Gráfico")

        if st.session_state.tipo_grafico == "Pyplot":
            fig = fig = px.bar(genero_por_ano,
                               x="Gênero",
                               y="Quantidade de filmes",
                               color="Ano",
                               barmode='group',
                               title="Gêneros 2020/2021")
            st.plotly_chart(fig)
        elif st.session_state.tipo_grafico == "Seaborn":
            pass


def analise_5():
    with st.container():
        global todos_streamings
        st.empty()
        st.header("6. Média de duração dos filmes")

        create_filter(st)

        duracao_media_filmes = todos_streamings.query('type=="Movie"')[["type", "duration"]].copy()
        duracao_media_filmes.duration.replace(r'[a-z]+', '', regex=True, inplace=True)
        duracao_media_filmes.duration.dropna().astype(int).max()
        classes = [50, 70, 90, 110, 130, 150, duracao_media_filmes.duration.dropna().astype(int).max()]
        labels = ['50', '70', '90', '110', '130', '150']
        duracao_media_filmes = duracao_media_filmes.dropna()
        duracao_media_filmes.duration = duracao_media_filmes.duration.astype(int)
        duracao_media_filmes['duracao'] = pd.cut(x=duracao_media_filmes.duration, bins=classes, labels=labels)
        duracao_media_filmes['qtd'] = 1
        duracao_media_filmes = duracao_media_filmes.groupby(['duracao'])['qtd'].sum()
        duracao_media_filmes = duracao_media_filmes.reset_index()
        duracao_media_filmes.columns = ['Duração', 'Quantidade de filmes']

        # if st.session_state.quantidade_1 != None:
        #    generos = generos.head(st.session_state.quantidade_1)

        st.subheader("Dataframe")
        st.dataframe(duracao_media_filmes)

        st.subheader("Gráfico")

        if st.session_state.tipo_grafico == "Pyplot":
            fig = px.histogram(duracao_media_filmes,
                               x="Duração",
                               y="Quantidade de filmes",
                               title="Duração dos filmes")
            fig.update_yaxes(title="Quantidade de filmes")
            st.plotly_chart(fig)
        elif st.session_state.tipo_grafico == "Seaborn":
            pass


def encerramento():
    with st.container():
        for i in range(2):
            st.empty()
            st.header('')
            st.text("")
            time.sleep(1)

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
