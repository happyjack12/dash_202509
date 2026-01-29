CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY,
    category_name VARCHAR NOT NULL UNIQUE
);