from models import Book, BookDatabase
from helpers import display_books
import sys

def main():
    print("\nWelcome to Book Tracker CLI!")
    
    with BookDatabase() as db:
        while True:
            print("\nMain Menu:")
            print("1. Add a new book")
            print("2. View all books")
            print("3. Search books")
            print("4. Update a book")
            print("5. Delete a book")
            print("6. Exit")
            
            choice = input("\nWhat would you like to do? (1-6): ")
            
            if choice == "1":
                add_book_interactive(db)
            elif choice == "2":
                view_books_interactive(db)
            elif choice == "3":
                search_books_interactive(db)
            elif choice == "4":
                update_book_interactive(db)
            elif choice == "5":
                delete_book_interactive(db)
            elif choice == "6":
                print("\nThank you for using Book Tracker! Goodbye!")
                sys.exit()
            else:
                print("\nInvalid choice. Please enter a number between 1-6.")

def add_book_interactive(db):
    print("\n➕ Add a New Book")
    while True:
        title = input("Title: ").strip()
        if not title:
            print("Title cannot be empty. Please try again.")
            continue
        break
    
    while True:
        author = input("Author: ").strip()
        if not author:
            print("Author cannot be empty. Please try again.")
            continue
        break
    
    genre = input("Genre (optional, press Enter to skip): ").strip() or None
    
    while True:
        year = input("Publication year (optional, press Enter to skip): ").strip()
        if not year:
            year = None
            break
        if year.isdigit():
            year = int(year)
            break
        print("Year must be a number. Please try again.")
    
    while True:
        status = input("Status (R for Read, U for Unread): ").upper()
        if status in ["R", "U"]:
            status = "Read" if status == "R" else "Unread"
            break
        print("Please enter R or U.")
    
    try:
        book = Book(title, author, genre, year, status)
        book_id = db.add_book(book)
        print(f"\nSuccess! Book added with ID: {book_id}")
    except Exception as e:
        print(f"\nError: {e}")

def view_books_interactive(db):
    print("\nYour Book Collection")
    books = db.get_all_books()
    
    if not books:
        print("\nYou don't have any books yet. Try adding some!")
        return
    
    display_books([(b.id, b.title, b.author, b.genre, b.year, b.status) for b in books])
    
    while True:
        print("\nOptions:")
        print("1. View details of a specific book")
        print("2. Return to main menu")
        choice = input("What would you like to do? (1-2): ")
        
        if choice == "1":
            book_id = input("\nEnter the ID of the book you want to view: ")
            try:
                book_id = int(book_id)
                book = db.get_book_by_id(book_id)
                if book:
                    print("\nBook Details:")
                    print(f"ID: {book.id}")
                    print(f"Title: {book.title}")
                    print(f"Author: {book.author}")
                    print(f"Genre: {book.genre if book.genre else 'Not specified'}")
                    print(f"Year: {book.year if book.year else 'Not specified'}")
                    print(f"Status: {book.status}")
                else:
                    print("No book found with that ID.")
            except ValueError:
                print("Please enter a valid number for the book ID.")
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")

def search_books_interactive(db):
    print("\nSearch Books")
    keyword = input("Enter search term (title or author): ").strip()
    
    if not keyword:
        print("Please enter a search term.")
        return
    
    results = db.search_books(keyword)
    
    if not results:
        print("\nNo books found matching your search.")
        return
    
    print(f"\nFound {len(results)} matching book(s):")
    display_books([(b.id, b.title, b.author, b.genre, b.year, b.status) for b in results])

def update_book_interactive(db):
    print("\nUpdate a Book")
    view_books_interactive(db)
    
    while True:
        book_id = input("\nEnter the ID of the book you want to update: ")
        try:
            book_id = int(book_id)
            book = db.get_book_by_id(book_id)
            if not book:
                print("No book found with that ID.")
                continue
            
            print("\nCurrent Book Details:")
            print(f"1. Title: {book.title}")
            print(f"2. Author: {book.author}")
            print(f"3. Genre: {book.genre if book.genre else 'Not specified'}")
            print(f"4. Year: {book.year if book.year else 'Not specified'}")
            print(f"5. Status: {book.status}")
            
            print("\nEnter the numbers of fields you want to update (comma-separated, e.g., '1,3,5'):")
            fields = input("Fields to update: ").strip().split(',')
            
            updates = {}
            for field in fields:
                field = field.strip()
                if field == "1":
                    new_title = input("New title: ").strip()
                    if new_title:
                        updates['title'] = new_title
                elif field == "2":
                    new_author = input("New author: ").strip()
                    if new_author:
                        updates['author'] = new_author
                elif field == "3":
                    new_genre = input("New genre (press Enter to clear): ").strip()
                    updates['genre'] = new_genre if new_genre else None
                elif field == "4":
                    while True:
                        new_year = input("New year (press Enter to clear): ").strip()
                        if not new_year:
                            updates['year'] = None
                            break
                        if new_year.isdigit():
                            updates['year'] = int(new_year)
                            break
                        print("Year must be a number. Please try again.")
                elif field == "5":
                    while True:
                        new_status = input("New status (R for Read, U for Unread): ").upper()
                        if new_status in ["R", "U"]:
                            updates['status'] = "Read" if new_status == "R" else "Unread"
                            break
                        print("Please enter R or U.")
                else:
                    print(f"Ignoring invalid field number: {field}")
            
            if not updates:
                print("No valid updates provided.")
                continue
            
            # Apply updates to the book object
            updated_book = Book(
                title=updates.get('title', book.title),
                author=updates.get('author', book.author),
                genre=updates.get('genre', book.genre),
                year=updates.get('year', book.year),
                status=updates.get('status', book.status),
                book_id=book.id
            )
            
            if db.update_book(updated_book):
                print("\nBook updated successfully!")
            else:
                print("\nFailed to update book.")
            break
            
        except ValueError:
            print("Please enter a valid number for the book ID.")
        except Exception as e:
            print(f"Error: {e}")
            break

def delete_book_interactive(db):
    print("\n Delete a Book")
    view_books_interactive(db)
    
    while True:
        book_id = input("\nEnter the ID of the book you want to delete: ")
        try:
            book_id = int(book_id)
            book = db.get_book_by_id(book_id)
            if not book:
                print("No book found with that ID.")
                continue
            
            print(f"\nYou're about to delete: {book.title} by {book.author}")
            confirm = input("Are you sure? This cannot be undone. (y/n): ").lower()
            
            if confirm == 'y':
                if db.delete_book(book_id):
                    print("Book deleted successfully!")
                else:
                    print("Failed to delete book.")
            else:
                print("Deletion cancelled.")
            break
        except ValueError:
            print("Please enter a valid number for the book ID.")
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()