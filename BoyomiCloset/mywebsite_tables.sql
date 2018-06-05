DROP TABLE IF EXISTS tbuser;
DROP TABLE IF EXISTS tbboard;

CREATE TABLE IF NOT EXISTS tbuser(
    u_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    pw TEXT NOT NULL,
    u_name TEXT NOT NULL,
    gender TEXT NULL
);