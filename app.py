import streamlit as st
import pandas as pd
import pymssql
from PIL import Image

from utils.config import Config

def log_in(user,password):
    user_dict = pd.read_csv(r'C:\NL\visor\visor\auxiliar\users.csv').set_index('user').to_dict()
    if (user in user_dict['pass'].keys()) and (user_dict['pass'][user] == password):
        return True,user_dict['role'][user]
    else:
        return False,'Usuario o Contraseña Incorrecta'

def home():
    image = Image.open('C:\\NL\\auxiliar\\sii.png')
    col1, col2 = st.columns(2)
    col1.image(image, width=300)

# dashboard checs.py

def checs():

    ESTATUS = {1: 'Validando', 2: 'Validado', 3: 'Solicitud de Apoyo', 4: 'Beneficiado(a)',
               5: 'Cancelada', 6: 'Duplicado', 7: 'Rechazado', 8: 'Por solicitar',
               9: 'Fallecido (lista espera)', 10: 'Por beneficiar'}
    SEXO = {1: 'Hombre', 2: 'Mujer'}
    PROGRAMAS = {12: 'Hambre Cero',
                 13: 'Programa de Inclusión para Personas con Discapacidad en condición de vulnerabilidad',
                 5: 'Red de cuidados'}
    MUNICIPIOS = pd.read_json('auxiliar/muns.json').set_index('id_municipio')['nom_agem'].to_dict()

    # filter

    st.sidebar.write('#### Filtrar')
    sexo = st.sidebar.selectbox('Sexo',['Todos','Hombre','Mujer'])
    edad = st.sidebar.selectbox('Edad',['Todas','Primera Infancia (0-5)','6-29','30-65','+65'])
    mun = st.sidebar.selectbox('Municipio',['Todos']+list(MUNICIPIOS.values()))
    origen = st.sidebar.selectbox('Origen', ['Todos'] + ['Ruta','Sistema CHECS'])

    # data

    data = st.session_state.data.copy()
    data['Estatus'] = data['IDEstatusBeneficiario'].map(ESTATUS)
    data['Sexo'] = data['IDSexo'].map(SEXO)
    data['Programa'] = data['IDPrograma'].map(PROGRAMAS)
    data = data.dropna(subset=['Estatus'])
    data['rango'] = pd.cut(data['edad'], [0, 5, 30, 65, 200], labels=['Primera Infancia (0-5)', '6-29', '30-65', '+65'])
    data['Municipio'] = data['Municipio'].map(MUNICIPIOS)
    data['origen'] = data['IDProgramaOrigen'].apply(lambda x: 'Ruta' if x == 9 else 'Sistema CHECS')

    if sexo != 'Todos':
        data = data[data['Sexo']==sexo]
    if edad != 'Todas':
        data = data[data['rango']==edad]
    if mun != 'Todos':
        data = data[data['Municipio']==mun]
    if origen != 'Todos':
        data = data[data['origen']==origen]

    # display

    st.write('#### Estatus Sistema CHECS')

    table_data = data.groupby(['Programa', 'Estatus']).count().reset_index().pivot(
        index='Programa', columns='Estatus', values='IDBeneficiario').fillna(0).astype(int)
    table_data['Total'] = table_data.sum(axis=1)
    st.table(table_data)

    submit = st.empty()

    if submit ('Descargar'):
        table_data.to_excel('Datos.xlsx')



def carencia():

    ESTATUS = {1: 'Validando', 2: 'Validado', 3: 'Solicitud de Apoyo', 4: 'Beneficiado(a)',
               5: 'Cancelada', 6: 'Duplicado', 7: 'Rechazado', 8: 'Por solicitar',
               9: 'Fallecido (lista espera)', 10: 'Por beneficiar'}
    SEXO = {1: 'Hombre', 2: 'Mujer'}
    MUNICIPIOS = pd.read_json('auxiliar/muns.json').set_index('id_municipio')['nom_agem'].to_dict()

    # filter

    st.sidebar.write('#### Filtrar')
    sexo = st.sidebar.selectbox('Sexo',['Todos','Hombre','Mujer'])
    edad = st.sidebar.selectbox('Edad',['Todas','Primera Infancia (0-5)','6-29','30-65','+65'])
    mun = st.sidebar.selectbox('Municipio',['Todos']+list(MUNICIPIOS.values()))
    origen = st.sidebar.selectbox('Origen', ['Todos'] + ['Ruta','Sistema CHECS'])

    # data

    data = st.session_state.data.copy()
    data['Estatus'] = data['IDEstatusBeneficiario'].map(ESTATUS)
    data['Sexo'] = data['IDSexo'].map(SEXO)
    data = data.dropna(subset=['Estatus'])
    data['rango'] = pd.cut(data['edad'], [0, 5, 30, 65, 200], labels=['Primera Infancia (0-5)', '6-29', '30-65', '+65'])
    data['Municipio'] = data['Municipio'].map(MUNICIPIOS)
    data['origen'] = data['IDProgramaOrigen'].apply(lambda x: 'Ruta' if x == 9 else 'Sistema CHECS')
    data.loc[(data['TipoPobreza']=='Faltan datos') | (data['TipoPobreza'].isna()),'TipoPobreza'] = 'Indefinido'

    if sexo != 'Todos':
        data = data[data['Sexo']==sexo]
    if edad != 'Todas':
        data = data[data['rango']==edad]
    if mun != 'Todos':
        data = data[data['Municipio']==mun]
    if origen != 'Todos':
        data = data[data['origen']==origen]

    # display

    st.write('#### Algoritmo de Pobreza Sistema CHECS')

    table_data = data.groupby(['TipoPobreza', 'Estatus']).count().reset_index().pivot(
        index='TipoPobreza', columns='Estatus', values='IDBeneficiario').fillna(0).astype(int)
    table_data['Total'] = table_data.sum(axis=1)
    st.table(table_data)

    if submit ('Descargar'):
        table_data.to_excel('Datos.xlsx')


# sidebar



sb1 = st.sidebar.empty()
sb2 = st.sidebar.empty()
sb3 = st.sidebar.empty()
sb4 = st.sidebar.empty()

try:
    if st.session_state.auth:
        pass

except:
    user = sb1.text_input('Usuario')
    password = sb2.text_input('Contraseña',type='password')
    log = sb3.button('Ingresar')

try:
    if log:
        st.session_state.auth, st.session_state.role = log_in(user,password)

        if st.session_state.auth:
            sb1.empty()
            sb2.empty()
            sb3.empty()

            config = Config()
            conn = pymssql.connect(**config)
            query = 'select * from visor_sii'

            st.session_state.data = pd.read_sql(query, conn)

        else:
            sb4.write(st.session_state.role)
except:
    pass

# page

if 'auth' in st.session_state:

    page = sb1.selectbox('', ['Inicio', 'CHECS', 'Carencia'],key=1)

    if st.session_state.auth and page == 'Inicio':
        home()

    if st.session_state.auth and page == 'CHECS':
        checs()

    if st.session_state.auth and page == 'Carencia':
        carencia()

