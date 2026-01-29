SELECT 
    c.category_name,
    b.brand_name,
    UPPER(p.product_name) as product_name_up,
    SUM(oi.quantity) as total_qty,
    ROUND(SUM(oi.list_price * oi.quantity * (1 - oi.discount)), 2) as revenue
FROM order_items oi
LEFT JOIN products p ON oi.product_id = p.product_id
LEFT JOIN categories c ON p.category_id = c.category_id
LEFT JOIN brands b ON p.brand_id = b.brand_id
GROUP BY 1, 2, 3
HAVING revenue > 0
ORDER BY revenue DESC;