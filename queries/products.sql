CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR NOT NULL,
    brand_id INTEGER,
    category_id INTEGER,
    model_year INTEGER,
    list_price DECIMAL(10, 2) NOT NULL
);