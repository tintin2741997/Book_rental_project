from services.report_service import (
    count_rented_books,
    count_available_books,
    get_rental_count_by_book,
    get_books_by_status,
)


def show_total_rented_books():
    result = count_rented_books()
    total = result.TotalRented if result else 0

    print("\n===== THỐNG KÊ SÁCH ĐANG ĐƯỢC THUÊ =====")
    print(f"Tổng số sách đang được thuê: {total}")

    books = get_books_by_status("Rented")
    if books:
        print("\nDanh sách sách đang được thuê:")
        print("-" * 100)
        print(f"{'ID':<5}{'Code':<10}{'Title':<30}{'Author':<20}{'Category':<15}{'Status':<10}")
        print("-" * 100)
        for book in books:
            print(
                f"{book.BookID:<5}{book.BookCode:<10}{book.Title:<30}{book.Author:<20}"
                f"{(book.Category or ''):<15}{book.BookStatus:<10}"
            )
        print("-" * 100)


def show_total_available_books():
    result = count_available_books()
    total = result.TotalAvailable if result else 0

    print("\n===== THỐNG KÊ SÁCH CÓ SẴN =====")
    print(f"Tổng số sách có sẵn: {total}")

    books = get_books_by_status("Available")
    if books:
        print("\nDanh sách sách có sẵn:")
        print("-" * 100)
        print(f"{'ID':<5}{'Code':<10}{'Title':<30}{'Author':<20}{'Category':<15}{'Status':<10}")
        print("-" * 100)
        for book in books:
            print(
                f"{book.BookID:<5}{book.BookCode:<10}{book.Title:<30}{book.Author:<20}"
                f"{(book.Category or ''):<15}{book.BookStatus:<10}"
            )
        print("-" * 100)


def show_rental_count_by_book():
    rows = get_rental_count_by_book()

    print("\n===== THỐNG KÊ SỐ LƯỢT THUÊ THEO SÁCH =====")

    if not rows:
        print("Không có dữ liệu thống kê.")
        return

    print("-" * 90)
    print(f"{'BookCode':<12}{'Title':<35}{'Author':<25}{'RentalCount':<12}")
    print("-" * 90)

    for row in rows:
        print(f"{row.BookCode:<12}{row.Title:<35}{row.Author:<25}{row.RentalCount:<12}")

    print("-" * 90)


def show_report_menu():
    while True:
        print("\n==================== BÁO CÁO ====================")
        print("1. Thống kê sách đang được thuê")
        print("2. Thống kê sách có sẵn")
        print("3. Thống kê số lượt thuê theo sách")
        print("0. Quay lại")
        print("=================================================")

        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            show_total_rented_books()
        elif choice == "2":
            show_total_available_books()
        elif choice == "3":
            show_rental_count_by_book()
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")