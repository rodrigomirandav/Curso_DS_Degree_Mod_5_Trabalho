import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import unidecode
from PIL import Image

# from dataprep.clean import clean_country
container_id = "id_principal"


def create_sidebar():
    st.sidebar.title("Menu")
    st.sidebar.button("Principal", key="id_principal", on_click=principal)
    st.sidebar.button("Equipe", key="id_equipe", on_click=equipe)
    st.sidebar.button("Equipe", key="id_equipe1")
    st.sidebar.button("Equipe", key="id_equipe2")
    st.sidebar.button("Equipe", key="id_equipe3")
    st.sidebar.button("Equipe", key="id_equipe4")
    st.sidebar.button("Equipe", key="id_equipe5")


def main():
    create_sidebar()


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
            \n* Através das três bases coletadas utilizamos várias técnicas de \nKDD (Knowledge Discovery in Databases - Extração de conhecimento)\n para criar uma base única, e que foi utilizada para nossas análises
        """)


def equipe():
    with st.container():
        st.empty()
        st.text("")
        st.header("Squad")
        st.subheader("Electus")
        image = Image.open('Equipe.png')
        st.image(image, caption="Equipe")


if __name__ == '__main__':
    main()
