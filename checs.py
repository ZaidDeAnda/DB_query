import pymssql
import pandas as pd
import streamlit as st

from utils.config import Config

config = Config()

conn = pymssql.connect(**config)
query = 'select * from X' # ricardo nos debe ayudar a crear una vista en el servidor 108 con los beneficiarios de primera infancia del servidor 112

data = pd.read_sql(query, conn)