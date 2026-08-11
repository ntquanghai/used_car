import os
from supabase import create_client, Client, ClientOptions
from dotenv import load_dotenv
import pandas as pd
import supabase
import lmstudio as lms

load_dotenv()

url: str = os.getenv("SPBASE_DB_URL")
public_key: str = os.getenv("SPBASE_PUBLIC_KEY")
secret_key: str = os.getenv("SPBASE_SECRET_KEY")

def get_supabase_client() -> Client:
    """
    Returns a Supabase client instance for interacting with the Supabase database.
    """

    supabase: Client = create_client(
        url, 
        secret_key,
        options = ClientOptions(
            postgrest_client_timeout=30,
            storage_client_timeout=30,
            schema="public",    
        )
    )
    if (supabase is None):
        raise ValueError("Supabase client could not be created. Please check again.")

    return supabase

def get_table(client, table_name, batch_size: int = 1000) -> pd.DataFrame:
    """
    Returns a pandas DataFrame of the retrieve table
    """
    all_rows = []
    index = 0 
    print(f"Retrieving data from table: {table_name} in batches of {batch_size}...")

    while True:
        index_end = index + batch_size - 1
        response = (
            client.table(table_name).select("*").range(index, index_end).execute()
        )
        response_data = response.data
        if not response_data:
            break
        else:
            all_rows.extend(response_data)
            index += batch_size

    return pd.DataFrame(all_rows)

def connect_to_lm_studio(prompt: str):
    #model_name = os.getenv("LM_STUDIO_MODEL_NAME")
    model_name = "qwen/qwen3-4b-2507"

    if model_name is None:
        raise ValueError("LM_STUDIO_MODEL_NAME is not set.")

    model = lms.llm(model_name)
    response = model.respond(prompt)

    return(response)