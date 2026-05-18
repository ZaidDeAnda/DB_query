import streamlit as st
import pandas as pd
import plotly.express as px

from utils.database import get_mongo_client
from utils.config import Config
from utils.data import load_data
from utils.data import generate_individual_dataframe
from utils.data import generate_individual_poverty_dataframe
from utils.data import generate_housing_dataframe
from utils.data import generate_housing_poverty_dataframe
from utils.data import to_excel
from utils.authentication import check_password

config = Config()

st.set_page_config(layout="wide")

# Autenticacion
if check_password(config):

    st.header("Visualización de datos")

    #Carga los datos
    client = get_mongo_client(config)
    
    programa_df = load_data()

    # Filtro para los datos

    seleccion = st.selectbox("Seleccione opción", options=["Visualizar por individuo", "Visualizar por vivienda"])

    visualization_first_row = st.columns(2)

    visualization_second_row = st.columns(2)

    if seleccion == "Visualizar por individuo":

        #Transformacion de los datos

        objective_dataframe = generate_individual_dataframe(programa_df)

        poverty_individual_dataframe = generate_individual_poverty_dataframe(programa_df)

        #Visualizacion
        
        visualization_first_row[0].subheader("Estado de los registros de la ruta por programa")

        visualization_first_row[0].dataframe(objective_dataframe)

        visualization_first_row[0].download_button("Descargar excel", data=to_excel(objective_dataframe), file_name = "indicadores_programa.xlsx")

        visualization_second_row[0].subheader("Estado de los registros de la ruta por situación socioeconómica")

        visualization_second_row[0].dataframe(poverty_individual_dataframe.astype(float), width=1200)

        visualization_second_row[0].download_button("Descargar excel", data=to_excel(poverty_individual_dataframe), file_name = "indicadores_pobreza.xlsx")
    
    elif seleccion == "Visualizar por vivienda":

        #Transformacion de los datos

        objective_dataframe = generate_housing_dataframe(programa_df)

        poverty_housing_dataframe = generate_housing_poverty_dataframe(objective_dataframe)

        #Visualiazciobn

        visualization_first_row[0].dataframe(objective_dataframe, width=1200)

        visualization_first_row[0].download_button("Descargar excel", data=to_excel(objective_dataframe), file_name = "indicadores_viviendas.xlsx")   

        visualization_first_row[0].subheader("Situación socioeconómica de las viviendas beneficiadas")

        visualization_second_row[0].dataframe(poverty_housing_dataframe, width=1200)

        visualization_second_row[0].download_button("Descargar excel", data=to_excel(poverty_housing_dataframe), file_name = "indicadores_vivienda_pobreza.xlsx")
