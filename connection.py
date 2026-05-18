from sqlalchemy import create_engine
import pandas as pd

from utils.config import Config

config = Config.get_config()

DATABASE_CONNECTION = f'mssql://{config.sql.USERNAME}:{config.sql.PASSWORD}@{config.sql.SERVER}/{config.sql.DATABASE}?driver={config.sql.DRIVER}'

engine = create_engine(DATABASE_CONNECTION)
connection = engine.connect()

query = 'SELECT * FROM VW_PRIMERA_INFANCIA'

data = pd.read_sql_query(query,connection)
print(data)
mun = data['municipiodesc'].unique()
#mun.append('todos')


print(mun)