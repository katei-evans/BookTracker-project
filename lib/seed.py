from models import get_connection

def seed():
    conn = get_connection()
    cursor = conn.cursor()
    books = [
        ("1984", "George Orwell", "Dystopian", 1949, "Read"),
        ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 1937, "Unread")
    ]
    cursor.executemany("INSERT INTO books (title, author, genre, year, status) VALUES (?, ?, ?, ?, ?)", books)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed()
