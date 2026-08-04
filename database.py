import sqlite3
import os

DB_PATH = "data/clients.db"

os.makedirs("data", exist_ok=True)


def connect():
    conn = sqlite3.connect(
        DB_PATH,
        timeout=30,
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=30000;")

    return conn


def create_tables():
    with connect() as conn:
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
            education TEXT,
            marital_status TEXT,
            address TEXT,
            notes TEXT,
            photo TEXT,
            added_by INTEGER,
            added_by_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cur.execute("PRAGMA table_info(clients)")
        columns = [row[1] for row in cur.fetchall()]

        if "education" not in columns:
            cur.execute(
                "ALTER TABLE clients ADD COLUMN education TEXT DEFAULT ''"
            )

        if "marital_status" not in columns:
            cur.execute(
                "ALTER TABLE clients ADD COLUMN marital_status TEXT DEFAULT ''"
            )

        conn.commit()


def add_client(
    name,
    facebook,
    instagram,
    threads,
    age,
    profession,
    education,
    marital_status,
    address,
    notes,
    photo,
    added_by,
    added_by_name,
):
    with connect() as conn:
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO clients(
            name,
            facebook,
            instagram,
            threads,
            age,
            profession,
            education,
            marital_status,
            address,
            notes,
            photo,
            added_by,
            added_by_name
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name.strip(),
            facebook.strip(),
            instagram.strip(),
            threads.strip(),
            age.strip(),
            profession.strip(),
            education.strip(),
            marital_status.strip(),
            address.strip(),
            notes.strip(),
            photo,
            added_by,
            added_by_name,
        ))

        conn.commit()


def client_exists(facebook="", instagram="", threads=""):
    facebook = facebook.strip()
    instagram = instagram.strip()
    threads = threads.strip()

    conditions = []
    values = []

    if facebook:
        conditions.append("LOWER(TRIM(facebook)) = LOWER(TRIM(?))")
        values.append(facebook)

    if instagram:
        conditions.append("LOWER(TRIM(instagram)) = LOWER(TRIM(?))")
        values.append(instagram)

    if threads:
        conditions.append("LOWER(TRIM(threads)) = LOWER(TRIM(?))")
        values.append(threads)

    if not conditions:
        return None

    query = f"""
    SELECT *
    FROM clients
    WHERE {" OR ".join(conditions)}
    LIMIT 1
    """

    with connect() as conn:
        cur = conn.cursor()
        cur.execute(query, values)
        return cur.fetchone()


def get_client_by_username(username):
    username = username.strip()

    with connect() as conn:
        cur = conn.cursor()

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

        return cur.fetchone()


def search_client(keyword):
    keyword = keyword.strip().lower()

    with connect() as conn:
        cur = conn.cursor()

        cur.execute("""
        SELECT *
        FROM clients
        WHERE
            LOWER(name) LIKE ?
            OR LOWER(facebook) LIKE ?
            OR LOWER(instagram) LIKE ?
            OR LOWER(threads) LIKE ?
            OR LOWER(profession) LIKE ?
            OR LOWER(education) LIKE ?
            OR LOWER(marital_status) LIKE ?
            OR LOWER(address) LIKE ?
        ORDER BY id DESC
        LIMIT 1
        """, (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
        ))

        return cur.fetchone()


def get_total_clients():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM clients")
        return cur.fetchone()[0]