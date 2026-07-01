import sqlite3
import os

DB_PATH = "data/clients.db"

os.makedirs("data", exist_ok=True)


def connect():
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        facebook TEXT,
        instagram TEXT,
        threads TEXT,
        age TEXT,
        profession TEXT,
        address TEXT,
        photo TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def add_client(name, facebook, instagram, threads, age, profession, address, photo):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO clients
    (name, facebook, instagram, threads, age, profession, address, photo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        facebook,
        instagram,
        threads,
        age,
        profession,
        address,
        photo
    ))

    conn.commit()
    conn.close()


def client_exists(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM clients
    WHERE facebook=?
       OR instagram=?
       OR threads=?
    """, (
        username,
        username,
        username
    ))

    row = cur.fetchone()

    conn.close()

    return row