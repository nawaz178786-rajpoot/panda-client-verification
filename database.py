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
        notes TEXT,
        photo TEXT,
        added_by INTEGER,
        added_by_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def add_client(
    name,
    facebook,
    instagram,
    threads,
    age,
    profession,
    address,
    notes,
    photo,
    added_by,
    added_by_name,
):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO clients
    (
        name,
        facebook,
        instagram,
        threads,
        age,
        profession,
        address,
        notes,
        photo,
        added_by,
        added_by_name
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        facebook,
        instagram,
        threads,
        age,
        profession,
        address,
        notes,
        photo,
        added_by,
        added_by_name,
    ))

    conn.commit()
    conn.close()


def client_exists(facebook="", instagram="", threads=""):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM clients
    WHERE
        facebook = ?
        OR instagram = ?
        OR threads = ?
    """, (
        facebook,
        instagram,
        threads,
    ))

    row = cur.fetchone()

    conn.close()

    return row