from db import fetch_all, fetch_one, execute_query

def get_all_books():
    query = """
            select BookID, BookCode, Title, Author, Category, Publisher, PublishYear, BookStatus
            from Books
            order by BookID
"""
    return fetch_all(query)

def get_book_by_code(book_code):
    query = """
            select BookID, BookCode, Title, Author, Category, Publisher, PublishYear, BookStatus
            from Books
            where BookCode = ?
"""
    return fetch_one(query,(book_code))

def search_books(keyword):
    query = """
            select BookID, BookCode, Title, Author, Category, Publisher, PublishYear, BookStatus
            from Books
            where BookCode like ?
                    or Title like ?
                    or Author like ?
                    or Category like ?
            order by BookID
"""
    like_keyword = f'%{keyword}%'
    return fetch_all(query,(like_keyword, like_keyword, like_keyword, like_keyword))

def add_book (book_code, title, author, category, publisher, publish_year, book_status = "Available"):
    query = """
            insert into Books (BookCode, Title, Author, Category, Publisher, PublishYear, BookStatus)
            VALUES (?,?,?,?,?,?,?)
"""
    params = (book_code, title, author, category, publisher, publish_year, book_status)
    return execute_query(query,params)

def update_book (book_code, title, author, category, publisher, publish_year):
    query = """
            update Books
            set Title = ?, Author = ?, Category = ?, Publisher = ?, publishYear = ?
            where BookCode = ?
    """
    params = (title, author, category, publisher, publish_year, book_code)
    return execute_query(query, params)

def delete_book(book_code):
    book = get_book_by_code(book_code)
    if not book:
        print("Khong tim thay sach, xin vui long tim sach khac")
        return False
    if book.BookStatus != "Available":
        print("Khong xoa sach duoc do sach hien khong Available")
        return False
    query = """
            delete from Books where BookCode = ?
"""
    result = execute_query(query, (book_code,))
    if result:
        print("Xoa sach thanh cong")
        return True
    else:
        print("Xoa sach that bai")
        return False

def is_book_code_exists(book_code):
    book = get_book_by_code(book_code)
    return book is not None

