import pandas as pd

from utils.database import get_mongo_client
from utils.config import Config

config = Config()

client = get_mongo_client(config)
db = client.query_database
user_collection = db.users

users = pd.read_csv("auxiliar/users.csv")

for row in users.iterrows():
    print(user_collection.insert_one(row[1].to_dict()).inserted_id)