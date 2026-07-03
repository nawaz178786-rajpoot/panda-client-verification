import sqlite3
import os

DB_PATH = "data/clients.db"

os.makedirs("data", exist_ok=True)


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


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
    INSERT INTO clients (
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
        name.strip(),
        facebook.strip(),
        instagram.strip(),
        threads.strip(),
        age.strip(),
        profession.strip(),
        address.strip(),
        notes.strip(),
        photo,
        added_by,
        added_by_name,
    ))

    conn.commit()
    conn.close()


def client_exists(facebook="", instagram="", threads=""):
    conn = connect()
    cur = conn.cursor()

    conditions = []
    values = []

    facebook = facebook.strip()
    instagram = instagram.strip()
    threads = threads.strip()

    if facebook:
        conditions.append("LOWER(TRIM(facebook)) = LOWER(TRIM(?))")
        values.append(facebook)

    if instagram:
        conditions.append("LOWER(TRIM(instagram)) = LOWER(TRIM(?))")
        values.append(instagram)

    if threads:
        conditions.append("LOWER(TRIM(threads)) = LOWER(TRIM(?))")
        values.append(threads)

    # No username entered
    if not conditions:
        conn.close()
        return None

    query = f"""
    SELECT *
    FROM clients
    WHERE {" OR ".join(conditions)}
    LIMIT 1
    """

    cur.execute(query, values)

    row = cur.fetchone()

    conn.close()

    return row


def get_client_by_username(username):
    conn = connect()
    cur = conn.cursor()

    username = username.strip()

    cur.execute("""
    SELECT *
    FROM clients
    WHERE
        LOWER(TRIM(facebook)) = LOWER(TRIM(?))
        OR LOWER(TRIM(instagram)) = LOWER(TRIM(?))
        OR LOWER(TRIM(threads)) = LOWER(TRIM(?))
    LIMIT 1
    """, (
        username,
        username,
        username,
    ))

    row = cur.fetchone()

    conn.close()

    return row


def search_client(keyword):
    conn = connect()
    cur = conn.cursor()

    keyword = keyword.strip().lower()

    cur.execute("""
    SELECT *
    FROM clients
    WHERE
        LOWER(name) LIKE ?
        OR LOWER(facebook) LIKE ?
        OR LOWER(instagram) LIKE ?
        OR LOWER(threads) LIKE ?
    ORDER BY id DESC
    LIMIT 1
    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%",
    ))

    row = cur.fetchone()

    conn.close()

    return row


def get_total_clients():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM clients")

    total = cur.fetchone()[0]

    conn.close()

    return total