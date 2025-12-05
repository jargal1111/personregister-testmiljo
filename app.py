def init_database():
    """Initialize the database and create users table"""
    db_path = os.getenv('DATABASE_PATH', '/data/test_users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    
    # Check if users already exist
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert test users only if table is empty
        test_users = [
            ('Anna Andersson', 'anna@test.se'),
            ('Bo Bengtsson', 'bo@test.se')
        ]
        
        cursor.executemany('INSERT INTO users (name, email) VALUES (?, ?)', test_users)
        print("Database initialized with test users")
    else:
        print(f"Database already contains {count} users")
    
    conn.commit()
    conn.close()