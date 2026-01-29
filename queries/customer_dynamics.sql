SELECT 
    strftime('%Y-%m', order_date) as month, -- Работа с датами
    SUM(revenue) as monthly_revenue,
    SUM(SUM(revenue)) OVER (ORDER BY strftime('%Y-%m', order_date)) as running_total -- Оконная функция
FROM (
    SELECT o.order_date, (oi.list_price * oi.quantity) as revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
) sub -- Подзапрос
GROUP BY 1;