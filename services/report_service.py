from db import fetch_all, fetch_one

def count_rented_books():
    query = """
        select count(*) as TotalRented from Books
        where BookStatus = 'Rented'
    """
    return fetch_one(query)

def count_available_books():
    query = """
        select count(*) as TotalAvailable from Books 
        where BookStatus = 'Available'
    """
    return fetch_one(query)

# Hàm đếm số lần sách được thuê
def get_rental_count_by_book():
    query = """
            select b.BookCode, b.Title, b.Author, count(rod.BookID) as Rental_Count
            from Books b left join RentalOrderDetails rod on rod.BookID = b.BookID
            group by b.BookID, b.BookCode, b.Title, b.Author
            order by Rental_Count desc, b.BookID asc
    """
    return fetch_all(query)

def get_books_by_status(status):
    query = """
        select BookID, BookCode, Title, Author, Category, Publisher, PublishYear, BookStatus
        from Books
        where BookStatus = ?
        order by BookID
    """
    return fetch_all(query,(status,))