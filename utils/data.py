import pandas as pd
import streamlit as st
import warnings
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
from sqlalchemy import create_engine
warnings.filterwarnings('ignore')

from utils.dict_utils import ESTATUS
from utils.config import Config

config = Config()

@st.cache(allow_output_mutation=True)
def load_data(sql_connection=False):
    """Carga los datos referentes a los programas sociales.

        Params
        ------
        sql_connection: Bool
        Debe ser True si desea conectarse a la base de datos 
        sql mantenida en la nube, de lo contrario usará un
        csv proporcionado.

        Returns
        -------
        programa_df : pd.DataFrame
            Un dataframe conteniendo toda la información referente a 
            los programas sociales.
        """
    if sql_connection:

        sql_data = config.get_config()["sql"]

        DATABASE_CONNECTION = f'mssql://{sql_data["USERNAME"]}:{sql_data["PASSWORD"]}@{sql_data["SERVER"]}/{sql_data["DATABASE"]}?driver={sql_data["DRIVER"]}'

        engine = create_engine(DATABASE_CONNECTION)
        connection = engine.connect()

        query = 'SELECT * FROM VW_PROGRAMAS_SOCIALES_CHECS'

        data = pd.read_sql_query(query,connection)

    else:

        data = pd.read_csv("data_zaid.csv")

    data["NombrePrograma"] = data["NombrePrograma"].fillna("Sin programa")
    programa_df = data
    programa_df["Status"] = programa_df["IDEstatusBeneficiario"].map(ESTATUS)
    programa_df.loc[~programa_df["Descripcion_Inconsistencia"].isnull(), "Descripcion_Inconsistencia"] = "Datos con inconsistencia"
    programa_df.loc[(programa_df["Status"].isnull()) & (programa_df["Descripcion_Inconsistencia"].isnull()), "Status"] = "Sin asignar"

    programa_df["TipoPobreza"] = programa_df["TipoPobreza"].fillna("Por definir")

    return programa_df

@st.cache(allow_output_mutation=True)
def generate_individual_dataframe(programa_df):
    """Genera un dataframe con codificacion one-hot sobre
        los programas sociales y su status por individuo.

        Params
        ------
        programa_df : pd.DataFrame
        un dataframe de pandas conteniendo toda la informacion 
        sobre los programas sociales
        
        Returns
        -------
        individuos_df : pd.DataFrame
            Un dataframe conteniendo la informacion sobre los
            programas sociales con codificacion one-hot por individuo.
        """

    individuos_dummies = pd.get_dummies(programa_df[["Status", "Descripcion_Inconsistencia"]], prefix="", prefix_sep="")
    individuos_dummies[["NombrePrograma", "Status"]] = programa_df[["NombrePrograma", "Status"]]
    individuos_df = individuos_dummies.groupby("NombrePrograma").sum()

    cols = individuos_df.columns.tolist()
    cols = cols[:3] + cols[4:] + cols[3:4]
    individuos_df = individuos_df[cols]
    
    individuos_df["total"] = individuos_df[list(individuos_df.columns)].sum(axis=1)

    return individuos_df

@st.cache(allow_output_mutation=True)
def generate_individual_poverty_dataframe(programa_df):
    """Genera un dataframe con codificacion one-hot sobre
        el tipo de pobreza de los individuos y su status.

        Params
        ------
        programa_df : pd.DataFrame
        un dataframe de pandas conteniendo toda la informacion 
        sobre los programas sociales
        
        Returns
        -------
        pobreza_df : pd.DataFrame
            Un dataframe conteniendo la informacion sobre los
            tipos de pobreza de los individuos con codificacion 
            one-hot.
        """
    
    pobreza_dummies = pd.get_dummies(programa_df[["Status", "Descripcion_Inconsistencia"]], prefix="", prefix_sep="")
    pobreza_dummies[["NombrePrograma", "Status", "TipoPobreza"]] = programa_df[["NombrePrograma", "Status", "TipoPobreza"]]
    pobreza_df = pobreza_dummies.groupby("TipoPobreza").sum()
    pobreza_df["total"] = pobreza_df[list(pobreza_df.columns)].sum(axis=1)

    return pobreza_df


@st.cache(allow_output_mutation=True)
def generate_housing_dataframe(programa_df):
    """Genera un dataframe con codificacion one-hot sobre
        los programas sociales y su status por vivienda.

        Params
        ------
        programa_df : pd.DataFrame
        un dataframe de pandas conteniendo toda la informacion 
        sobre los programas sociales
        
        Returns
        -------
        vivienda_df : pd.DataFrame
            Un dataframe conteniendo la informacion sobre los
            programas sociales con codificacion one-hot por vivienda.
        """

    programa_df_por_vivienda = pd.get_dummies(programa_df[["NombrePrograma","Status"]], prefix="", prefix_sep="")
    programa_df_por_vivienda[["IDVivienda","TipoPobreza"]] = programa_df[["IDVivienda","TipoPobreza"]]
    cols = programa_df_por_vivienda.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    programa_df_por_vivienda = programa_df_por_vivienda[cols]

    vivienda_df = programa_df_por_vivienda.groupby("IDVivienda").sum()
    vivienda_df["Habitantes"] = vivienda_df["Hambre Cero"] + \
                                vivienda_df["Impulso a Cuidadoras"] + \
                                vivienda_df["Programa de Inclusión para Personas con Discapacidad en condición de vulnerabilidad"] + \
                                vivienda_df["Sin programa"]

    vivienda_df = vivienda_df.astype(float)

    vivienda_df["Pobreza"] = programa_df_por_vivienda["TipoPobreza"]

    cols = vivienda_df.columns.tolist()
    cols = cols[-2:-1] + cols[:4] + cols[4:-2] +cols[-1:]

    vivienda_df = vivienda_df[cols]

    total_series = vivienda_df.sum()
    total_series.name = "Total"
    vivienda_df.append(total_series)

    return vivienda_df
    
@st.cache(allow_output_mutation=True)
def generate_housing_poverty_dataframe(vivienda_df):
    """Genera un dataframe con codificacion one-hot sobre
        el tipo de pobreza de las viviendas y su status.

        Params
        ------
        programa_df : pd.DataFrame
        un dataframe de pandas conteniendo toda la informacion 
        sobre los programas sociales
        
        Returns
        -------
        pobreza_vivienda_df : pd.DataFrame
            Un dataframe conteniendo la informacion sobre los
            tipos de pobreza de las viviendas con codificacion 
            one-hot.
        """
    
    pobreza_vivienda_df = vivienda_df.groupby("Pobreza").sum()
    pobreza_vivienda_df["Habitantes"]

    return pobreza_vivienda_df

def to_excel(df):
    """Genera un archivo excel de un dataframe.

        Params
        ------
        ddf : pd.DataFrame
        el dataframe de pandas que se desee convertir
        
        Returns
        -------
        processed_data
            un archivo de excel conteniendo la informacion
            del DataFrame procesado
        """
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data