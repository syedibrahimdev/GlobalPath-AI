import os
import sqlite3
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_key_secret_123'
DB_PATH = 'globalpath.db'

# Simple DB Helper Functions
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'Student'
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS agents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        license_number TEXT UNIQUE NOT NULL,
        status TEXT NOT NULL,
        trust_score INTEGER DEFAULT 0
    )''')
    
    # Seed data
    cursor = conn.execute('SELECT COUNT(*) FROM agents')
    if cursor.fetchone()[0] == 0:
        conn.execute("INSERT INTO agents (name, license_number, status, trust_score) VALUES (?, ?, ?, ?)",
                    ("Global Education Services", "GX-101", "Safe", 98))
        conn.execute("INSERT INTO agents (name, license_number, status, trust_score) VALUES (?, ?, ?, ?)",
                    ("Fake Consultant Pvt", "BAD-666", "Blacklisted", 0))
        conn.commit()
    conn.close()

init_db()

# Routes
@app.route('/health')
def health():
    return "OK"

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html')
    return redirect(url_for('signup'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('auth.html', mode='login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db()
        existing = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if existing:
            flash('Username already exists.', 'error')
            conn.close()
        else:
            password_hash = generate_password_hash(password)
            conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
            conn.commit()
            conn.close()
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('auth.html', mode='signup')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user={'username': session['username']})

@app.route('/verify-agent', methods=['GET', 'POST'])
def verify_agent():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    result = None
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        
        # Load agents from JSON
        import json
        try:
            with open('data/agents_data.json', 'r') as f:
                agents = json.load(f)
            
            # Search by name or license number
            agent = None
            for a in agents:
                if (query.lower() in a['name'].lower()) or (query.upper() == a['license_number'].upper()):
                    agent = a
                    break
            
            if agent:
                result = agent
            else:
                result = {'status': 'Not Found', 'message': 'No record found in our database.'}
        except FileNotFoundError:
            result = {'status': 'Error', 'message': 'Database not available.'}
    
    return render_template('verify.html', result=result)

@app.route('/api/chat', methods=['POST'])
def chat():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'reply': "Please say something!"})
    
    # Try to use AI Engine
    try:
        from backend.ai_engine import get_chat_response
        bot_reply = get_chat_response(user_message)
        print(f"DEBUG: Message: {user_message} -> Reply: {bot_reply[:50]}...")
    except Exception as e:
        print(f"❌ Chat Error: {e}")
        bot_reply = "I'm having trouble connecting to the AI engine. Please check the server logs."
    
    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    print("=" * 60)
    print("🌍 GlobalPath AI Server Starting...")
    print("📍 Open: http://127.0.0.1:5001")
    print("=" * 60)
    app.run(debug=False, port=5001)
