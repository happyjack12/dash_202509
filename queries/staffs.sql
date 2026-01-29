CREATE TABLE IF NOT EXISTS staffs (
    staff_id INTEGER PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR NOT NULL UNIQUE,
    phone VARCHAR,
    active INTEGER NOT NULL,
    store_id INTEGER,
    manager_id INTEGER 
);