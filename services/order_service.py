from db import fetch_all, fetch_one, get_connection, execute_query

def generate_order_code():
    query = """
        SELECT TOP 1 OderID from RentalOrders
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
        return "Khách hàng không tồn tại."
    
    if not book_codes:
        return "Thông tin sách được thuê trống."
    
    normalized_codes = [] #danh sách các mã đã được chuẩn hóa
    seen = set() #Loại bỏ các code trùng lặp 

    # Chuẩn hóa book code
    for code in book_codes:
        code = code.strip()
        if not code:
            continue
        upper_code = code.upper()

        if upper_code not in seen:
            seen.add(upper_code)
            normalized_codes.append(upper_code)
        
    if not normalized_codes:
        return "Thông tin mã sách thuê không hợp lệ"
    
    # Kiểm tra tính hợp lệ của sách
    books = []
    for code in normalized_codes:
        book = get_book_by_code(code)
        if not book:
            return f'Sách với mã {code} không tồn tại. '
        if book.BookStatus != "Available":
            print(f'Sách với mã {code} hiện không sẵn sàng để được thuê.')
            return False
        books.append(book)

    # Tạo mã order mới và thêm vào database
    order_code = generate_order_code()
    conn = get_connection()
    if not conn:
        print("Lỗi kết nối với Database")
        return False
    
    # Insert đơn thuê vào bảng RentalOrders
    try:
        cursor = conn.cursor()
        insert_order_query = """
            INSERT INTO RentalOrders (OrderCode, CustomerID, RentDate, ExpectedReturnDate, ReturnDate, OrderStatus)
            OUTPUT INSERTED.OrderID
            VALUES (?, ?, GETDATE(), ?, NULL, 'Renting')
        """

        cursor.execute(insert_order_query, (order_code, customer.CustomerID, expected_return_date))
        # Lấy ra dòng chứa OrderID
        order_row = cursor.fetchone()

        if not order_row:
            conn.rollback() #hủy bỏ tất cả các thay đổi chưa được lưu (commit) trong một giao dịch (transaction) hiện tại, nhằm đưa cơ sở dữ liệu về trạng thái an toàn trước đó khi gặp lỗi. 
            print("Tạo đơn thuê thất bại.")
            return False

        order_id = order_row[0] # OrderID nằm ở cột đầu tiên trong order_row
        
        # THêm chi tiết sách vào đơn
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
        print()
        print(f'Tạo đơn thuê thành công. Mã đơn: {order_code}')
        return True

    except Exception as e:
        conn.rollback()
        print(f"Lỗi khi tạo đơn thuê: {e}")
        return False
    
    finally:
        if conn:
            conn.close()

# Hàm thực hiện trả sách:
# - kiểm tra đơn thuê có tồn tại không
# - kiểm tra đơn đã trả chưa
# - cập nhật trạng thái đơn thành “Returned”
# - cập nhật lại trạng thái các sách về “Available”
def return_rental_order (order_code):
    order = get_order_by_code (order_code)

    if not order:
        print("Đơn thuê không tồn tại.")
        return False
    
    if order.OrderStatus == "Returned":
        print("Đơn thuê này đã được hoàn trả.")
        return False
    
    conn = get_connection()
    if not conn:
        print("Lỗi kết nối đến database.")
        return False
    
    try:
        cursor = conn.cursor()
        # cập nhật trạng thái đơn thành “Returned”
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
        print("Ghi nhận trả sách thành công.")
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"Lỗi khi ghi nhận trả sách: {e}")
        return False
    finally:
        if conn:
            conn.close()







