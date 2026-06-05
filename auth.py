from database import conn, cursor


def register_user(username, email, password):

    cursor.execute(
        """
        INSERT INTO users(username,email,password)
        VALUES(?,?,?)
        """,
        (username, email, password)
    )

    conn.commit()


def login_user(email, password):

    cursor.execute(
        """
        SELECT * FROM users
        WHERE email=? AND password=?
        """,
        (email, password)
    )

    return cursor.fetchone()