def client_exists(facebook="", instagram="", threads=""):
    conn = connect()
    cur = conn.cursor()

    conditions = []
    values = []

    if facebook.strip():
        conditions.append("LOWER(TRIM(facebook)) = LOWER(TRIM(?))")
        values.append(facebook)

    if instagram.strip():
        conditions.append("LOWER(TRIM(instagram)) = LOWER(TRIM(?))")
        values.append(instagram)

    if threads.strip():
        conditions.append("LOWER(TRIM(threads)) = LOWER(TRIM(?))")
        values.append(threads)

    # Nothing entered
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