DROP TABLE IF EXISTS tbuser;
DROP TABLE IF EXISTS tbboard;
DROP TABLE IF EXISTS comment;

CREATE TABLE IF NOT EXISTS tbuser(
    u_id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_id TEXT NOT NULL UNIQUE,
    email TEXT NULL,
    pw TEXT NOT NULL,
    u_name TEXT NOT NULL,
    gender TEXT NULL,
    birth TEXT NULL,
    u_tel INTEGER NULL,
    u_live TEXT NULL,
    sns_inform TEXT NULL,
    add_at DATETIME DEFAULT (DATETIME('now', 'localtime')),
    upd_at DATETIME DEFAULT (DATETIME('now', 'localtime')),
    use_flag TEXT DEFAULT('Y')
);



-- INSERT INTO tbuser (input_id, pw, u_name) VALUES ('godboyun', 'boyunjjang1', 'Admin');

CREATE TABLE IF NOT EXISTS tbproduct(
    p_id INTEGER PRIMARY KEY AUTOINCREMENT,
    p_name TEXT NOT NULL UNIQUE,
    price INTEGER DEFAULT 0,
    img_path TEXT NOT NULL UNIQUE,
    kind TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS tbboard(
    b_id INTEGER PRIMARY KEY AUTOINCREMENT,
    u_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    add_at DATETIME DEFAULT (DATETIME('now', 'localtime')),
    upd_at DATETIME DEFAULT (DATETIME('now', 'localtime')),
    visit INTEGER DEFAULT 0,
    use_flag TEXT DEFAULT('Y')
);

CREATE TABLE IF NOT EXISTS comment(
    cmt INTEGER PRIMARY KEY AUTOINCREMENT,
    b_id INTEGER NOT NULL,
    u_name TEXT NOT NULL,
    naeyong TEXT NOT NULL,
    add_at DATETIME DEFAULT (DATETIME('now', 'localtime')),
    upd_at DATETIME DEFAULT (DATETIME('now', 'localtime'))
);


-- 자료형은 바뀐다

INSERT OR REPLACE INTO tbuser (input_id, email, pw, u_name) VALUES ('1', 'admin@example.com', 'admin', '관리자');
INSERT OR REPLACE INTO tbuser (input_id, email, pw, u_name) VALUES ('2', 'user@example.com', 'user', '사용자');
INSERT INTO tbuser (input_id, email, pw, u_name) VALUES ('admin', 'boyunjjang1@naver.com', 'boyun1004', '운영자');
INSERT INTO tbboard (u_id, title, content) VALUES (1, '공지사항입니다.', '공지내용 볼 꺼 뭐 있나요.');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 01_01_과목소개', '강의자료 01_01_과목소개');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 01_02_HTML5', '강의자료 01_02_HTML5');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 02_01_HTML5 2', '강의자료 02_01_HTML5 2');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 02_02_HTML5 3', '강의자료 02_02_HTML5 3');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 03_02_Github', '강의자료 03_02_Github');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 04_01_CSS', '강의자료 04_01_CSS');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 04_02_CSS 2', '강의자료 04_02_CSS 2');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 05_01_BS4', '강의자료 05_01_BS4');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 05_02_JS', '강의자료 05_02_JS');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 06_01_JS 2', '강의자료 06_01_JS 2');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 06_02_JS 3', '강의자료 06_02_JS 3');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 07_01_JS 4', '강의자료 07_01_JS 4');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 07_02_jQuery', '강의자료 07_02_jQuery');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 08_02_jQuery 2', '강의자료 08_02_jQuery 2');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 09_01_Python_Flask', '강의자료 09_01_Python_Flask');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 09_02_Python', '강의자료 09_02_Python');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 10_01_Python 2', '강의자료 10_01_Python 2');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 10_02_Python 3', '강의자료 10_02_Python 3');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 11_01_AJAX', '강의자료 11_01_AJAX');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 11_02_SQLite&SQL', '강의자료 11_02_SQLite&SQL');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 12_02_Python_Flask', '강의자료 12_02_Python_Flask');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 13_01_Python_Flask 2', '강의자료 13_01_Python_Flask 2');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 14_01_Website_project', '강의자료 14_01_Website_project');
INSERT INTO tbboard (u_id, title, content) VALUES (2, '강의자료 14_01_Website_project 2', '강의자료 14_01_Website_project 2');

