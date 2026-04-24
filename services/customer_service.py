from db import fetch_all, fetch_one, execute_query


def get_all_customers():
    query = """
        SELECT CustomerID, CustomerCode, FullName, Phone, Address, Email
        FROM Customers
        ORDER BY CustomerID
    """
    return fetch_all(query)


def get_customer_by_code(customer_code):
    query = """
        SELECT CustomerID, CustomerCode, FullName, Phone, Address, Email
        FROM Customers
        WHERE CustomerCode = ?
    """
    return fetch_one(query, (customer_code,))


def search_customers(keyword):
    query = """
        SELECT CustomerID, CustomerCode, FullName, Phone, Address, Email
        FROM Customers
        WHERE CustomerCode LIKE ?
           OR FullName LIKE ?
           OR Phone LIKE ?
        ORDER BY CustomerID
    """
    like_keyword = f"%{keyword}%"
    return fetch_all(query, (like_keyword, like_keyword, like_keyword))


def add_customer(customer_code, full_name, phone, address, email):
    query = """
        INSERT INTO Customers (CustomerCode, FullName, Phone, Address, Email)
        VALUES (?, ?, ?, ?, ?)
    """
    params = (customer_code, full_name, phone, address, email)
    return execute_query(query, params)


def update_customer(customer_code, full_name, phone, address, email):
    query = """
        UPDATE Customers
        SET FullName = ?, Phone = ?, Address = ?, Email = ?
        WHERE CustomerCode = ?
    """
    params = (full_name, phone, address, email, customer_code)
    return execute_query(query, params)


def is_customer_code_exists(customer_code):
    customer = get_customer_by_code(customer_code)
    if customer:
        return True
    else:
        return False

def has_active_rental(customer_id):
    query = """
        SELECT TOP 1 1
        FROM RentalOrders
        WHERE CustomerID = ? AND OrderStatus = 'Renting'
    """
    result = fetch_one(query, (customer_id,))
    if result:
        return True
    else:
        return False

def has_user_account (customer_id):
    query = """
    SELEECT * FROM Users
    WHERE CustomerID = ?
    """
    result = execute_query(query, (customer_id,))
    if result:
        return True
    else:
        return False

def delete_customer(customer_code):
    customer = get_customer_by_code(customer_code)

    if not customer:
        print("Khách hàng không tồn tại.")
        return False

    if has_active_rental(customer.CustomerID):
        print("Không thể xóa khách hàng đang có đơn thuê chưa trả.")
        return False    
    
    if has_user_account:
        print("Không thể xóa khách hàng đã có account")

    query = "DELETE FROM Customers WHERE CustomerCode = ?"
    result = execute_query(query, (customer_code,))

    if result:
        print("Xóa khách hàng thành công.")
        return True
    else:
        print("Xóa khách hàng thất bại")
        return False
        