# supabase_client.py

import os
import logging

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("watchfiles").setLevel(logging.WARNING)
import supabase


def supabase_client():
    # setup supabase
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    client = supabase.Client(supabase_url, supabase_key)
    return client
