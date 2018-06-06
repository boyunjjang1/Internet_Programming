DROP TABLE IF EXISTS tbuser;
DROP TABLE IF EXISTS tbboard;

CREATE TABLE IF NOT EXISTS tbuser(
    u_id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_id TEXT NOT NULL UNIQUE,
    email TEXT NULL UNIQUE,
    pw TEXT NOT NULL,
    u_name TEXT NOT NULL,
    gender TEXT NULL,
    birth TEXT NULL,
    u_tel INTEGER NULL,
    u_live TEXT NULL,
    sns_inform TEXT NULL,
    add_at DATETIME DEFAULT (DATETIME('now', 'localtime'))
    upd_at DATETIME DEFAULT (DATETIME('now', 'localtime'))
    use_flag TEXT DEFAULT('Y')
);