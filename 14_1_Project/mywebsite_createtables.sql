-- mywebsite
DROP TABLE IF EXISTS tbuser;
DROP TABLE IF EXISTS tbboard;
CREATE TABLE IF NOT EXISTS tbuser (
    u_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE, 
    password TEXT NOT NULL,
    u_name TEXT NOT NULL,
    gender TEXT NULL,
    birth_year INT NULL,
    add_dt DATETIME DEFAULT (DATETIME('now', 'localtime')), 
    upd_dt DATETIME DEFAULT (DATETIME('now', 'localtime')),
    use_flag TEXT DEFAULT ('Y')
);
CREATE TABLE IF NOT EXISTS tbboard (
    b_id INTEGER PRIMARY KEY AUTOINCREMENT,
    u_id INTEGER NOT NULL,
    title TEXT NOT NULL, 
    content TEXT NOT NULL, 
    add_dt DATETIME DEFAULT (DATETIME('now', 'localtime')), 
    upd_dt DATETIME DEFAULT (DATETIME('now', 'localtime')),
    use_flag TEXT DEFAULT ('Y')
);