import pytest
from models.book import Book, BookDatabase

@pytest.fixture
def db():
    """Fixture for database connection"""
    db = BookDatabase(":memory:")
    db.create_table()
    yield db
    db.conn.close()

@pytest.fixture
def sample_book():
    """Fixture for sample book"""
    return Book("Test Book", "Test Author", "Fiction", 2023, "Unread")