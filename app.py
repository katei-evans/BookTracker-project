import sqlite3

class Book:
    def __init__(self, title, author, genre, year, status):
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.status = status

class BookDatabase:
    def __init__(self, db_name="books.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT,
            year INTEGER,
            status TEXT CHECK(status IN ('Read', 'Unread')) NOT NULL
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_book(self, book):
        query = """
        INSERT INTO books (title, author, genre, year, status)
        VALUES (?, ?, ?, ?, ?)
        """
        self.conn.execute(query, (book.title, book.author, book.genre, book.year, book.status))
        self.conn.commit()

    def get_all_books(self):
        cursor = self.conn.execute("SELECT * FROM books")
        return cursor.fetchall()
if __name__ == "__main__":
    db = BookDatabase()

    new_book = Book("The Hobbit", "J.R.R. Tolkien", "Fantasy", 1937, "Read")

    db.add_book(new_book)

    all_books = db.get_all_books()
    for book in all_books:
        print(book)
