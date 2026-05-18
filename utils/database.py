import pandas as pd
import pymongo
import urllib
import streamlit as st

@st.cache(allow_output_mutation=True)
def get_mongo_client(config):
    """Get the mongo client and store it in cache.

        Params
        ------
        config : Config
            Configuration object containing email details.
        
        Returns
        -------
        client
            The mongo client connected to the database.
        """
    db_mongo = config.get_config()['db_mongo']
    user = db_mongo["user"]
    password = urllib.parse.quote_plus(db_mongo["password"])
    cluster = db_mongo["cluster"]
    client = pymongo.MongoClient(
        f"mongodb+srv://{user}:{password}@{cluster}/?retryWrites=true&w=majority"
    )
    return client

def create_dataframe_from_cursor(cursor):
    """Transform the cursor from mongo into a dataframe

        Params
        ------
        cursor : cursor
            Cursor pointing to a mongo collection.
        
        Returns
        -------
        df
            The dataframe made from the mongo cursor.
        """
    df = None
    for document in cursor:
        if df is not None:
            df = df.append(document, ignore_index=True)
        else:
            df = pd.DataFrame(document, index=[0])
    df.drop("_id", axis=1, inplace=True)
    return df


def prepare_data_dict(data_dict):
    """Change the form data dictionary into a better use format.

        Params
        ------
        data_dict : dict
            Dict containing the new ticket info.
        
        Returns
        -------
        data
            A dictionary containing the new ticket info with a better format for emailing.
        """
    data = {
        'ticket_id': data_dict['ID'],
        'ticket_type': data_dict['error'],
        'ticket_datetime': data_dict['fecha'],
        'ticket_requester': data_dict['autor'],
        'ticket_attached': [],
        'ticket_info': data_dict['comentarios'],
        'ticket_status': data_dict['status'],
        'ticket_area' : data_dict['direccion'],
        'ticket_solicitant' : data_dict['solicitante']
    }
    return data
