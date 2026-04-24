from db import fetch_all, execute_query,fetch_one
from menus.main_menu import show_main_menu

def select_books():
    query = "SELECT BookID, BookCode, Title, BookStatus FROM Books"
    rows = fetch_all(query)

    if not rows:
        print("Không có dữ liệu hoặc truy vấn lỗi.")
        return

    print("Danh sách books:")
    for row in rows:
        print(row.BookID, row.BookCode, row.Title, row.BookStatus)

def insert_customer():
    query = """INSERT INTO Customers (CustomerCode, FullName, Phone, Address, Email)
            VALUES (?, ?, ?, ?, ?)"""
    params = ('C003', 'Le Van C', '0903333333', 'Da Nang', 'c@gmail.com')

    result = execute_query(query, params)

    if result:
        print("Insert khách hàng thành công.")
    else:
        print("Insert khách hàng thất bại.")
from db import fetch_all

def show_customers():
    query = "SELECT CustomerID, CustomerCode, FullName, Phone FROM Customers"
    rows = fetch_all(query)

    for row in rows:
        print(row.CustomerID, row.CustomerCode, row.FullName, row.Phone)

def main():
    show_main_menu()

if __name__ == "__main__":
    main()