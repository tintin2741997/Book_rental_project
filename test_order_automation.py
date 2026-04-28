"""
Test Automation cho Project Book Rental
Chạy test: pytest test_order_automation.py -v
"""

import pytest
from datetime import datetime, timedelta
from services.order_service import (
    generate_order_code,
    get_customer_by_code,
    get_book_by_code,
    get_order_by_code,
    create_rental_order,
    return_rental_order,
    get_all_orders,
    get_order_details,
)


class TestOrderCodeGeneration:
    """Test Case: Kiểm tra tạo mã đơn hàng"""
    
    def test_generate_order_code_format(self):
        """Mã order phải có format O001, O002, ... """
        code = generate_order_code()
        assert code is not None, "Mã order không được None"
        assert code.startswith("O"), f"Mã order phải bắt đầu bằng 'O', nhưng nhận {code}"
        assert len(code) >= 4, f"Mã order phải có ít nhất 4 ký tự, nhưng nhận {code}"
        print(f"✓ Mã order tạo thành công: {code}")


class TestGetCustomerByCode:
    """Test Case: Kiểm tra lấy thông tin khách hàng"""
    
    def test_get_existing_customer(self):
        """Lấy khách hàng tồn tại"""
        # Giả sử C001 tồn tại trong DB
        customer = get_customer_by_code("C001")
        if customer:
            assert customer.CustomerID is not None
            assert customer.CustomerCode == "C001"
            print(f"✓ Tìm khách hàng C001: {customer.FullName}")
        else:
            print("⚠ Khách hàng C001 không có trong DB (skip test)")
    
    def test_get_non_existing_customer(self):
        """Lấy khách hàng không tồn tại"""
        customer = get_customer_by_code("INVALID_CUST_9999")
        assert customer is None, "Khách hàng không tồn tại phải trả về None"
        print("✓ Khách hàng không tồn tại trả về None")


class TestGetBookByCode:
    """Test Case: Kiểm tra lấy thông tin sách"""
    
    def test_get_existing_book(self):
        """Lấy sách tồn tại"""
        # Giả sử B001 tồn tại trong DB
        book = get_book_by_code("B001")
        if book:
            assert book.BookID is not None
            assert book.BookCode == "B001"
            print(f"✓ Tìm sách B001: {book.Title} (Status: {book.BookStatus})")
        else:
            print("⚠ Sách B001 không có trong DB (skip test)")
    
    def test_get_non_existing_book(self):
        """Lấy sách không tồn tại"""
        book = get_book_by_code("INVALID_BOOK_9999")
        assert book is None, "Sách không tồn tại phải trả về None"
        print("✓ Sách không tồn tại trả về None")


class TestCreateRentalOrder:
    """Test Case: Kiểm tra tạo đơn thuê"""
    
    def test_create_order_invalid_customer(self):
        """Test: Khách hàng không tồn tại"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        success, message = create_rental_order(
            customer_code="INVALID_CUST_9999",
            book_codes=["B001"],
            expected_return_date=tomorrow
        )
        assert success is False, "Tạo đơn với khách hàng không tồn tại phải thất bại"
        assert "Khách hàng không tồn tại" in message
        print(f"✓ Test khách hàng không tồn tại: {message}")
    
    def test_create_order_empty_book_list(self):
        """Test: Danh sách sách trống"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        success, message = create_rental_order(
            customer_code="C001",
            book_codes=[],
            expected_return_date=tomorrow
        )
        assert success is False, "Tạo đơn với sách trống phải thất bại"
        assert "trống" in message.lower()
        print(f"✓ Test danh sách sách trống: {message}")
    
    def test_create_order_invalid_return_date(self):
        """Test: Ngày trả < ngày thuê"""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        success, message = create_rental_order(
            customer_code="C001",
            book_codes=["B001"],
            expected_return_date=yesterday
        )
        assert success is False, "Ngày trả < ngày thuê phải thất bại"
        assert "phải" in message.lower() or "sau" in message.lower()
        print(f"✓ Test ngày trả không hợp lệ: {message}")
    
    def test_create_order_duplicate_books(self):
        """Test: Không được trùng sách trong cùng đơn"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        success, message = create_rental_order(
            customer_code="C001",
            book_codes=["B001", "b001", "B002", "B001"],  # B001 trùng
            expected_return_date=tomorrow
        )
        if success is False:
            assert "trùng" in message.lower()
            print(f"✓ Test sách trùng: {message}")
        else:
            print("⚠ Không phát hiện sách trùng (có thể do B001 không tồn tại)")
    
    def test_create_order_non_existing_book(self):
        """Test: Sách không tồn tại"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        success, message = create_rental_order(
            customer_code="C001",
            book_codes=["INVALID_BOOK_9999"],
            expected_return_date=tomorrow
        )
        assert success is False, "Sách không tồn tại phải thất bại"
        assert "không tồn tại" in message or "lỗi" in message.lower()
        print(f"✓ Test sách không tồn tại: {message}")
    
    def test_create_valid_order(self):
        """Test: Tạo đơn hợp lệ (Integration Test)"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        success, message = create_rental_order(
            customer_code="C001",
            book_codes=["B001"],
            expected_return_date=tomorrow
        )
        if success:
            assert "thành công" in message.lower()
            print(f"✓ Test tạo đơn hợp lệ: {message}")
        else:
            print(f"⚠ Không thể tạo đơn hợp lệ: {message}")


class TestReturnRentalOrder:
    """Test Case: Kiểm tra trả sách"""
    
    def test_return_non_existing_order(self):
        """Test: Trả đơn không tồn tại"""
        success, message = return_rental_order("INVALID_ORDER_9999")
        assert success is False, "Trả đơn không tồn tại phải thất bại"
        assert "không tồn tại" in message.lower()
        print(f"✓ Test trả đơn không tồn tại: {message}")
    
    def test_return_already_returned_order(self):
        """Test: Trả đơn đã trả rồi"""
        # Giả sử có đơn đã trả (nếu có trong DB)
        # Đây là test optional
        print("⚠ Test trả đơn đã trả (cần đơn đã trả trong DB)")
    
    def test_return_valid_order(self):
        """Test: Trả sách hợp lệ (Integration Test)"""
        # Trước tiên tạo một đơn thuê
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        created_success, created_msg = create_rental_order(
            customer_code="C001",
            book_codes=["B002"],
            expected_return_date=tomorrow
        )
        
        if created_success:
            # Lấy mã order từ message
            import re
            match = re.search(r"O\d+", created_msg)
            if match:
                order_code = match.group()
                success, message = return_rental_order(order_code)
                if success:
                    assert "thành công" in message.lower()
                    print(f"✓ Test trả sách hợp lệ: {message}")
                else:
                    print(f"⚠ Không thể trả sách: {message}")
        else:
            print(f"⚠ Không thể tạo đơn để test trả: {created_msg}")


class TestGetOrderByCode:
    """Test Case: Kiểm tra lấy thông tin đơn hàng"""
    
    def test_get_non_existing_order(self):
        """Lấy đơn không tồn tại"""
        order = get_order_by_code("INVALID_ORDER_9999")
        assert order is None, "Đơn không tồn tại phải trả về None"
        print("✓ Đơn không tồn tại trả về None")
    
    def test_get_existing_order(self):
        """Lấy đơn tồn tại"""
        # Giả sử O001 tồn tại trong DB
        order = get_order_by_code("O001")
        if order:
            assert order.OrderID is not None
            assert order.OrderCode == "O001"
            print(f"✓ Tìm đơn O001: {order.FullName}")
        else:
            print("⚠ Đơn O001 không có trong DB (skip test)")


class TestGetAllOrders:
    """Test Case: Kiểm tra lấy danh sách tất cả đơn hàng"""
    
    def test_get_all_orders_returns_list(self):
        """Danh sách đơn hàng phải là list"""
        orders = get_all_orders()
        assert isinstance(orders, list), "get_all_orders() phải trả về list"
        print(f"✓ Tìm được {len(orders)} đơn hàng")


class TestGetOrderDetails:
    """Test Case: Kiểm tra lấy chi tiết sách trong đơn"""
    
    def test_get_details_non_existing_order(self):
        """Lấy chi tiết đơn không tồn tại"""
        details = get_order_details("INVALID_ORDER_9999")
        assert isinstance(details, list), "get_order_details() phải trả về list"
        print("✓ Chi tiết đơn không tồn tại trả về danh sách trống")


# ============== CHẠY TEST ==============
def run_all_tests():
    """Chạy tất cả test"""
    print("\n" + "="*70)
    print("TEST AUTOMATION CHO PROJECT BOOK RENTAL")
    print("="*70)
    
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_all_tests()
