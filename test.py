import pandas as pd
import os

SOURCE_DIR = 'source'
FILES = ['brands', 'categories', 'customers', 'orders', 'products', 'order_items', 
         'staffs', 'stocks', 'stores']

def analyze_csv():
    analysis_results = []

    for file in FILES:
        path = f"{SOURCE_DIR}/{file}.csv"
        if not os.path.exists(path):
            print(f"Файл {path} не найден, пропускаю...")
            continue
        
        df = pd.read_csv(path)
        print(f"\n--- Анализ таблицы: {file} ({df.shape[0]} строк) ---")
        
        for col in df.columns:
            null_count = df[col].isnull().sum()
            is_unique = df[col].is_unique
            dtype = df[col].dtype
            
            # Определяем примерный тип для SQL
            sql_type = "VARCHAR"
            if "int" in str(dtype):
                sql_type = "INTEGER"
            elif "float" in str(dtype):
                sql_type = "DECIMAL(10,2)"
            elif "date" in col.lower() or "time" in col.lower():
                sql_type = "DATE"

            print(f"Колонка: {col:20} | Тип: {str(dtype):10} | Уникальна: {str(is_unique):5} | Пустых: {null_count}")

if __name__ == "__main__":
    analyze_csv()