import duckdb
import pandas as pd

# Путь к локальной базе данных DuckDB
DB = 'my.db'

def read_query_file(query_name: str) -> str:
    """
    Читает SQL-запрос из файла в папке queries.
    
    Args:
        query_name (str): Название файла без расширения .sql
    Returns:
        str: Содержимое SQL-файла
    """
    with open(f"./queries/{query_name}.sql", encoding='utf-8') as f:
        query = f.read()
    return query

def fetch_data(query: str) -> pd.DataFrame:
    """
    Выполняет SQL-запрос в базе DuckDB и возвращает результат в виде Pandas DataFrame.
    
    Args:
        query (str): SQL-запрос для выполнения
    Returns:
        pd.DataFrame: Данные результата запроса
    """
    with duckdb.connect(DB) as duck:
        df = duck.query(query).to_df()
    return df

def get_data(query_name: str) -> pd.DataFrame:
    """
    Комплексная функция: читает файл запроса и сразу возвращает датафрейм.
    
    Args:
        query_name (str): Имя sql-файла в папке queries
    """
    query = read_query_file(query_name)
    df = fetch_data(query)
    return df