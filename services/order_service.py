from db import fetch_all, fetch_one, get_connection, execute_query
from datetime import datetime
def generate_order_code():
    query = """
        SELECT TOP 1 OrderID from RentalOrders
        ORDER BY OrderID DESC
    """
    row = fetch_one(query)
    if not row:
        return "O001"
    
    next_id = row.OrderID + 1

    return f"O{next_id:03d}"

def get_customer_by_code(customer_code):
    query = """
        SELECT CustomerID, CustomerCode, FullName from Customers
        WHERE CustomerCode = ?
    """
    return fetch_one(query, (customer_code,))
    
def get_book_by_code(book_code):
    query = """
    SELECT BookID, BookCode, Title, BookStatus from Books
    WHERE BookCode =  ?
"""
    return fetch_one(query, (book_code,))

def get_order_by_code(order_code):
    query = """
        SELECT ro.OrderID, ro.OrderCode, c.CustomerCode, c.FullName,
               ro.RentDate, ro.ExpectedReturnDate, ro.ReturnDate, ro.OrderStatus
        FROM RentalOrders ro
        JOIN Customers c ON ro.CustomerID = c.CustomerID
        WHERE ro.OrderCode = ?
"""
    return fetch_one(query, (order_code,))

def get_all_orders():
    query = """
    SELECT ro.OrderID, ro.OrderCode, c.CustomerCode, c.FullName,
            ro.RentDate, ro.ExpectedReturnDate, ro.ReturnDate, ro.OrderStatus
        FROM RentalOrders ro
        JOIN Customers c ON ro.CustomerID = c.CustomerID
        ORDER BY ro.OrderID DESC
""" 
    return fetch_all(query)

def get_order_details(order_code):
    query = """
    SELECT ro.OrderCode, b.BookCode, b.Title, b.Author, b.BookStatus
    FROM RentalOrders ro
    JOIN RentalOrderDetails rod ON ro.OrderID = rod.OrderID
    JOIN Books b ON rod.BookID = b.BookID
    WHERE ro.OrderCode = ?
    ORDER BY b.BookID
"""
    return fetch_all(query,(order_code,))

def create_rental_order(customer_code, book_codes, expected_return_date):
    customer = get_customer_by_code(customer_code)

    if not customer:
        return False, "Khách hàng không tồn tại."
    
    if not book_codes:
        return False, "Thông tin sách được thuê trống."
    
    # Kiểm tra ExpectedReturnDate >= RentDate
    try:
        expected_date = datetime.strptime(expected_return_date, "%Y-%m-%d")
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if expected_date < today:
            return False, "Ngày dự kiến trả phải sau ngày thuê (hôm nay)."
    except ValueError:
        return False, "Định dạng ngày không hợp lệ."
    
    normalized_codes = [] #danh sách các mã đã được chuẩn hóa
    seen = set() #Loại bỏ các code trùng lặp 

    # Chuẩn hóa book code và kiểm tra trùng lặp
    for code in book_codes:
        code = code.strip()
        if not code:
            continue
        upper_code = code.upper()

        if upper_code in seen:
            return False, f"Mã sách '{upper_code}' bị trùng trong đơn. Không được phép trùng sách trong cùng đơn thuê."
        
        seen.add(upper_code)
        normalized_codes.append(upper_code)
        
    if not normalized_codes:
        return False, "Thông tin mã sách thuê không hợp lệ"
    
    # Kiểm tra tính hợp lệ của sách
    books = []
    for code in normalized_codes:
        book = get_book_by_code(code)
        if not book:
            return False, f'Sách với mã {code} không tồn tại. '
        if book.BookStatus != "Available":
            return False, f'Sách với mã {code} hiện không sẵn sàng để được thuê.'
        books.append(book)

    # Tạo mã order mới và thêm vào database
    order_code = generate_order_code()
    conn = get_connection()
    
    # Insert đơn thuê vào bảng RentalOrders sử dụng transaction
    if not conn:
        return False, "Lỗi kết nối với Database"
    
    try:
        cursor = conn.cursor()
        # Bắt đầu transaction
        
        insert_order_query = """
            INSERT INTO RentalOrders (OrderCode, CustomerID, RentDate, ExpectedReturnDate, ReturnDate, OrderStatus)
            OUTPUT INSERTED.OrderID
            VALUES (?, ?, GETDATE(), ?, NULL, 'Renting')
        """

        cursor.execute(insert_order_query, (order_code, customer.CustomerID, expected_return_date))
        # Lấy ra dòng chứa OrderID
        order_row = cursor.fetchone()

        if not order_row:
            conn.rollback()
            conn.close()
            return False, "Tạo đơn thuê thất bại."

        order_id = order_row[0] # OrderID nằm ở cột đầu tiên trong order_row
        
        # Thêm chi tiết sách vào đơn
        for book in books:
            #Thêm chi tiết sách vào bảng RentalOrderDetails
            cursor.execute(
                "INSERT INTO RentalOrderDetails (OrderID, BookID) VALUES (?, ?)",
                (order_id, book.BookID)
            )
            # Cập nhật status sách
            cursor.execute(
                "UPDATE Books SET BookStatus = 'Rented' WHERE BookID = ?",
                (book.BookID,)
            )

        conn.commit()
        conn.close()
        return True, f'Tạo đơn thuê thành công. Mã đơn: {order_code}'

    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Lỗi khi tạo đơn thuê: {e}"

# Hàm thực hiện trả sách:
# - kiểm tra đơn thuê có tồn tại không
# - kiểm tra đơn đã trả chưa
# - cập nhật trạng thái đơn thành “Returned”
# - cập nhật lại trạng thái các sách về “Available”
def return_rental_order (order_code):
    order = get_order_by_code (order_code)

    if not order:
        return False, "Đơn thuê không tồn tại."
    
    if order.OrderStatus == "Returned":
        return False, "Đơn thuê này đã được hoàn trả."
    
    conn = get_connection()
    if not conn:
        return False, "Lỗi kết nối đến database."
    
    try:
        cursor = conn.cursor()
        # Bắt đầu transaction
        
        # cập nhật trạng thái đơn thành "Returned"
        cursor.execute(
            """
            update RentalOrders 
            set ReturnDate = GETDATE(), OrderStatus = 'Returned'
            where OrderCode = ? 
        """, (order_code,)
        )

        # cập nhật lại trạng thái các sách nằm trong Order được hoàn trả về “Available”
        cursor.execute("""
            UPDATE Books
            SET BookStatus = 'Available'
            WHERE BookID IN (
                SELECT rod.BookID
                FROM RentalOrderDetails rod
                JOIN RentalOrders ro ON rod.OrderID = ro.OrderID
                WHERE ro.OrderCode = ?
            )
        """, (order_code,))

        conn.commit()
        conn.close()
        return True, "Trả sách thành công."
        
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Lỗi khi ghi nhận trả sách: {e}"
