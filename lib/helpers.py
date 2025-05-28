def display_books(books):
    """Display books in a formatted table"""
    if not books:
        print("No books found.")
        return
        
    print("\n{:<5} {:<30} {:<20} {:<15} {:<10} {:<10}".format(
        "ID", "Title", "Author", "Genre", "Year", "Status"))
    print("-" * 90)
    
    for book in books:
        print("{:<5} {:<30} {:<20} {:<15} {:<10} {:<10}".format(
            book[0], 
            book[1][:28] + '..' if len(book[1]) > 30 else book[1],
            book[2][:18] + '..' if len(book[2]) > 20 else book[2],
            book[3][:13] + '..' if book[3] and len(book[3]) > 15 else book[3] if book[3] else 'N/A',
            book[4] if book[4] else 'N/A',
            book[5]))