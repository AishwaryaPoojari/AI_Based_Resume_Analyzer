import sqlite3
import hashlib

DB_NAME = "resume_analyzer.db"


def get_conn():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        name      TEXT    NOT NULL,
        email     TEXT    UNIQUE NOT NULL,
        password  TEXT    NOT NULL,
        age       INTEGER,
        department TEXT,
        experience TEXT,
        occupation TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        email    TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Seed default admin if not exists
    from config import ADMIN_EMAIL, ADMIN_PASSWORD

    hashed = hash_password(ADMIN_PASSWORD)
    cursor.execute(
        "INSERT OR IGNORE INTO admins(email,password) VALUES(?,?)",
        (ADMIN_EMAIL, hashed)
    )

    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ── User auth ──────────────────────────────────────────────

def register_user(name, email, password, age, department, experience, occupation):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO users(name,email,password,age,department,experience,occupation)
               VALUES(?,?,?,?,?,?,?)""",
            (name, email, hash_password(password), age, department, experience, occupation)
        )
        conn.commit()
        return True, "Registered successfully!"
    except sqlite3.IntegrityError:
        return False, "Email already registered."
    finally:
        conn.close()


def login_user(email, password):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, hash_password(password))
    )
    user = cursor.fetchone()
    conn.close()
    return user


# ── Admin auth ─────────────────────────────────────────────

def login_admin(email, password):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM admins WHERE email=? AND password=?",
        (email, hash_password(password))
    )
    admin = cursor.fetchone()
    conn.close()
    return admin


def get_all_users():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id,name,email,age,department,experience,occupation,created_at FROM users ORDER BY created_at DESC")
    users = cursor.fetchall()
    conn.close()
    return users