CREATE TABLE IF NOT EXISTS order_items (
    order_id INTEGER,
    item_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    list_price DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(4, 2) DEFAULT 0,
    PRIMARY KEY (order_id, item_id)
);