CREATE DATABASE myshop;
USE myshop;

CREATE TABLE IF NOT EXISTS customer(
    u_id TEXT PRIMARY KEY,
    u_name TEXT NOT NULL,
    u_pw TEXT NOT NULL,
    gender TEXT,
    birthday TEXT,
    u_email TEXT,
    u_tel TEXT,
    u_live TEXT,
    SNS Boolean);

