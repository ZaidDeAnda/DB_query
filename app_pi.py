import streamlit as st
import pandas as pd
from PIL import Image
from sqlalchemy import create_engine
import numpy as np

from utils.config import Config

config = Config()

image = Image.open('C:\\NL\\auxiliar\\sii.png')
col1, col2 = st.columns(2)
col1.title('Gobierno del Estado de Nuevo León')
col2.image(image, width=300)

st.write('#### Primera Infancia')


def log_in(user,password):
    user_dict = pd.read_csv(r'C:\NL\checs_primera_infancia\users.csv').set_index('user').to_dict()
    if (user in user_dict['pass'].keys()) and (user_dict['pass'][user] == password):
        return True,user_dict['role'][user]
    else:
        return False,'Usuario o Contraseña Incorrecta'

def home():

    st.markdown('### Bienvenido')

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

def primera_infancia():

    data = st.session_state.data.copy()

    st.sidebar.write('#### Filtrar')
    sexo = st.sidebar.selectbox('Sexo', ['Todos', 'Hombre', 'Mujer'])
    edad = st.sidebar.selectbox('Edad', ['Todas', 'Primera Infancia (0-5)', '6-29', '30-65', '+65'])
    mun = st.sidebar.selectbox('Municipio', ['Todos'] +  list(data['municipiodesc'].unique()))



    data['rango'] = pd.cut(data['edad'], [0, 6, 30, 65, 200], labels=['Primera Infancia (0-5)', '6-29', '30-65', '+65'])


    if sexo != 'Todos':
        data = data[data['P37_Sexo'] == sexo]

    if edad != 'Todas':
        data = data[data['rango'] == edad]

    if mun != 'Todos':
        data = data[data['municipiodesc'] == mun]




    table_data = data.groupby(['LeyendaCSIPS', 'EstatusBeneficiario']).count().reset_index().pivot(
        index='LeyendaCSIPS', columns='EstatusBeneficiario', values='IdBeneficiario1').fillna(0).astype(int)
    table_data['Total'] = table_data.sum(axis=1)
    st.table(table_data)

    csv = convert_df(data)

    st.download_button(
        label = 'Descargar',
        data=csv,
        file_name='primera_infancia.csv',)





# sidebar
image = Image.open('C:\\NL\\auxiliar\\leon.png')
st.sidebar.image(image, width=300)

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

            DATABASE_CONNECTION = f'mssql://{config.sql.USERNAME}:{config.sql.PASSWORD}@{config.sql.SERVER}/{config.sql.DATABASE}?driver={config.sql.DRIVER}'

            engine = create_engine(DATABASE_CONNECTION)
            connection = engine.connect()

            query = 'SELECT * FROM VW_PRIMERA_INFANCIA'


            st.session_state.data = pd.read_sql_query(query, connection)

        else:
            sb4.write(st.session_state.role)
except Exception as e:
    print(e)

# page

if 'auth' in st.session_state:

    page = sb1.selectbox('', ['Inicio', 'Primera infancia'], key=1)

    if st.session_state.auth and page == 'Inicio':
        home()

    if st.session_state.auth and page == 'Primera infancia':
        primera_infancia()



