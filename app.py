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

    def search_books(self, keyword):
        query = """
        SELECT * FROM books
        WHERE title LIKE ? OR author LIKE ?
        """
        keyword = f"%{keyword}%"
        cursor = self.conn.execute(query, (keyword, keyword))
        return cursor.fetchall()

    def delete_book(self, book_id):
        query = "DELETE FROM books WHERE id = ?"
        self.conn.execute(query, (book_id,))
        self.conn.commit()

    def update_book(self, book_id, title=None, author=None, genre=None, year=None, status=None):
        query = "UPDATE books SET "
        fields = []
        values = []

        if title:
            fields.append("title = ?")
            values.append(title)
        if author:
            fields.append("author = ?")
            values.append(author)
        if genre:
            fields.append("genre = ?")
            values.append(genre)
        if year:
            fields.append("year = ?")
            values.append(year)
        if status:
            status = status.capitalize()
            if status not in ["Read", "Unread"]:
                raise ValueError("Status must be 'Read' or 'Unread'")
            fields.append("status = ?")
            values.append(status)

        if not fields:
            return

        query += ", ".join(fields) + " WHERE id = ?"
        values.append(book_id)
        self.conn.execute(query, values)
        self.conn.commit()

def menu():
    db = BookDatabase()

    while True:
        print("\nWelcome to the Book Tracker!")
        print("1. Add a Book")
        print("2. View All Books")
        print("3. Search Books")
        print("4. Delete a Book")
        print("5. Update a Book")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            genre = input("Enter genre: ")
            year = input("Enter year: ")
            status = input("Enter status (Read/Unread): ")

            try:
                year = int(year)
                status = status.capitalize()
                if status not in ["Read", "Unread"]:
                    raise ValueError("Invalid status")
                new_book = Book(title, author, genre, year, status)
                db.add_book(new_book)
                print("Book added successfully!")
            except ValueError as ve:
                print(f"Error: {ve}")

        elif choice == "2":
            books = db.get_all_books()
            if books:
                print("\n Your Book List:")
                for book in books:
                    print(f"ID: {book[0]} | {book[1]} by {book[2]} | Genre: {book[3]} | Year: {book[4]} | Status: {book[5]}")
            else:
                print("No books found.")

        elif choice == "3":
            keyword = input("Enter a title or author to search: ")
            results = db.search_books(keyword)
            if results:
                print("\n Search Results:")
                for book in results:
                    print(f"ID: {book[0]} | {book[1]} by {book[2]} | Genre: {book[3]} | Year: {book[4]} | Status: {book[5]}")
            else:
                print("No matching books found.")

        elif choice == "4":
            book_id = input("Enter the ID of the book to delete: ")
            try:
                book_id = int(book_id)
                db.delete_book(book_id)
                print("Book deleted (if ID was valid).")
            except ValueError:
                print("Invalid ID. Please enter a number.")

        elif choice == "5":
            try:
                book_id = int(input("Enter the ID of the book to update: "))
                print("Leave a field blank to keep the current value.")
                title = input("New title: ")
                author = input("New author: ")
                genre = input("New genre: ")
                year_input = input("New year: ")
                year = int(year_input) if year_input else None
                status = input("New status (Read/Unread): ")
                status = status if status else None

                db.update_book(book_id, title or None, author or None, genre or None, year, status)
                print("Book updated successfully!")
            except ValueError as ve:
                print(f"Error: {ve}")

        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
