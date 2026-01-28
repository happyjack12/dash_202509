import json
import pandas as pd
import duckdb

DB = 'my.db'
SOURCE = 'source/adventure_works.xlsx'

# важно сохранять порядок листов так как сначала идут таблицы без внешних ключей
SHEETS = ['Customers', 'Territory', 'ProductCategory', 
          'ProductSubCategory', 'Products', 'Sales']

with open('dicts/columns.json') as f:
    columns_dict = json.load(f)


def make_snake_case(camel_cased_word: str) -> str:
    """
    Преобразовывает текст в snake_case
    
    Принимает:
    * camel_cased_word: текстовая строка в формате camel_case
    Возвращает:
    * snake_case_word: текстовую строку в формате snake_case
    """
    snake_cased_word = ''
    for ix, sym in enumerate(camel_cased_word):
        if sym.isupper() and ix != 0:
            snake_cased_word += f"_{sym.lower()}"
        else:
            snake_cased_word += sym.lower().replace(' ', '')
    
    if snake_cased_word == 'group':
        snake_cased_word = 'continent'

    return snake_cased_word


def read_data(sheet_name: str) -> pd.DataFrame:
    print(f"reading data from {sheet_name}...")
    df = pd.read_excel(
        SOURCE, 
        sheet_name=sheet_name,
    ).dropna(thresh=3)

    df.rename(
        columns={col: make_snake_case(col) for col in df.columns}, 
        inplace=True
    )

    return df


def create_table(table_name: str) -> None:
    ddl_file = f"ddl/{table_name}_ddl.sql"

    with open(ddl_file) as f:
        ddl_query = f.read()

    with duckdb.connect(DB) as duck:
        print(f"creating table {table_name}...")
        duck.execute(ddl_query)
        duck.commit()

    with duckdb.connect(DB) as duck:
        duck.execute(f"truncate table {table_name}")
        duck.commit()


def load_data(df: pd.DataFrame, table_name: str) -> None:
    print(f"{table_name}: {df.shape}")
    with duckdb.connect(DB) as duck:
        print(f"loading data to {table_name}...")
        duck.execute(f"""
            insert into {table_name}
            select *
            from df
        """)


def pipeline() -> None:
    
    for sheet_name in SHEETS:
        df = read_data(sheet_name)
        
        table_name = make_snake_case(sheet_name)
        usecols = columns_dict[table_name]

        create_table(table_name)
        load_data(df[usecols], table_name)

