"""
Test Automation cho Main Menu Functions
Kiểm tra các chức năng chính của ứng dụng
"""

import pytest
from datetime import datetime, timedelta
from services.book_service import get_all_books, get_book_by_code, search_books
from services.customer_service import get_all_customers, get_customer_by_code, search_customers
from services.order_service import (
    get_all_orders,
    get_order_by_code,
    get_order_details,
)


class TestBookService:
    """Test Case: Kiểm tra dịch vụ sách"""
    
    def test_get_all_books_returns_list(self):
        """Lấy tất cả sách phải trả về danh sách"""
        books = get_all_books()
        assert isinstance(books, list), "get_all_books() phải trả về list"
        print(f"✓ Tìm được {len(books)} sách")
    
    def test_get_book_by_code_valid(self):
        """Lấy sách theo mã hợp lệ"""
        book = get_book_by_code("B001")
        if book:
            assert book.BookID is not None
            print(f"✓ Tìm được sách B001: {book.Title}")
        else:
            print("⚠ Không có sách B001 trong DB")
    
    def test_search_books_returns_list(self):
        """Tìm kiếm sách phải trả về danh sách"""
        results = search_books("Python")
        assert isinstance(results, list), "search_books() phải trả về list"
        print(f"✓ Tìm được {len(results)} sách khi tìm 'Python'")


class TestCustomerService:
    """Test Case: Kiểm tra dịch vụ khách hàng"""
    
    def test_get_all_customers_returns_list(self):
        """Lấy tất cả khách hàng phải trả về danh sách"""
        customers = get_all_customers()
        assert isinstance(customers, list), "get_all_customers() phải trả về list"
        print(f"✓ Tìm được {len(customers)} khách hàng")
    
    def test_get_customer_by_code_valid(self):
        """Lấy khách hàng theo mã hợp lệ"""
        customer = get_customer_by_code("C001")
        if customer:
            assert customer.CustomerID is not None
            print(f"✓ Tìm được khách hàng C001: {customer.FullName}")
        else:
            print("⚠ Không có khách hàng C001 trong DB")
    
    def test_search_customers_returns_list(self):
        """Tìm kiếm khách hàng phải trả về danh sách"""
        results = search_customers("Nguyen")
        assert isinstance(results, list), "search_customers() phải trả về list"
        print(f"✓ Tìm được {len(results)} khách hàng khi tìm 'Nguyen'")


class TestOrderService:
    """Test Case: Kiểm tra dịch vụ đơn hàng"""
    
    def test_get_all_orders_returns_list(self):
        """Lấy tất cả đơn hàng phải trả về danh sách"""
        orders = get_all_orders()
        assert isinstance(orders, list), "get_all_orders() phải trả về list"
        print(f"✓ Tìm được {len(orders)} đơn hàng")
    
    def test_get_order_by_code_valid(self):
        """Lấy đơn hàng theo mã"""
        order = get_order_by_code("O001")
        if order:
            assert order.OrderID is not None
            print(f"✓ Tìm được đơn O001: {order.FullName}")
        else:
            print("⚠ Không có đơn O001 trong DB")
    
    def test_get_order_details_valid(self):
        """Lấy chi tiết sách trong đơn"""
        details = get_order_details("O001")
        assert isinstance(details, list), "get_order_details() phải trả về list"
        print(f"✓ Tìm được {len(details)} sách trong đơn O001")


class TestDataIntegrity:
    """Test Case: Kiểm tra tính toàn vẹn dữ liệu"""
    
    def test_book_status_valid_values(self):
        """Trạng thái sách phải là Available hoặc Rented"""
        books = get_all_books()
        valid_statuses = ["Available", "Rented"]
        
        for book in books:
            assert book.BookStatus in valid_statuses, \
                f"Sách {book.BookCode} có status không hợp lệ: {book.BookStatus}"
        
        print(f"✓ Tất cả {len(books)} sách có status hợp lệ")
    
    def test_order_status_valid_values(self):
        """Trạng thái đơn phải là Renting hoặc Returned"""
        orders = get_all_orders()
        valid_statuses = ["Renting", "Returned"]
        
        for order in orders:
            assert order.OrderStatus in valid_statuses, \
                f"Đơn {order.OrderCode} có status không hợp lệ: {order.OrderStatus}"
        
        print(f"✓ Tất cả {len(orders)} đơn có status hợp lệ")
    
    def test_order_date_consistency(self):
        """Ngày dự kiến trả >= ngày thuê"""
        orders = get_all_orders()
        
        for order in orders:
            if order.RentDate and order.ExpectedReturnDate:
                assert order.RentDate <= order.ExpectedReturnDate, \
                    f"Đơn {order.OrderCode}: ngày trả < ngày thuê"
        
        print(f"✓ Tất cả {len(orders)} đơn có ngày hợp lệ")


class TestEdgeCases:
    """Test Case: Kiểm tra các trường hợp đặc biệt"""
    
    def test_empty_search_results(self):
        """Tìm với mã không tồn tại"""
        book = get_book_by_code("INVALID_9999")
        assert book is None, "Tìm sách không tồn tại phải trả về None"
        print("✓ Tìm kiếm không tồn tại xử lý đúng")
    
    def test_special_characters_in_names(self):
        """Tên chứa ký tự đặc biệt"""
        customers = get_all_customers()
        for customer in customers:
            # Kiểm tra tên không trống
            assert customer.FullName and len(customer.FullName) > 0
        print(f"✓ Kiểm tra {len(customers)} tên khách hàng")


# ============== CHẠY TEST ==============
def run_menu_tests():
    """Chạy tất cả test cho menu"""
    print("\n" + "="*70)
    print("TEST AUTOMATION CHO MAIN MENU - BOOK RENTAL PROJECT")
    print("="*70)
    
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_menu_tests()
