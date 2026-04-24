from datetime import datetime
from services.order_service import (
    create_rental_order,
    get_all_orders,
    get_order_by_code,
    get_order_details,
    return_rental_order,
)


def print_order_header():
    print("-" * 130)
    print(
        f"{'ID':<5}{'OrderCode':<12}{'CustCode':<12}{'Customer Name':<25}"
        f"{'RentDate':<22}{'ExpectedReturn':<22}{'Status':<12}"
    )
    print("-" * 130)


def print_order_row(order):
    rent_date = str(order.RentDate)[:19] if order.RentDate else ""
    expected_return = str(order.ExpectedReturnDate)[:19] if order.ExpectedReturnDate else ""

    print(
        f"{order.OrderID:<5}{order.OrderCode:<12}{order.CustomerCode:<12}{order.FullName:<25}"
        f"{rent_date:<22}{expected_return:<22}{order.OrderStatus:<12}"
    )


def show_all_orders():
    orders = get_all_orders()

    if not orders:
        print("Không có đơn thuê nào trong hệ thống.")
        return

    print("\n===== DANH SÁCH ĐƠN THUÊ =====")
    print_order_header()
    for order in orders:
        print_order_row(order)
    print("-" * 130)


def handle_create_order():
    print("\n===== TẠO ĐƠN THUÊ =====")
    customer_code = input("Nhập mã khách hàng: ").strip()

    raw_book_codes = input("Nhập danh sách mã sách, cách nhau bằng dấu phẩy: ").strip()
    expected_return_date = input("Nhập ngày dự kiến trả (YYYY-MM-DD): ").strip()

    if not customer_code or not raw_book_codes or not expected_return_date:
        print("Không được để trống thông tin bắt buộc.")
        return

    try:
        parsed_date = datetime.strptime(expected_return_date, "%Y-%m-%d")
        expected_return_str = parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        print("Ngày dự kiến trả không đúng định dạng YYYY-MM-DD.")
        return

    book_codes = [code.strip() for code in raw_book_codes.split(",") if code.strip()]

    success, message = create_rental_order(
        customer_code=customer_code,
        book_codes=book_codes,
        expected_return_date=expected_return_str,
    )
    print(message)


def handle_view_order_detail():
    print("\n===== XEM CHI TIẾT ĐƠN THUÊ =====")
    order_code = input("Nhập mã đơn thuê: ").strip()

    if not order_code:
        print("Mã đơn thuê không được để trống.")
        return

    order = get_order_by_code(order_code)
    if not order:
        print("Không tìm thấy đơn thuê.")
        return

    print("\n--- THÔNG TIN ĐƠN THUÊ ---")
    print(f"Mã đơn thuê       : {order.OrderCode}")
    print(f"Mã khách hàng     : {order.CustomerCode}")
    print(f"Tên khách hàng    : {order.FullName}")
    print(f"Ngày thuê         : {order.RentDate}")
    print(f"Ngày dự kiến trả  : {order.ExpectedReturnDate}")
    print(f"Ngày trả thực tế  : {order.ReturnDate}")
    print(f"Trạng thái đơn    : {order.OrderStatus}")

    details = get_order_details(order_code)

    print("\n--- DANH SÁCH SÁCH TRONG ĐƠN ---")
    if not details:
        print("Không có chi tiết đơn thuê.")
        return

    print("-" * 90)
    print(f"{'BookCode':<12}{'Title':<35}{'Author':<25}{'BookStatus':<12}")
    print("-" * 90)
    for item in details:
        print(f"{item.BookCode:<12}{item.Title:<35}{item.Author:<25}{item.BookStatus:<12}")
    print("-" * 90)


def handle_return_order():
    print("\n===== GHI NHẬN TRẢ SÁCH =====")
    order_code = input("Nhập mã đơn thuê cần trả: ").strip()

    if not order_code:
        print("Mã đơn thuê không được để trống.")
        return

    success, message = return_rental_order(order_code)
    print(message)


def show_order_menu():
    while True:
        print("\n================ QUẢN LÝ ĐƠN THUÊ ================")
        print("1. Tạo đơn thuê")
        print("2. Xem danh sách đơn thuê")
        print("3. Xem chi tiết đơn thuê")
        print("4. Ghi nhận trả sách")
        print("0. Quay lại")
        print("==================================================")

        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            handle_create_order()
        elif choice == "2":
            show_all_orders()
        elif choice == "3":
            handle_view_order_detail()
        elif choice == "4":
            handle_return_order()
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")