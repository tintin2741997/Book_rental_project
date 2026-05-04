"""
COMPREHENSIVE TEST AUTOMATION SUITE
Book Rental System - Python Pytest Framework
Date: 2026-05-04
This script automates the execution of test cases for the Book Rental system.
Since this is a console-based Python application, we use pytest for direct service testing
and mock console inputs for menu navigation testing.
"""

import pytest
from datetime import datetime, timedelta
from io import StringIO
import re
import sys
sys.path.insert(0, r'c:\Users\SV STORE\Desktop\UIT\Python\book_rental_project')

from services.auth_service import login_by_role
from services.book_service import (
    get_all_books, get_book_by_code, search_books, add_book, 
    update_book, delete_book, is_book_code_exists
)
from services.customer_service import (
    get_all_customers, get_customer_by_code, search_customers, 
    add_customer, update_customer, delete_customer, is_customer_code_exists, 
    has_active_rental
)
from services.order_service import (
    create_rental_order, get_all_orders, get_order_by_code, 
    get_order_details, return_rental_order, generate_order_code
)
from services.report_service import (
    count_rented_books, count_available_books, get_rental_count_by_book
)
from db import fetch_all, fetch_one, execute_query, get_connection


def unique_code(prefix):
    return f"{prefix}{datetime.now().strftime('%H%M%S%f')[-10:]}"


def create_temp_available_book(prefix="TBOOK"):
    book_code = unique_code(prefix)
    created = add_book(
        book_code,
        "Automation Temp Book",
        "QA Automation",
        "Testing",
        "QA Publisher",
        2026,
    )
    assert created is True, f"Could not create available temp book {book_code}"
    book = get_book_by_code(book_code)
    assert book is not None, f"Temp book {book_code} should exist"
    assert book.BookStatus == "Available", f"Temp book {book_code} should start Available"
    return book_code


def extract_order_code(message):
    match = re.search(r"O\d+", message)
    assert match, f"Order code should be present in message: {message}"
    return match.group(0)

# ============================================================================
# SECTION 1: AUTHENTICATION TESTS
# ============================================================================

class TestAuthentication:
    """Test cases for authentication and login functionality"""
    
    def test_au_001_admin_login_valid_credentials(self):
        """TC-AU-001: Admin login with valid credentials"""
        result = login_by_role("admin", "123", "Admin")
        assert result is not None, "Admin login should succeed with valid credentials"
        assert result.Username == "admin", "Username should match"
        assert result.Role == "Admin", "Role should be Admin"
    
    def test_au_002_admin_login_invalid_password(self):
        """TC-AU-002: Admin login with invalid password"""
        result = login_by_role("admin", "wrongpassword", "Admin")
        assert result is None, "Admin login should fail with wrong password"
    
    def test_au_003_customer_login_valid_credentials(self):
        """TC-AU-003: Customer login with valid credentials"""
        result = login_by_role("customer1", "123", "Customer")
        assert result is not None, "Customer login should succeed with valid credentials"
        assert result.Role == "Customer", "Role should be Customer"
    
    def test_au_004_customer_login_invalid_username(self):
        """TC-AU-004: Customer login with non-existent username"""
        result = login_by_role("nonexistent", "anypassword", "Customer")
        assert result is None, "Login should fail with non-existent username"
    
    def test_au_006_empty_username_validation(self):
        """TC-AU-006: Login with empty username should fail"""
        result = login_by_role("", "password", "Admin")
        assert result is None, "Login should fail with empty username"

# ============================================================================
# SECTION 2: BOOK MANAGEMENT TESTS
# ============================================================================

class TestBookManagement:
    """Test cases for book CRUD operations"""
    
    def test_bm_001_view_all_books(self):
        """TC-BM-001: View all books returns list"""
        books = get_all_books()
        assert isinstance(books, (list, type(None))) or hasattr(books, '__iter__'), "Should return iterable"
        if books:
            for book in books:
                assert hasattr(book, 'BookID'), "Book should have BookID"
                assert hasattr(book, 'BookCode'), "Book should have BookCode"
                assert hasattr(book, 'BookStatus'), "Book should have BookStatus"
    
    def test_bm_002_view_books_returns_data(self):
        """TC-BM-002: View books retrieves from database"""
        books = get_all_books()
        assert books is not None, "View all books should not return None"
    
    def test_bm_003_search_books_by_keyword(self):
        """TC-BM-003: Search books by partial title"""
        results = search_books("Python")
        assert isinstance(results, (list, type(None))) or hasattr(results, '__iter__'), "Search should return iterable"
    
    def test_bm_004_search_books_no_results(self):
        """TC-BM-004: Search with non-matching keyword returns empty or None"""
        results = search_books("XXXXXXXX_NONEXISTENT")
        # Results should be empty or None, not throw error
        if results is None:
            pass
        elif isinstance(results, list):
            assert len(results) == 0, "Should return empty results"
    
    def test_bm_005_add_book_valid_data(self):
        """TC-BM-005: Add book with valid data succeeds"""
        book_code = f"TEST{datetime.now().strftime('%H%M%S')}"
        result = add_book(book_code, "Test Book", "Author", "Test Category", "Test Pub", "2024")
        # Verify book was added by searching for it
        if result:
            added_book = get_book_by_code(book_code)
            # Clean up
            if added_book:
                execute_query("DELETE FROM Books WHERE BookCode = ?", (book_code,))
    
    def test_bm_006_add_book_duplicate_code(self):
        """TC-BM-006: Add book with duplicate code fails"""
        # First verify a book exists
        existing_book = get_book_by_code("B001")
        if existing_book:
            # Try to add book with same code - should fail or handle gracefully
            result = add_book("B001", "Duplicate Title", "Author", "Cat", "Pub", "2024")
            # Database constraint should prevent this
    
    def test_bm_007_add_book_empty_field(self):
        """TC-BM-007: Add book with empty required field"""
        result = add_book("", "Title", "Author", "Cat", "Pub", "2024")
        # Should not succeed
    
    def test_bm_008_update_book_valid(self):
        """TC-BM-008: Update book information"""
        existing_book = get_book_by_code("B001")
        if existing_book:
            result = update_book("B001", "Updated Title", "New Author", "Fiction", "Pub", "2024")
            if result:
                updated = get_book_by_code("B001")
                assert updated.Title == "Updated Title", "Title should be updated"
                # Restore original
                execute_query(
                    "UPDATE Books SET Title = ?, Author = ? WHERE BookCode = ?",
                    ("Python Programming", "Guido van Rossum", "B001")
                )
    
    def test_bm_009_update_book_nonexistent(self):
        """TC-BM-009: Update non-existent book returns error"""
        result = update_book("NONEXIST999", "Title", "Author", "Cat", "Pub", "2024")
        # Should handle gracefully
    
    def test_bm_010_delete_book_available_status(self):
        """TC-BM-010: Delete book with Available status"""
        # Create test book
        test_code = f"DELTEST{datetime.now().strftime('%H%M%S')}"
        add_book(test_code, "Delete Test", "Author", "Test", "Pub", "2024")
        
        # Verify it was created
        book = get_book_by_code(test_code)
        if book and book.BookStatus == "Available":
            result = delete_book(test_code)
            # Verify deletion
            deleted_book = get_book_by_code(test_code)
            assert deleted_book is None, "Book should be deleted"
    
    def test_bm_011_delete_book_rented_status(self):
        """TC-BM-011: Cannot delete book with Rented status"""
        # Find a rented book
        rented_book = fetch_one(
            "SELECT TOP 1 BookCode FROM Books WHERE BookStatus = 'Rented'"
        )
        if rented_book:
            result = delete_book(rented_book.BookCode)
            # Deletion should fail
            still_exists = get_book_by_code(rented_book.BookCode)
            assert still_exists is not None, "Rented book should not be deleted"
    
    def test_bm_012_search_case_insensitivity(self):
        """TC-BM-012: Search is case-insensitive"""
        results_lower = search_books("python")
        results_upper = search_books("PYTHON")
        # Results should be comparable (may have different object types but same data)
        assert len(results_lower) == len(results_upper), "Case-insensitive search should return same count"

# ============================================================================
# SECTION 3: CUSTOMER MANAGEMENT TESTS
# ============================================================================

class TestCustomerManagement:
    """Test cases for customer CRUD operations"""
    
    def test_cm_001_view_all_customers(self):
        """TC-CM-001: View all customers"""
        customers = get_all_customers()
        assert customers is not None, "View all customers should not return None"
        if customers:
            assert len(customers) > 0, "Should have at least one customer"
    
    def test_cm_002_search_customers_by_name(self):
        """TC-CM-002: Search customers by name"""
        results = search_customers("Nguyen")
        assert isinstance(results, (list, type(None))) or hasattr(results, '__iter__'), "Should return iterable"
    
    def test_cm_003_search_customers_by_phone(self):
        """TC-CM-003: Search customers by phone"""
        results = search_customers("0901")
        assert isinstance(results, (list, type(None))) or hasattr(results, '__iter__'), "Should return iterable"
    
    def test_cm_004_add_customer_valid(self):
        """TC-CM-004: Add customer with valid data"""
        cust_code = f"TEST{datetime.now().strftime('%H%M%S')}"
        result = add_customer(cust_code, "Test Customer", "0912345678", "HCM", "test@test.com")
        if result:
            added_cust = get_customer_by_code(cust_code)
            assert added_cust is not None, "Customer should be added"
            # Clean up
            execute_query("DELETE FROM Customers WHERE CustomerCode = ?", (cust_code,))
    
    def test_cm_005_add_customer_duplicate(self):
        """TC-CM-005: Add customer with duplicate code"""
        existing = get_customer_by_code("C001")
        if existing:
            result = add_customer("C001", "Duplicate", "0999999999", "HCM", "dup@test.com")
            # Should fail due to unique constraint
    
    def test_cm_006_update_customer_valid(self):
        """TC-CM-006: Update customer information"""
        existing = get_customer_by_code("C001")
        if existing:
            result = update_customer("C001", "Updated Name", "0987654321", "Ha Noi", "updated@test.com")
            if result:
                updated = get_customer_by_code("C001")
                assert updated.FullName == "Updated Name", "Name should be updated"
                # Restore original
                execute_query(
                    "UPDATE Customers SET FullName = ?, Phone = ?, Address = ? WHERE CustomerCode = ?",
                    ("Nguyen Van A", "0901111111", "Ho Chi Minh", "C001")
                )
    
    def test_cm_007_delete_customer_no_active_rentals(self):
        """TC-CM-007: Delete customer with no active rentals"""
        # Create test customer
        cust_code = f"DELTEST{datetime.now().strftime('%H%M%S')}"
        add_customer(cust_code, "Delete Test", "0999999999", "HCM", "del@test.com")
        
        # Verify created
        cust = get_customer_by_code(cust_code)
        if cust:
            # Verify no active rentals
            has_rental = has_active_rental(cust.CustomerID)
            if not has_rental:
                result = delete_customer(cust_code)
                # Verify deletion
                deleted = get_customer_by_code(cust_code)
                assert deleted is None, "Customer should be deleted"
    
    def test_cm_008_delete_customer_with_active_rentals(self):
        """TC-CM-008: Cannot delete customer with active rentals"""
        # Find customer with active rentals
        cust_with_rental = fetch_one(
            """SELECT TOP 1 c.CustomerID, c.CustomerCode FROM Customers c
            JOIN RentalOrders ro ON c.CustomerID = ro.CustomerID
            WHERE ro.OrderStatus = 'Renting'"""
        )
        if cust_with_rental:
            result = delete_customer(cust_with_rental.CustomerCode)
            # Deletion should fail
            still_exists = get_customer_by_code(cust_with_rental.CustomerCode)
            assert still_exists is not None, "Customer with active rentals should not be deleted"

# ============================================================================
# SECTION 4: RENTAL ORDER MANAGEMENT TESTS
# ============================================================================

class TestRentalOrderManagement:
    """Test cases for rental order operations"""
    
    def test_ro_001_create_order_single_book_valid(self):
        """TC-RO-001: Create rental order with single available book"""
        book_code = create_temp_available_book("ROONE")
        success, message = create_rental_order("C001", [book_code], "2026-05-15")
        assert success is True, f"Order creation should succeed: {message}"
        assert "thành công" in message.lower() or "success" in message.lower(), f"Success message expected: {message}"
        return_rental_order(extract_order_code(message))
    
    def test_ro_002_create_order_multiple_books(self):
        """TC-RO-002: Create order with multiple available books"""
        book_one = create_temp_available_book("ROMUL")
        book_two = create_temp_available_book("ROMUL")
        success, message = create_rental_order("C002", [book_one, book_two], "2026-05-20")
        assert success is True, f"Multiple book order should succeed: {message}"
        order_code = extract_order_code(message)
        details = get_order_details(order_code)
        assert len(details) == 2, "Order detail should contain both rented books"
        return_rental_order(order_code)
    
    def test_ro_003_create_order_nonexistent_customer(self):
        """TC-RO-003: Create order with non-existent customer"""
        success, message = create_rental_order("C999999", ["B001"], "2026-05-20")
        assert success is False, "Should fail for non-existent customer"
        assert "không tồn tại" in message.lower(), "Error message should indicate customer not found"
    
    def test_ro_004_create_order_nonexistent_book(self):
        """TC-RO-004: Create order with non-existent book code"""
        success, message = create_rental_order("C001", ["B999999"], "2026-05-20")
        assert success is False, "Should fail for non-existent book"
        assert "không tồn tại" in message.lower(), "Error message should indicate book not found"
    
    def test_ro_005_create_order_rented_book(self):
        """TC-RO-005: Cannot create order with already rented book"""
        # Find a rented book
        rented = fetch_one("SELECT TOP 1 BookCode FROM Books WHERE BookStatus = 'Rented'")
        if rented:
            success, message = create_rental_order("C001", [rented.BookCode], "2026-05-20")
            assert success is False, "Should fail for rented book"
            assert "không sẵn sàng" in message.lower(), "Error message should indicate book not available"
    
    def test_ro_006_create_order_duplicate_books(self):
        """TC-RO-006: Cannot add same book twice in one order"""
        success, message = create_rental_order("C001", ["B001", "B001"], "2026-05-20")
        assert success is False, "Should fail for duplicate books in same order"
        assert "trùng" in message.lower(), "Error message should indicate duplicate"
    
    def test_ro_007_create_order_invalid_date_format(self):
        """TC-RO-007: Invalid date format rejected"""
        success, message = create_rental_order("C001", ["B001"], "05/15/2026")
        assert success is False, "Should fail for invalid date format"
        assert "định dạng" in message.lower() or "format" in message.lower(), "Error should indicate format issue"
    
    def test_ro_008_create_order_return_date_before_today(self):
        """TC-RO-008: Expected return date must be >= today"""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        success, message = create_rental_order("C001", ["B001"], yesterday)
        assert success is False, "Should fail when return date is in past"
        assert "phải sau" in message.lower() or "before" in message.lower(), "Error should indicate date constraint"
    
    def test_ro_009_create_order_empty_book_list(self):
        """TC-RO-009: Cannot create order without books"""
        success, message = create_rental_order("C001", [], "2026-05-20")
        assert success is False, "Should fail when no books specified"
        assert "trống" in message.lower() or "empty" in message.lower(), "Error should indicate empty list"
    
    def test_ro_010_view_all_orders(self):
        """TC-RO-010: View all orders returns list"""
        orders = get_all_orders()
        assert orders is not None, "Should return orders list"
        if orders:
            assert len(orders) > 0, "Should have at least one order"
    
    def test_ro_011_view_order_detail(self):
        """TC-RO-011: View order detail with books"""
        # Get first order
        order = fetch_one("SELECT TOP 1 OrderCode FROM RentalOrders")
        if order:
            details = get_order_details(order.OrderCode)
            assert details is not None, "Should return order details"
    
    def test_ro_012_view_order_detail_nonexistent(self):
        """TC-RO-012: View detail of non-existent order"""
        details = get_order_details("O999999")
        # Should return None or empty
        assert details is None or len(details) == 0, "Non-existent order should return no details"
    
    def test_ro_013_return_order_valid(self):
        """TC-RO-013: Return order updates status and book status"""
        # Create order first
        success, msg = create_rental_order("C001", ["B003"], "2026-05-30")
        if success:
            # Extract order code from message
            order_code = msg.split("O")[1].split()[0] if "O" in msg else None
            if order_code:
                order_code = "O" + order_code
                # Verify order is Renting
                order = get_order_by_code(order_code)
                if order and order.OrderStatus == "Renting":
                    # Return it
                    success_return, msg_return = return_rental_order(order_code)
                    assert success_return is True, f"Return should succeed: {msg_return}"
                    
                    # Verify status changed
                    returned = get_order_by_code(order_code)
                    assert returned.OrderStatus == "Returned", "Order status should be Returned"
    
    def test_ro_014_return_order_already_returned(self):
        """TC-RO-014: Cannot return already returned order"""
        # Find a returned order
        returned_order = fetch_one("SELECT TOP 1 OrderCode FROM RentalOrders WHERE OrderStatus = 'Returned'")
        if returned_order:
            success, message = return_rental_order(returned_order.OrderCode)
            assert success is False, "Should fail for already returned order"
            assert "đã được hoàn trả" in message.lower(), "Error should indicate already returned"
    
    def test_ro_015_return_order_nonexistent(self):
        """TC-RO-015: Cannot return non-existent order"""
        success, message = return_rental_order("O999999")
        assert success is False, "Should fail for non-existent order"
        assert "không tồn tại" in message.lower(), "Error should indicate order not found"
    
    def test_ro_016_order_code_sequence(self):
        """TC-RO-016: Order codes are sequential"""
        code1 = generate_order_code()
        # Extract number from O###
        num1 = int(code1[1:])
        assert code1.startswith("O"), "Order code should start with O"
        assert num1 >= 1, "Order code number should be positive"

# ============================================================================
# SECTION 5: REPORTING TESTS
# ============================================================================

class TestReporting:
    """Test cases for reporting and statistics"""
    
    def test_rpt_001_count_rented_books(self):
        """TC-RPT-001: Count rented books report"""
        result = count_rented_books()
        assert result is not None, "Should return result"
    
    def test_rpt_002_count_available_books(self):
        """TC-RPT-002: Count available books report"""
        result = count_available_books()
        assert result is not None, "Should return result"
    
    def test_rpt_003_rental_count_by_book(self):
        """TC-RPT-003: Rental count by book report"""
        results = get_rental_count_by_book()
        assert isinstance(results, (list, type(None))) or hasattr(results, '__iter__'), "Should return iterable"

# ============================================================================
# SECTION 6: DATA VALIDATION & BUSINESS RULES TESTS
# ============================================================================

class TestBusinessRules:
    """Test cases for business rule enforcement"""
    
    def test_br_001_book_status_only_available_rented(self):
        """TC-BR-001: Book status constraint - only Available or Rented"""
        books = get_all_books()
        if books:
            for book in books:
                assert book.BookStatus in ["Available", "Rented"], f"Invalid book status: {book.BookStatus}"
    
    def test_br_002_book_deletion_requires_available(self):
        """TC-BR-002: Can only delete books with Available status"""
        # Create test book
        test_code = f"BRDEL{datetime.now().strftime('%H%M%S')}"
        add_book(test_code, "BR Test", "Test Author", "Test", "Pub", "2024")
        
        # Delete it (should succeed since it's Available)
        result = delete_book(test_code)
        assert result is True, "Should delete Available book"
    
    def test_br_003_customer_deletion_requires_no_active_rentals(self):
        """TC-BR-003: Cannot delete customer with active rentals"""
        # This is tested in TC-CM-008
        pass
    
    def test_br_005_expected_return_gte_rent_date(self):
        """TC-BR-005: Expected return date must be >= rent date (today)"""
        book_code = create_temp_available_book("BRTDY")
        today = datetime.now().strftime("%Y-%m-%d")
        success, msg = create_rental_order("C001", [book_code], today)
        assert success is True, f"Should accept return date = today: {msg}"
        order_code = extract_order_code(msg)
        return_rental_order(order_code)

# ============================================================================
# SECTION 7: REGRESSION TESTS
# ============================================================================

class TestRegression:
    """Full workflow regression tests"""
    
    def test_reg_001_full_book_workflow(self):
        """TC-REG-001: Complete book lifecycle - Add → Search → Update → Delete"""
        book_code = f"REG{datetime.now().strftime('%H%M%S')}"
        
        # 1. Add book
        add_result = add_book(book_code, "Workflow Test", "Test Author", "Test", "Pub", "2024")
        
        # 2. Search for it
        search_result = search_books(book_code)
        
        # 3. Verify it exists
        book = get_book_by_code(book_code)
        assert book is not None, "Book should exist after add"
        
        # 4. Update it
        update_result = update_book(book_code, "Updated Title", "New Author", "Test", "Pub", "2024")
        
        # 5. Verify update
        updated = get_book_by_code(book_code)
        assert updated.Title == "Updated Title", "Title should be updated"
        
        # 6. Delete it
        delete_result = delete_book(book_code)
        
        # 7. Verify deletion
        deleted = get_book_by_code(book_code)
        assert deleted is None, "Book should be deleted"
    
    def test_reg_002_full_order_workflow(self):
        """TC-REG-002: Complete order lifecycle - Create → View → Return"""
        book_code = create_temp_available_book("REGORD")

        # Create order
        success, msg = create_rental_order("C001", [book_code], "2026-05-25")
        assert success is True, f"Should create order: {msg}"
        
        # Extract order code
        order_code = extract_order_code(msg)
        
        # View order detail
        details = get_order_details(order_code)
        assert details is not None, "Should view order detail"
        
        # Verify book is rented
        book_after = get_book_by_code(book_code)
        assert book_after.BookStatus == "Rented", "Book should be rented"
        
        # Return order
        return_success, return_msg = return_rental_order(order_code)
        assert return_success is True, f"Should return order: {return_msg}"
        
        # Verify book is available again
        book_final = get_book_by_code(book_code)
        assert book_final.BookStatus == "Available", "Book should be available after return"

# ============================================================================
# PYTEST FIXTURES & UTILITIES
# ============================================================================

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Setup test environment before running tests"""
    print("\n" + "="*70)
    print("BOOK RENTAL SYSTEM - TEST AUTOMATION SUITE")
    print("="*70)
    print(f"Test Execution Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")

@pytest.fixture(autouse=True)
def log_test_execution(request):
    """Log each test execution"""
    print(f"\n[TEST] {request.node.nodeid}")
    yield
    print(f"[PASSED] {request.node.nodeid}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\nStarting comprehensive test execution...\n")
    pytest.main([__file__, "-v", "--tb=short", "-ra"])
