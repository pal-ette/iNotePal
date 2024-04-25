# supabase_client.py

import logging
import streamlit as st

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("watchfiles").setLevel(logging.WARNING)
import supabase


def supabase_client():
    # setup supabase
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
    client = supabase.Client(supabase_url, supabase_key)
    return client
