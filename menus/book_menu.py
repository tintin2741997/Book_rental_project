from services.book_service import (
    get_all_books,
    get_book_by_code,
    search_books,
    add_book,
    update_book,
    delete_book,
    is_book_code_exists,
)

def print_book_header():
    print("-" * 110)
    # Canh le trai + các cột thẳng hàng
    print(f"{'ID':<5}{'Code':<10}{'Title':<30}{'Author':<20}{'Category':<15}{'Year':<8}{'Status':<12}")
    print("-" * 110)


def print_book_row(book):
    print(
        f"{book.BookID:<5}{book.BookCode:<10}{book.Title:<30}{book.Author:<20}"
        f"{(book.Category or ''):<15}{str(book.PublishYear or ''):<8}{book.BookStatus:<12}"
    )


def show_all_books():
    books = get_all_books()

    if not books:
        print("Không có sách nào trong hệ thống.")
        return

    print("\n===== DANH SÁCH =====")
    print_book_header()
    for book in books:
        print_book_row(book)
    print("-" * 110)


def handle_add_book():
    print("\n===== THÊM SÁCH =====")
    book_code = input("Nhập mã sách: ").strip()
    title = input("Nhập tên sách: ").strip()
    author = input("Nhập tác giả: ").strip()
    category = input("Nhập thể loại: ").strip()
    publisher = input("Nhập nhà xuất bản: ").strip()
    publish_year = input("Nhập năm xuất bản: ").strip()

    if not book_code or not title or not author:
        print("Mã sách, tên sách và tác giả không được để trống.")
        return

    if is_book_code_exists(book_code):
        print("Mã sách đã tồn tại.")
        return

    year_value = None
    if publish_year:
        if not publish_year.isdigit():
            print("Năm xuất bản phải là số nguyên.")
            return
        year_value = int(publish_year)

    result = add_book(
        book_code=book_code,
        title=title,
        author=author,
        category=category if category else None,
        publisher=publisher if publisher else None,
        publish_year=year_value,
        book_status="Available",
    )

    if result:
        print("Thêm sách thành công.")
    else:
        print("Thêm sách thất bại.")


def handle_search_books():
    print("\n===== TÌM KIẾM SÁCH =====")
    keyword = input("Nhập từ khóa (mã sách / tên sách / tác giả / thể loại): ").strip()

    if not keyword:
        print("Từ khóa không được để trống.")
        return

    books = search_books(keyword)

    if not books:
        print("Không tìm thấy sách phù hợp.")
        return

    print_book_header()
    for book in books:
        print_book_row(book)
    print("-" * 110)


def handle_update_book():
    print("\n===== CẬP NHẬT SÁCH =====")
    book_code = input("Nhập mã sách cần cập nhật: ").strip()

    if not book_code:
        print("Mã sách không được để trống.")
        return

    book = get_book_by_code(book_code)

    if not book:
        print("Không tìm thấy sách.")
        return

    print("Để trống nếu muốn giữ nguyên giá trị cũ.")

    new_title = input(f"Tên sách [{book.Title}]: ").strip()
    new_author = input(f"Tác giả [{book.Author}]: ").strip()
    new_category = input(f"Thể loại [{book.Category or ''}]: ").strip()
    new_publisher = input(f"Nhà xuất bản [{book.Publisher or ''}]: ").strip()
    new_publish_year = input(f"Năm xuất bản [{book.PublishYear or ''}]: ").strip()

    title = new_title if new_title else book.Title
    author = new_author if new_author else book.Author
    category = new_category if new_category else book.Category
    publisher = new_publisher if new_publisher else book.Publisher

    if new_publish_year:
        if not new_publish_year.isdigit():
            print("Năm xuất bản phải là số nguyên.")
            return
        publish_year = int(new_publish_year)
    else:
        publish_year = book.PublishYear

    result = update_book(book_code, title, author, category, publisher, publish_year)

    if result:
        print("Cập nhật sách thành công.")
    else:
        print("Cập nhật sách thất bại.")


def handle_delete_book():
    print("\n===== XÓA SÁCH =====")
    book_code = input("Nhập mã sách cần xóa: ").strip()

    if not book_code:
        print("Mã sách không được để trống.")
        return

    success, message = delete_book(book_code)
    print(message)


def show_book_menu():
    while True:
        print("\n================= QUẢN LÝ SÁCH =================")
        print("1. Thêm sách")
        print("2. Xem danh sách sách")
        print("3. Tìm kiếm sách")
        print("4. Cập nhật thông tin sách")
        print("5. Xóa sách")
        print("0. Quay lại")
        print("================================================")

        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            handle_add_book()
        elif choice == "2":
            show_all_books()
        elif choice == "3":
            handle_search_books()
        elif choice == "4":
            handle_update_book()
        elif choice == "5":
            handle_delete_book()
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")