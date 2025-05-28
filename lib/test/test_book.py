def test_add_book(db, sample_book):
    book_id = db.add_book(sample_book)
    assert book_id == 1

def test_get_book(db, sample_book):
    db.add_book(sample_book)
    book = db.get_book_by_id(1)
    assert book.title == "Test Book"
    assert book.author == "Test Author"

def test_delete_book(db, sample_book):
    db.add_book(sample_book)
    assert db.delete_book(1) is True
    assert db.get_book_by_id(1) is None