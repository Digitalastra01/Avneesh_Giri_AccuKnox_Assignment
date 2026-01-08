import sqlite3
import requests
import json
import sys

# Configuration
API_URL = "https://api.example.com/books" # Placeholder URL
DB_NAME = "books.db"

def fetch_books_from_api():
    """
    Fetches books from the API.
    Uses a mock response if the URL is the placeholder.
    """
    if "api.example.com" in API_URL:
        print("[INFO] Using mock data for demonstration purposes.")
        return [
            {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
            {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
            {"title": "1984", "author": "George Orwell", "year": 1949},
            {"title": "Pride and Prejudice", "author": "Jane Austen", "year": 1813},
            {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "year": 1951}
        ]
    
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch data from API: {e}")
        return []

def setup_database():
    """Creates the books table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER
            )
        ''')
        conn.commit()
        return conn
    except sqlite3.Error as e:
        print(f"[ERROR] Database setup failed: {e}")
        sys.exit(1)

def save_books(conn, books):
    """Inserts books into the database, avoiding duplicates based on title."""
    cursor = conn.cursor()
    count = 0
    for book in books:
        try:
            # Check if exists (simple check by title for this example)
            cursor.execute("SELECT id FROM books WHERE title = ?", (book['title'],))
            if cursor.fetchone() is None:
                cursor.execute(
                    "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
                    (book['title'], book['author'], book['year'])
                )
                count += 1
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to insert book {book.get('title')}: {e}")
    
    conn.commit()
    print(f"[INFO] stored {count} new books in the database.")

def display_books(conn):
    """Retrieves and displays all books from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT title, author, year FROM books")
    rows = cursor.fetchall()
    
    print("\n--- Books in Database ---")
    print(f"{'Title':<30} | {'Author':<20} | {'Year'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<30} | {row[1]:<20} | {row[2]}")
    print("-" * 60)

def main():
    print("Starting Book Manager...")
    
    # 1. Fetch Data
    books = fetch_books_from_api()
    if not books:
        print("No books found.")
        return

    # 2. Setup Database
    conn = setup_database()

    # 3. Store Data
    save_books(conn, books)

    # 4. Display Data
    display_books(conn)

    conn.close()
    print("Done.")

if __name__ == "__main__":
    main()
