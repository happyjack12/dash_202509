CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    phone VARCHAR,
    email VARCHAR NOT NULL UNIQUE,
    street VARCHAR,
    city VARCHAR,
    state VARCHAR,
    zip_code INTEGER
);