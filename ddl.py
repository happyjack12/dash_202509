import json
import pandas as pd
import duckdb

DB = 'my.db'

# Список таблиц в порядке их зависимости (сначала справочники, потом таблицы с FK)
TABLES = ['brands', 'categories', 'customers', 'stores', 
          'staffs', 'products', 'orders', 'order_items', 'stocks']

# Загрузка словаря соответствия колонок из JSON
with open('queries/columns.json') as f:
    columns_dict = json.load(f)

def make_snake_case(camel_cased_word: str) -> str:
    """
    Преобразовывает строку из CamelCase или с пробелами в snake_case.
    
    Args:
        camel_cased_word (str): Исходная строка
    Returns:
        str: Строка в формате snake_case
    """
    snake_cased_word = ''
    for ix, sym in enumerate(camel_cased_word):
        if sym.isupper() and ix != 0:
            snake_cased_word += f"_{sym.lower()}"
        else:
            snake_cased_word += sym.lower().replace(' ', '')
    
    # Обработка исключения для зарезервированного слова 'group'
    if snake_cased_word == 'group':
        snake_cased_word = 'continent'

    return snake_cased_word

def read_data(query_name: str) -> pd.DataFrame:
    """
    Читает CSV файл, очищает его от пустых строк и приводит заголовки к snake_case.
    """
    print(f"reading data from {query_name}...")
    df = pd.read_csv(f"source/{query_name}.csv")

    # Удаление полностью пустых строк
    df = df.dropna(how='all')

    # Массовое переименование колонок
    df.rename(
        columns={col: make_snake_case(col) for col in df.columns}, 
        inplace=True
    )
    return df

def create_table(table_name: str) -> None:
    """
    Выполняет DDL скрипт для создания таблицы и очищает её (truncate).
    """
    ddl_file = f"queries/{table_name}.sql"

    with open(ddl_file) as f:
        ddl_query = f.read()

    with duckdb.connect(DB) as duck:
        print(f"creating table {table_name}...")
        duck.execute(ddl_query)
        # Очистка таблицы перед новой загрузкой
        duck.execute(f"truncate table {table_name}")
        duck.commit()

def load_data(df: pd.DataFrame, table_name: str) -> None:
    """
    Загружает Pandas DataFrame в таблицу DuckDB через промежуточную регистрацию.
    """
    print(f"Подготовка к загрузке {table_name}: {df.shape} строк")
    
    with duckdb.connect(DB) as duck:
        # Регистрация DF как временной таблицы внутри сессии DuckDB
        duck.register('tmp_df', df)
        
        print(f"Загрузка данных в {table_name}...")
        duck.execute(f"INSERT INTO {table_name} SELECT * FROM tmp_df")
        
        # Валидация: вывод количества успешно загруженных строк
        count = duck.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]
        print(f"Готово. В таблице {table_name} теперь {count} строк.")

def pipeline() -> None:
    """
    Основной процесс ETL: чтение файлов -> создание таблиц -> загрузка данных.
    """
    for sheet_name in TABLES:
        df = read_data(sheet_name)
        
        table_name = make_snake_case(sheet_name)
        # Выбираем только те колонки, которые описаны в конфигурации JSON
        usecols = columns_dict[table_name]

        create_table(table_name)
        load_data(df[usecols], table_name)

if __name__ == "__main__":
    pipeline()