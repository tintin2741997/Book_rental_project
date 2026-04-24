from services.auth_service import login_by_role
from menus.admin_menu import show_admin_menu
from menus.customer_menu import show_customer_menu

def input_credentials():
    username = input("User Name: ").strip()
    password = input("Password: ").strip()

    if not username or not password:
        print("Username và Password không được để trống.")
        return None, None

    return username, password
def handle_admin_login():
    print("\n========== ĐĂNG NHẬP ==========")
    
    username, password = input_credentials()
    if not username or not password:
        return

    user = login_by_role(username, password, "Admin")

    if user:
        print("Đăng nhập thành công.")
        print("Xin chào Admin")
        show_admin_menu(user)
    else:
        print("Sai username hoặc password, xin vui lòng kiểm tra lại.")

def handle_customer_login():
    print("\n========= ĐĂNG NHẬP =========")

    username, password = input_credentials()
    if not username or not password:
        return

    user = login_by_role(username, password, "Customer")

    if user:
        print("Đăng nhập thành công.")
        show_customer_menu(user)
    else:
        print("Sai username hoặc password, xin vui lòng kiểm tra lại.")


def show_main_menu():
    while True:
        print("\n================ BOOK RENTAL STORE ================")
        print("1. Đăng nhập dành cho Admin")
        print("2. Đăng nhập dành cho Khách Hàng")
        print("0. Thoát")
        print("===================================================")

        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            handle_admin_login()
        elif choice == "2":
            handle_customer_login()
        elif choice == "0":
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")