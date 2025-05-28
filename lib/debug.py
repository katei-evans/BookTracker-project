from models import Book, create_connection, create_tables
from helpers import display_books

def test_application():
    conn = create_connection(":memory:")
    assert conn is not None, "Database connection failed"
    
    create_tables(conn)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
    assert cursor.fetchone() is not None, "Table creation failed"
    
    test_book = Book("Test Book", "Test Author")
    book_id = test_book.save()
    assert book_id is not None, "Book saving failed"
    
    books = Book.get_all()
    assert len(books) > 0, "Book retrieval failed"
    
    print("All tests passed successfully!")
    conn.close()

if __name__ == "__main__":
    test_application()