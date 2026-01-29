CREATE TABLE IF NOT EXISTS stores (
    store_id INTEGER PRIMARY KEY,
    store_name VARCHAR NOT NULL,
    phone VARCHAR,
    email VARCHAR,
    street VARCHAR,
    city VARCHAR,
    state VARCHAR,
    zip_code INTEGER
);