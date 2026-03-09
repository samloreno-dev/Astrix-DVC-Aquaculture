import sqlite3

# Create (or connect to) the database file
conn = sqlite3.connect('aquaculture.db')
cursor = conn.cursor()

# 1. Create Users Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
''')

# 2. Create Devices Table (1 User : N Devices)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Devices (
        device_id TEXT PRIMARY KEY,
        user_id INTEGER,
        location TEXT,
        FOREIGN KEY (user_id) REFERENCES Users (user_id)
    )
''')

# 3. Create Sensor Logs Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS SensorLogs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        ph REAL,
        temp REAL,
        do REAL,
        turbidity REAL,
        quality_score INTEGER,
        FOREIGN KEY (device_id) REFERENCES Devices (device_id)
    )
''')

conn.commit()
conn.close()
print("Step 2 Complete: 'aquaculture.db' created with normalized tables.")