import pandas as pd

import pymongo
import streamlit as st

from utils.dict_utils import change_user_dict
from utils.database import get_mongo_client, create_dataframe_from_cursor


def check_password(config):
    client = get_mongo_client(config)
    db = client.query_database
    users_collection = db.users
    users_cursor = users_collection.find({})
    users = create_dataframe_from_cursor(users_cursor)
    user_dict = change_user_dict(users.to_dict())
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (st.session_state["username"] in user_dict.keys()
                and st.session_state["password"]
                == user_dict[st.session_state["username"]]["password"]):
            st.runtime.legacy_caching.clear_cache()
            st.session_state["password_correct"] = True
            st.session_state["admin_role"] = user_dict[
                st.session_state["username"]]["role"]
            st.session_state["username"] = st.session_state["username"]
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    sb1 = st.sidebar.empty()
    sb2 = st.sidebar.empty()
    sb3 = st.sidebar.empty()

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        sb1.text_input("Correo", key="username")
        sb2.text_input("Contraseña",
                       type="password",
                       on_change=password_entered,
                       key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        sb1.text_input("Correo", key="username")
        sb2.text_input("Contraseña",
                       type="password",
                       on_change=password_entered,
                       key="password")
        sb3.error("😕 Usuario desconocido o contraseña errónea")
        return False
    else:
        # Password correct.
        sb3.success("Datos ingresados correctamente")
        return True


@st.cache
def get_user():
    return st.session_state["username"]
