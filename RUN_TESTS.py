#!/usr/bin/env python
"""
Test Automation Setup Guide - Book Rental Project
Hướng dẫn cài đặt và chạy test automation
"""

# ============================================================
# SETUP INSTRUCTIONS - HƯỚNG DẪN CÀI ĐẶT
# ============================================================

print("""
╔════════════════════════════════════════════════════════════════╗
║         BOOK RENTAL PROJECT - TEST AUTOMATION GUIDE            ║
╚════════════════════════════════════════════════════════════════╝

📦 BƯỚC 1: CÀI ĐẶT PYTEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

pip install pytest

✅ Đã cài đặt! Kiểm tra:
pip show pytest


📊 BƯỚC 2: CHẠY TEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A. Chạy tất cả test:
   pytest test_order_automation.py test_menu_automation.py -v

B. Chạy test từng file:
   pytest test_order_automation.py -v      # 18 tests - Order functionality
   pytest test_menu_automation.py -v       # 14 tests - Menu & main functions

C. Chạy test cụ thể:
   pytest test_order_automation.py::TestCreateRentalOrder -v
   pytest test_order_automation.py::TestCreateRentalOrder::test_create_valid_order -v

D. Chạy test với chi tiết lỗi:
   pytest test_order_automation.py -v --tb=long

E. Chạy test im lặng:
   pytest test_order_automation.py -q


📈 BƯỚC 3: SINH BÁO CÁO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A. HTML Report (yêu cầu: pip install pytest-html):
   pytest test_order_automation.py test_menu_automation.py --html=report.html

B. JUnit Report:
   pytest test_order_automation.py test_menu_automation.py --junit-xml=report.xml

C. Coverage Report (yêu cầu: pip install pytest-cov):
   pytest test_order_automation.py test_menu_automation.py --cov=services --cov-report=html


🎯 TEST COVERAGE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test File 1: test_order_automation.py (18 tests)
├─ Order Code Generation (1 test)
│  └─ ✅ test_generate_order_code_format
├─ Customer Services (2 tests)
│  ├─ ✅ test_get_existing_customer
│  └─ ✅ test_get_non_existing_customer
├─ Book Services (2 tests)
│  ├─ ✅ test_get_existing_book
│  └─ ✅ test_get_non_existing_book
├─ Create Rental Order (6 tests)
│  ├─ ✅ test_create_order_invalid_customer
│  ├─ ✅ test_create_order_empty_book_list
│  ├─ ✅ test_create_order_invalid_return_date
│  ├─ ✅ test_create_order_duplicate_books
│  ├─ ✅ test_create_order_non_existing_book
│  └─ ✅ test_create_valid_order
├─ Return Order (3 tests)
│  ├─ ✅ test_return_non_existing_order
│  ├─ ✅ test_return_already_returned_order
│  └─ ✅ test_return_valid_order
├─ Get Order Info (4 tests)
│  ├─ ✅ test_get_non_existing_order
│  ├─ ✅ test_get_existing_order
│  ├─ ✅ test_get_all_orders_returns_list
│  └─ ✅ test_get_details_non_existing_order

Test File 2: test_menu_automation.py (14 tests)
├─ Book Service (3 tests)
│  ├─ ✅ test_get_all_books_returns_list
│  ├─ ✅ test_get_book_by_code_valid
│  └─ ✅ test_search_books_returns_list
├─ Customer Service (3 tests)
│  ├─ ✅ test_get_all_customers_returns_list
│  ├─ ✅ test_get_customer_by_code_valid
│  └─ ✅ test_search_customers_returns_list
├─ Order Service (3 tests)
│  ├─ ✅ test_get_all_orders_returns_list
│  ├─ ✅ test_get_order_by_code_valid
│  └─ ✅ test_get_order_details_valid
├─ Data Integrity (3 tests)
│  ├─ ✅ test_book_status_valid_values
│  ├─ ✅ test_order_status_valid_values
│  └─ ✅ test_order_date_consistency
└─ Edge Cases (2 tests)
   ├─ ✅ test_empty_search_results
   └─ ✅ test_special_characters_in_names


🔍 MAIN FUNCTIONALITIES TESTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Order Creation Validation:
   - ExpectedReturnDate >= RentDate kiểm tra
   - Không cho trùng sách trong đơn
   - Kiểm tra sách tồn tại và Available
   - Kiểm tra khách hàng tồn tại

✅ Transaction Support:
   - BEGIN TRANSACTION
   - INSERT/UPDATE operations
   - COMMIT on success
   - ROLLBACK on error

✅ Order Return:
   - Kiểm tra đơn tồn tại
   - Kiểm tra chưa trả
   - Cập nhật status
   - Restore book availability

✅ Data Queries:
   - Lấy tất cả sách/khách/đơn
   - Tìm kiếm theo mã/keyword
   - Get order details

✅ Data Integrity:
   - Book status: Available/Rented
   - Order status: Renting/Returned
   - Date consistency


📝 QUICK START COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Chạy tất cả test:
pytest test_order_automation.py test_menu_automation.py -v

# Kiểm tra tạo đơn:
pytest test_order_automation.py::TestCreateRentalOrder -v

# Kiểm tra trả sách:
pytest test_order_automation.py::TestReturnRentalOrder -v

# Kiểm tra validation:
pytest test_order_automation.py::TestCreateRentalOrder::test_create_order_duplicate_books -v
pytest test_order_automation.py::TestCreateRentalOrder::test_create_order_invalid_return_date -v


✨ EXPECTED OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-8.4.0, pluggy-1.6.0
collected 32 items

test_order_automation.py::TestOrderCodeGeneration::test_generate_order_code_format PASSED [  3%]
test_order_automation.py::TestGetCustomerByCode::test_get_existing_customer PASSED [  6%]
...
============================= 32 passed in 0.39s ==============================


🎉 SUCCESS INDICATORS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Nếu thấy: "32 passed in 0.39s"
   → Tất cả test OK, project ready for production!

⚠️  Nếu thấy: "FAILED" hoặc "ERROR"
   → Có vấn đề, cần debug


📞 TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q: ModuleNotFoundError: No module named 'pytest'
A: pip install pytest

Q: Database connection failed
A: Kiểm tra config.py - SERVER, DATABASE, USERNAME, PASSWORD

Q: Tests slow
A: Kiểm tra database connection - có thể network latency


📚 RESOURCES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pytest Documentation: https://docs.pytest.org
Test Best Practices: https://pytest.readthedocs.io/en/stable/
TEST_REPORT.md: Full detailed report


╔════════════════════════════════════════════════════════════════╗
║          TEST AUTOMATION SETUP COMPLETE ✅                     ║
║                Ready to run: pytest -v                         ║
╚════════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    print("\nTo run tests, execute one of these commands:")
    print("\n1. Run all tests:")
    print("   pytest test_order_automation.py test_menu_automation.py -v")
    print("\n2. Run specific test file:")
    print("   pytest test_order_automation.py -v")
    print("\n3. Run specific test class:")
    print("   pytest test_order_automation.py::TestCreateRentalOrder -v")
    print("\n4. Run with detailed output:")
    print("   pytest test_order_automation.py -vv -s")
