from services.customer_service import (
    get_all_customers,
    get_customer_by_code,
    search_customers,
    add_customer,
    update_customer,
    delete_customer,
    is_customer_code_exists,
)
def print_customer_header():
    print("-" * 120)
    print(f"{'ID':<5}{'Code':<12}{'Full Name':<25}{'Phone':<15}{'Address':<30}{'Email':<30}")
    print("-" * 120)

def print_customer_row(customer):
    print(
        f"{customer.CustomerID:<5}{customer.CustomerCode:<12}{customer.FullName:<25}"
        f"{(customer.Phone or ''):<15}{(customer.Address or ''):<30}{(customer.Email or ''):<30}"
    )

def show_all_customers():
    customers = get_all_customers()

    if not customers:
        return "Không có khách hàng nào trong hệ thống."
    
    print("\n===== DANH SÁCH KHÁCH HÀNG =====")
    print_customer_header()
    for customer in customers:
        print_customer_row(customer)
    print("-" * 120)

    def handel_add_customer():
        customer_code = input("Nhập mã khách hàng: ").strip()
        full_name = input("Nhập họ tên: ").strip()
        phone = input("Nhập số điện thoại: ").strip()
        address = input("Nhập địa chỉ: ").strip()
        email = input("Nhập email: ").strip()

        if not customer_code:
            return "Mã khách hàng và họ tên không được để trống."
        
        if is_customer_code_exists(customer_code):
            return "Mã khách hàng đã tồn tại."

        result = add_customer (
            customer_code = customer_code,
            full_name= full_name,
            phone = phone if phone else None,
            address= address if address else None,
            email= email if email else None,
        )
        
        if result:
            print("Thêm khách hàng thành công.")
        else:
            print("Thêm khách hàng thất bại.")

def handle_search_customer():
    keyword = input("Nhập từ khóa (mã khách hàng / họ tên / số điện thoại): ").strip()
    
    if not keyword:
        return "Từ khóa không được để trống."

    customers = search_customers(keyword) #customer la List chua cac customer co tu khoa

    if not customers: # Neu list la rong
        return "Không tìm thấy khách hàng phù hợp."
    
    print_customer_header()
    for i in customers:
        print_customer_row(customers)

def handle_update_customer():
    customer_code = input("Nhập mã khách hàng cần cập nhật thông tin: ")
    if not customer_code:
        return "Mã khách hàng trống, vui lòng nhập thông tin"
    
    customer = get_customer_by_code(customer_code)

    if not customer:
        return "không tin thấy khách hàng"
    
    print("Nhập thông tin khách hàng mới để dập nhật, bỏ trống thông tin nếu thông tin không có thay đổi.")

    new_full_name = input("Nhập họ và tên: ").strip()
    new_phone = input("Nhập số điện thoại: ").strip()
    new_address = input("Nhập địa chỉ: ").strip()
    new_email = input("Nhập email: ").strip()

    # Xu ly bo trong thong tin neu muon giu thong tin cu
    full_name = new_full_name if new_full_name else customer.FullName
    phone = new_phone if new_phone else customer.Phone
    address = new_address if new_address else customer.Address
    email = new_email if new_email else customer.Email

    result = update_customer(customer_code, full_name, phone, address, email)

    if result:
        return "Cập nhật thành công."
    else:
        return "Cập nhật thất bại"

def handle_delete_customer():
    customer_code = input("Nhập mã khách hàng muốn xóa: ")

    if not customer_code:
        return "Mã khách hàng trống, vui lòng nhập thông tin."
    
    delete_customer(customer_code)

def show_customer_manage_menu():
    while True:
        print("\n=============== QUẢN LÝ KHÁCH HÀNG ===============")
        print("1. Thêm khách hàng")
        print("2. Xem danh sách khách hàng")
        print("3. Tìm kiếm khách hàng")
        print("4. Cập nhật thông tin khách hàng")
        print("5. Xóa khách hàng")
        print("0. Quay lại")
        print("==================================================")

        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            add_customer()
        elif choice == "2":
            show_all_customers()
        elif choice == "3":
            search_customers()
        elif choice == "4":
            handle_update_customer()
        elif choice == "5":
            handle_delete_customer()
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

    





