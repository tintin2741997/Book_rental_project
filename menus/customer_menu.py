from datetime import datetime
from services.customer_user_service import (
    search_books_for_customer,
    get_book_info_by_code,
    get_books_by_status_for_customer,
    create_rental_order_for_customer,
    get_current_rented_books_by_customer,
)


def print_book_header():
    print("-" * 110)
    print(f"{'ID':<5}{'Code':<10}{'Title':<30}{'Author':<20}{'Category':<15}{'Year':<8}{'Status':<12}")
    print("-" * 110)


def print_book_row(book):
    print(
        f"{book.BookID:<5}{book.BookCode:<10}{book.Title:<30}{book.Author:<20}"
        f"{(book.Category or ''):<15}{str(book.PublishYear or ''):<8}{book.BookStatus:<12}"
    )


def handle_search_books():
    keyword = input("Nhập từ khóa (mã sách / tên sách / tác giả / thể loại): ").strip()

    if not keyword:
        print("Từ khóa không được để trống.")
        return

    books = search_books_for_customer(keyword)

    if not books:
        print("Không tìm thấy sách phù hợp.")
        return

    print_book_header()
    for book in books:
        print_book_row(book)
    print("-" * 110)


def handle_view_book_info():
    book_code = input("Nhập mã sách: ").strip().upper()

    if not book_code:
        print("Mã sách không được để trống.")
        return

    book = get_book_info_by_code(book_code)

    if not book:
        print("Không tìm thấy sách.")
        return

    print("\n--- THÔNG TIN SÁCH ---")
    print(f"Mã sách        : {book.BookCode}")
    print(f"Tên sách       : {book.Title}")
    print(f"Tác giả        : {book.Author}")
    print(f"Thể loại       : {book.Category}")
    print(f"Nhà xuất bản   : {book.Publisher}")
    print(f"Năm xuất bản   : {book.PublishYear}")
    print(f"Trạng thái     : {book.BookStatus}")


def handle_view_book_status():
    print("1. Xem sách có sẵn")
    print("2. Xem sách đang được thuê")
    choice = input("Chọn chức năng: ").strip()

    if choice == "1":
        books = get_books_by_status_for_customer("Available")
        title = "DANH SÁCH SÁCH CÓ SẴN"
    elif choice == "2":
        books = get_books_by_status_for_customer("Rented")
        title = "DANH SÁCH SÁCH ĐANG ĐƯỢC THUÊ"
    else:
        print("Lựa chọn không hợp lệ.")
        return

    if not books:
        print("Không có dữ liệu.")
        return

    print(f"\n===== {title} =====")
    print_book_header()
    for book in books:
        print_book_row(book)
    print("-" * 110)


def handle_rent_books(user):
    raw_book_codes = input("Nhập danh sách mã sách, cách nhau bằng dấu phẩy: ").strip()
    expected_return_date = input("Nhập ngày dự kiến trả (YYYY-MM-DD): ").strip()

    if not raw_book_codes or not expected_return_date:
        print("Không được để trống thông tin bắt buộc.")
        return

    try:
        parsed_date = datetime.strptime(expected_return_date, "%Y-%m-%d")
        today = datetime.today().date()

        if parsed_date.date() < today:
            print("Ngày dự kiến trả không được nhỏ hơn ngày hiện tại.")
            return

        expected_return_str = parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        print("Ngày dự kiến trả không đúng định dạng YYYY-MM-DD.")
        return

    book_codes = [code.strip() for code in raw_book_codes.split(",") if code.strip()]

    success, message = create_rental_order_for_customer(
        customer_id=user.CustomerID,
        book_codes=book_codes,
        expected_return_date=expected_return_str,
    )
    print(message)


def handle_view_my_rented_books(user):
    rows = get_current_rented_books_by_customer(user.CustomerID)

    if not rows:
        print("Bạn hiện không có sách nào đang thuê.")
        return

    print("-" * 120)
    print(f"{'OrderCode':<12}{'RentDate':<22}{'ExpectedReturn':<22}{'BookCode':<10}{'Title':<30}{'Status':<12}")
    print("-" * 120)

    for row in rows:
        rent_date = str(row.RentDate)[:19] if row.RentDate else ""
        expected_return = str(row.ExpectedReturnDate)[:19] if row.ExpectedReturnDate else ""

        print(
            f"{row.OrderCode:<12}{rent_date:<22}{expected_return:<22}"
            f"{row.BookCode:<10}{row.Title:<30}{row.OrderStatus:<12}"
        )

    print("-" * 120)


def show_customer_menu(user):
    customer_name = user.FullName if hasattr(user, "FullName") and user.FullName else user.Username

    while True:
        print("\n================= MENU CUSTOMER =================")
        print(f"Xin chào Customer: {customer_name}")
        print("1. Tìm kiếm sách")
        print("2. Xem thông tin sách")
        print("3. Xem trạng thái sách")
        print("4. Chọn thuê sách")
        print("5. Xem sách mình đang thuê")
        print("0. Đăng xuất")
        print("=================================================")

        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            handle_search_books()
        elif choice == "2":
            handle_view_book_info()
        elif choice == "3":
            handle_view_book_status()
        elif choice == "4":
            handle_rent_books(user)
        elif choice == "5":
            handle_view_my_rented_books(user)
        elif choice == "0":
            print("Đăng xuất Customer thành công.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")