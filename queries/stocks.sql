CREATE TABLE IF NOT EXISTS stocks (
    store_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    PRIMARY KEY (store_id, product_id)
);