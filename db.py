import duckdb
import pandas as pd

DB = 'my.db'


def read_query_file(query_name: str) -> str:
    with open(f"./queries/{query_name}.sql", encoding='utf-8') as f:
        query = f.read()
    
    return query


def fetch_data(query: str) -> pd.DataFrame:
    with duckdb.connect(DB) as duck:
        df = duck.query(query).to_df()

    return df


def get_data(query_name: str) -> pd.DataFrame:
    query = read_query_file(query_name)
    df = fetch_data(query)

    return df


