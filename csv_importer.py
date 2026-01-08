import csv
import sqlite3
import os

# Configuration
CSV_FILE = "users.csv"
DB_NAME = "users.db"

def setup_database():
    """Creates the users table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # Email as UNIQUE to avoid duplicates
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        conn.commit()
        return conn
    except sqlite3.Error as e:
        print(f"[ERROR] Database creation failed: {e}")
        return None

def import_csv_to_db(conn):
    """
    Reads data from CSV and inserts into SQLite database.
    """
    if not os.path.exists(CSV_FILE):
        print(f"[ERROR] CSV file '{CSV_FILE}' not found. Please run generate_sample_data.py first.")
        return

    cursor = conn.cursor()
    success_count = 0
    duplicate_count = 0
    error_count = 0

    print(f"Reading from {CSV_FILE}...")
    
    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('name')
            email = row.get('email')

            if not name or not email:
                print(f"[WARN] Skipping invalid row: {row}")
                error_count += 1
                continue

            try:
                cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
                success_count += 1
            except sqlite3.IntegrityError:
                print(f"[INFO] Skipping duplicate email: {email}")
                duplicate_count += 1
            except sqlite3.Error as e:
                print(f"[ERROR] Database error for {email}: {e}")
                error_count += 1
    
    conn.commit()
    print("\n--- Import Summary ---")
    print(f"Successfully inserted: {success_count}")
    print(f"Duplicates skipped:    {duplicate_count}")
    print(f"Errors/Invalid rows:   {error_count}")

def display_users(conn):
    """Displays first 10 users for verification."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users LIMIT 10")
    rows = cursor.fetchall()

    print("\n--- First 10 Users in DB ---")
    for row in rows:
        print(row)

def main():
    print("Starting CSV Importer...")
    
    conn = setup_database()
    if not conn:
        return

    import_csv_to_db(conn)
    display_users(conn)
    conn.close()
    print("Done.")

if __name__ == "__main__":
    main()
