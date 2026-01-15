import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'users.db')

def init_db():
    """Initializes the users table if it doesn't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'student'
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup_user(username, password, role='student'):
    try:
        init_db()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        pwd_hash = hash_password(password)
        c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                  (username, pwd_hash, role))
        conn.commit()
        conn.close()
        return True, "User created successfully."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    except Exception as e:
        return False, f"Error: {e}"

def login_user(username, password):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    pwd_hash = hash_password(password)
    c.execute("SELECT username, role FROM users WHERE username=? AND password_hash=?", (username, pwd_hash))
    user = c.fetchone()
    conn.close()
    
    if user:
        return {"username": user[0], "role": user[1]}
    else:
        return None
