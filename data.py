import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS SignUp (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Score (
            username TEXT PRIMARY KEY,
            total_matches INTEGER DEFAULT 0,
            total_wins INTEGER DEFAULT 0,
            win_rate REAL DEFAULT 0,
            FOREIGN KEY (username) REFERENCES SignUp(username)
        )
    ''')
    conn.commit()
    conn.close()

def get_user_stats(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT total_matches, total_wins, win_rate FROM Score WHERE username = ?", (username,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return {
            'total_matches': result[0],
            'total_wins': result[1],
            'win_rate': result[2]
        }
    else:
        return None

def update_user_score(username, user_won):
    conn = get_db_connection()
    cursor = conn.cursor()

   
    cursor.execute("UPDATE Score SET total_matches = total_matches + 1 WHERE username = ?", (username,))

    if user_won:
        cursor.execute("UPDATE Score SET total_wins = total_wins + 1 WHERE username = ?", (username,))
   
    cursor.execute("""
        UPDATE Score 
        SET win_rate = 
        CASE 
            WHEN total_matches > 0 THEN total_wins * 1.0 / total_matches 
            ELSE 0 
        END 
        WHERE username = ?
    """, (username,))
    
    conn.commit()
    conn.close()
