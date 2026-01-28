import plotly.express as px
import streamlit as st
import pandas as pd

from db import get_data

st.set_page_config(layout='wide')


customers = get_data('customers')


min_date, max_date = customers['date_first_purchase'].agg(['min', 'max'])
occupation_options = customers['occupation'].sort_values().unique()


st.title("Dashboard on Customers data")

with st.sidebar:
    dates_selected = st.date_input(
        label="Select period",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )

    occupations_selected = st.multiselect(
        label="Select occupation",
        options=occupation_options,
        default=occupation_options
    )


if len(dates_selected) == 2:
    period_filter = f"date_first_purchase.between('{min_date}', '{max_date}')"
else:
    period_filter = f"date_first_purchase <= '{min_date}'" 

occupations_filter = f"occupation.isin({occupations_selected})"

composite_filter = f"{period_filter} and {occupations_filter}"


customers_filtered = customers.query(composite_filter)


if customers_filtered.shape[0] != 0:
    customers_count = customers_filtered['customer_key'].unique()[0]
    avg_yearly_income = customers_filtered['yearly_income'].mean()

    col1, col2 = st.columns(2)

    col1.metric(
        label="Number of customers",
        value=customers_count
    )

    col2.metric(
        label='Avg yearly income',
        value=int(round(avg_yearly_income, 0))
    )





hist_fig = px.histogram(
    data_frame=customers_filtered,
    x='yearly_income',
    facet_row='gender',
    color='gender',
    color_discrete_map={'Female': 'pink', 'Male': 'blue'},
    title='Yearly Income Distribution by gender'
)


st.plotly_chart(hist_fig)


col1, col2 = st.columns(2)
pie_fig = px.pie(
    data_frame=customers_filtered,
    values='customer_key',
    names='marital_status',
    hole=.5
)

col1.plotly_chart(pie_fig)


pie_fig2 = px.pie(
    data_frame=customers_filtered,
    values='customer_key',
    names='gender',
    color='gender',
    color_discrete_map={'Female': 'pink', 'Male': 'blue'}
)

col2.plotly_chart(pie_fig2)

st.dataframe(customers, hide_index=True)
