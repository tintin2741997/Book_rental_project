from menus.book_menu import show_book_menu
from menus.customer_manage_menu import show_customer_manage_menu
from menus.order_menu import show_order_menu
from menus.report_menu import show_report_menu


def show_admin_menu(user):
    while True:
        print("\n=================== MENU ADMIN ===================")
        print(f"Xin chào Admin: {user.Username}")
        print("1. Quản lý sách")
        print("2. Quản lý trạng thái sách")
        print("3. Quản lý khách hàng")
        print("4. Quản lý đơn thuê")
        print("5. Báo cáo")
        print("0. Đăng xuất")
        print("==================================================")

        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            show_book_menu()
        elif choice == "2":
            show_admin_menu()
        elif choice == "3":
            show_customer_manage_menu()
        elif choice == "4":
            show_order_menu()
        elif choice == "5":
            show_report_menu()
        elif choice == "0":
            print("Đăng xuất Admin thành công.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")