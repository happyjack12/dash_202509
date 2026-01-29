import streamlit as st
import plotly.express as px
import pandas as pd
from db import get_data

st.set_page_config(page_title="Bike Store Analytics", layout="wide")

st.title("Аналитика магазина")

sales_df = get_data('sales_analytics')
history_df = get_data('customer_dynamics')

st.write(f"Отладочная инфа: в таблице {len(sales_df)} строк")

st.sidebar.header("Настройка фильтров")

available_brands = [b for b in sales_df['brand_name'].unique().tolist() if pd.notnull(b)]

selected_brands = st.sidebar.multiselect(
    "Бренды:", 
    options=available_brands, 
    default=available_brands
)

high_score = sales_df['revenue'].max()
limit_val = int(high_score) if pd.notnull(high_score) else 0

threshold = st.sidebar.slider(
    "Порог выручки:", 
    0, 
    max(limit_val, 1), 
    0
)

mask = (sales_df['brand_name'].isin(selected_brands)) & (sales_df['revenue'] >= threshold)
filtered_data = sales_df[mask]

left_row, right_row = st.columns(2)

with left_row:
    # График по категориям
    st.plotly_chart(
        px.bar(filtered_data, x='category_name', y='revenue', color='brand_name', title="Выручка по категориям"),
        width="stretch"
    )

    # Накопительный итог
    st.plotly_chart(
        px.line(history_df, x='month', y='running_total', title="Общая динамика продаж"),
        width="stretch"
    )

with right_row:
    # Продажи в штуках
    st.plotly_chart(
        px.pie(filtered_data, values='total_qty', names='brand_name', title="Распределение по брендам"),
        width="stretch"
    )

    # Зависимость выручки от объема
    st.plotly_chart(
        px.scatter(filtered_data, x='total_qty', y='revenue', hover_name='product_name_up', title="Объем vs Доход"),
        width="stretch"
    )