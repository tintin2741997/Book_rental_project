from db import fetch_all, fetch_one, get_connection
from services.order_service import generate_order_code

def search_books_for_customer (keyword): #Khác với def search_book của admin (admin chỉ cần truyền book code)
    query = """
        Select BookID, BookCode, Title, Author, Category, Publisher, PublishYear, BookStatus from Books
        where BookCode like ?
                or Title like ?
                or Author like ?
                or Category like ?
        order by BookID;
    """
    like_keyword = f'%{keyword}%'
    return fetch_all(query,(like_keyword,like_keyword,like_keyword,like_keyword))

def get_book_info_by_code(book_code):
    query = """
        select BookID, BookCode, Title, Author, Category, Publisher, PublishYear, BookStatus
        from Books
        where BookCode = ?
        order by BookID
    """
    return fetch_one(query,(book_code,))

def get_books_by_status_for_customer(status):
    query = """
        select BookID, BookCode, Title, Author, Category, Publisher, PublishYear, BookStatus
        from Books
        where BookStatus = ?
        order by BookID
    """
    return fetch_all(query, (status,))

def create_rental_order_for_customer(customer_id, book_codes, expected_return_date):
    if not customer_id:
        print("Vui lòng nhập mã khách hàng.")
        return False
    if not book_codes:
        print("Vui lòng nhập mã sách muốn thuê.")
        return False
    
    seen = set()
    normalized_codes = []

    for code in book_codes:
        code = code.strip()
        if not code:
            continue # Xu ly truong hop nhap space
        upper_code = code.upper()
        if upper_code not in seen:
            normalized_codes.append(upper_code)
            seen.add(upper_code)
    
    if not normalized_codes:
        print("Mã sách không hợp lệ")
        return False
    
    books = []
    for code in normalized_codes:
        book = get_book_info_by_code(code)
        if not book:
            print(f'Mã sách {code} không tồn tại.')
            return False
        if book.BookStatus != "Available":
            print(f'Sách với mã {code} hiện đã được thuê')
            return False
        books.append(book)
    
    order_code = generate_order_code()

    conn = get_connection()
    if not conn:
        print("Lỗi kết nối database")
        return False
    try:
        cursor = conn.cursor()

        cursor.execute ("""
            insert into RentalOrders (OrderCode, CustomerID, RentDate, ExpectedReturnDate, ReturnDate, OrderStatus)
            output inserted.OrderID
            values (?,?,getdate(), ?, NULL, 'Renting')
        """,(order_code, customer_id, expected_return_date))

        row = cursor.fetchone()
        if not row:
            print('Có lỗi xảy ra, không thể tạo đơn thuê')
            conn.rollback
            return False
        
        order_id = row[0]

        for book in books:
            cursor.execute("""
                insert into RentalOrderDetails (OrderID, BookID)
                values(?,?)
            """,(order_id, book.BookID,))

        cursor.execute("""
            update Books
            set BookStatus = 'Rented'
            where BookID = ?
        """,(book.BookID,))

        conn.commit
        print("Tạo đơn thuê thành công.")
        return True

    except Exception as e:
        print(f'Lỗi {e} xảy ra khi tạo đơn thuê')
        conn.rollback
        return False
    finally:
        conn.close()

def get_current_rented_books_by_customer(customer_id):
    query = """
        select ro.OrderCode, ro.RentDate, ro.ExpectedReturnDate, ro.OrderStatus,
                b.BookID, b.Title, b.Author
        from RentalOrders ro join RentalOrderDetails rod on ro.OrderID = rod.OrderID
                            join Books b on rod.BookID = b.BookID
        where ro.CustomerID = ? and ro.OrderStatus = 'Renting'
        order by b.BookID, ro.OrderID desc
    """
    return fetch_all(query, (customer_id,))