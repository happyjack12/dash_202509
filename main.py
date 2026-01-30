import streamlit as st
import plotly.express as px
import pandas as pd
from db import get_data # Импорт функции для работы с БД

# Конфигурация интерфейса
st.set_page_config(page_title="Bike Store Analytics", layout="wide")

st.title("Аналитика магазина велосипедов")

# Загрузка данных (согласно требованиям, через SQL запросы/вьюшки)
sales_df = get_data('sales_analytics')
history_df = get_data('customer_dynamics')

# --- БОКОВАЯ ПАНЕЛЬ (ФИЛЬТРЫ) ---
st.sidebar.header("Настройка фильтров")

# Получение списка уникальных брендов (исключая пустые значения)
available_brands = [b for b in sales_df['brand_name'].unique().tolist() if pd.notnull(b)]

selected_brands = st.sidebar.multiselect(
    "Выберите бренды:", 
    options=available_brands, 
    default=available_brands
)

# Определение максимального порога для слайдера выручки
high_score = sales_df['revenue'].max()
limit_val = int(high_score) if pd.notnull(high_score) else 0

threshold = st.sidebar.slider(
    "Минимальный порог выручки:", 
    0, 
    max(limit_val, 1), 
    0
)

# Фильтрация данных на основе выбора пользователя
mask = (sales_df['brand_name'].isin(selected_brands)) & (sales_df['revenue'] >= threshold)
filtered_data = sales_df[mask]

# --- ВИЗУАЛИЗАЦИЯ ---
left_row, right_row = st.columns(2)

with left_row:
    # 1. Столбчатая диаграмма распределения выручки
    st.plotly_chart(
        px.bar(filtered_data, x='category_name', y='revenue', color='brand_name', 
               title="Выручка по категориям и брендам"),
        use_container_width=True
    )

    # 2. Линейный график накопительного итога
    st.plotly_chart(
        px.line(history_df, x='month', y='running_total', 
                title="Динамика продаж (накопительный итог)"),
        use_container_width=True
    )

with right_row:
    # 3. Круговая диаграмма доли рынка брендов в штуках
    st.plotly_chart(
        px.pie(filtered_data, values='total_qty', names='brand_name', 
               title="Доля продаж в количественном выражении"),
        use_container_width=True
    )

    # 4. Диаграмма рассеяния (Scatter plot) для поиска корреляций
    st.plotly_chart(
        px.scatter(filtered_data, x='total_qty', y='revenue', 
                   hover_name='product_name_up', title="Связь объема продаж и выручки"),
        use_container_width=True
    )