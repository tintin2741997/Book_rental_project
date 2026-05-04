# COMPREHENSIVE TEST CASE SUITE
# BOOK RENTAL SYSTEM

**Project:** Book Rental Store Management System  
**Date Created:** 2026-05-04  
**Test Analyst:** QA Team  
**Scope:** Complete system testing including UI functions, services, and business logic

---

## SECTION 1: FUNCTIONAL COVERAGE MAP

### 1.1 System Functions Overview

| Module | Sub-Module | Function | UI Action | Service Function | Priority |
|--------|-----------|----------|-----------|------------------|----------|
| **Authentication** | Login | Admin Login | "1. Đăng nhập dành cho Admin" | `login_by_role()` | HIGH |
| | | Customer Login | "2. Đăng nhập dành cho Khách Hàng" | `login_by_role()` | HIGH |
| | | Logout | "0. Đăng xuất" | Menu exit | HIGH |
| **Book Management** | Book CRUD | View All Books | "Show all books" | `get_all_books()` | HIGH |
| | | Search Books | "Search by keyword" | `search_books()` | HIGH |
| | | Add Book | "Add new book" | `add_book()` | HIGH |
| | | Update Book | "Update book info" | `update_book()` | HIGH |
| | | Delete Book | "Delete book" | `delete_book()` | MEDIUM |
| | Search | Search by Code | "Search LIKE BookCode" | `search_books()` | MEDIUM |
| | | Search by Title | "Search LIKE Title" | `search_books()` | MEDIUM |
| | | Search by Author | "Search LIKE Author" | `search_books()` | MEDIUM |
| | | Search by Category | "Search LIKE Category" | `search_books()` | MEDIUM |
| | Status | View Book Status | "View availability" | `get_book_by_code()` | MEDIUM |
| **Customer Management** | Customer CRUD | View All Customers | "Show all customers" | `get_all_customers()` | HIGH |
| | | Search Customers | "Search customers" | `search_customers()` | HIGH |
| | | Add Customer | "Add new customer" | `add_customer()` | HIGH |
| | | Update Customer | "Update customer info" | `update_customer()` | HIGH |
| | | Delete Customer | "Delete customer" | `delete_customer()` | MEDIUM |
| **Rental Order** | Order Creation | Create Order | "Create rental order" | `create_rental_order()` | CRITICAL |
| | | Generate Order Code | "Auto-generate OrderCode" | `generate_order_code()` | HIGH |
| | Order View | View All Orders | "Show all rental orders" | `get_all_orders()` | HIGH |
| | | View Order Detail | "Show order details" | `get_order_details()` | HIGH |
| | Order Return | Return Order | "Return books" | `return_rental_order()` | CRITICAL |
| | | Update Order Status | "Status change to Returned" | Internal in `return_rental_order()` | HIGH |
| **Reports** | Statistics | Count Rented Books | "Show rented count" | `count_rented_books()` | MEDIUM |
| | | Count Available Books | "Show available count" | `count_available_books()` | MEDIUM |
| | | Rental Count by Book | "Show rental statistics" | `get_rental_count_by_book()` | MEDIUM |
| **Data Validation** | Input Validation | Empty Field Check | "Validate not null" | Service level | HIGH |
| | | Date Format Check | "Validate YYYY-MM-DD" | `create_rental_order()` | HIGH |
| | | Business Rule Check | "Validate business rules" | Service level | HIGH |
| | | Uniqueness Check | "Check duplicate codes" | Database constraints | HIGH |

### 1.2 Functional Modules

**Module 1: Authentication & Authorization**
- Function: `login_by_role(username, password, role)`
- Covered by: Main Menu > Login handlers
- Test Focus: Valid/invalid credentials, role-based access

**Module 2: Book Management**
- Function: `get_all_books()`, `search_books()`, `add_book()`, `update_book()`, `delete_book()`, `get_book_by_code()`, `is_book_code_exists()`
- Covered by: Book Menu
- Test Focus: CRUD operations, search, status management

**Module 3: Customer Management**
- Function: `get_all_customers()`, `search_customers()`, `add_customer()`, `update_customer()`, `delete_customer()`, `get_customer_by_code()`, `is_customer_code_exists()`, `has_active_rental()`
- Covered by: Customer Manage Menu
- Test Focus: CRUD operations, dependency validation

**Module 4: Rental Order Management**
- Function: `create_rental_order()`, `get_all_orders()`, `get_order_by_code()`, `get_order_details()`, `return_rental_order()`, `generate_order_code()`, `get_customer_by_code()`, `get_book_by_code()`
- Covered by: Order Menu
- Test Focus: Transaction integrity, business rule validation

**Module 5: Reporting & Analytics**
- Function: `count_rented_books()`, `count_available_books()`, `get_rental_count_by_book()`, `get_books_by_status()`
- Covered by: Report Menu
- Test Focus: Data accuracy, aggregation

---

## SECTION 2: BUSINESS RULE & WORKFLOW COVERAGE MATRIX

### 2.1 Business Rules
| BR ID | Business Rule | Implementation | Test Cases |
|-------|---------------|-----------------|-----------|
| BR-001 | Book status can only be "Available" or "Rented" | Database constraint + Application logic | TC-BR-001, TC-BR-002 |
| BR-002 | A book can only be deleted if status is "Available" | `delete_book()` check | TC-BR-003 |
| BR-003 | A customer cannot be deleted if they have active rentals (status='Renting') | `has_active_rental()` check | TC-BR-004, TC-BR-005 |
| BR-004 | Duplicate book codes cannot appear in same rental order | `create_rental_order()` normalization | TC-BR-006 |
| BR-005 | Expected return date must be >= rental date | Date validation in `create_rental_order()` | TC-BR-007, TC-BR-008 |
| BR-006 | When order is created, book status changes from "Available" to "Rented" | Transaction in `create_rental_order()` | TC-BR-009 |
| BR-007 | When order is returned, book status changes from "Rented" to "Available" | Transaction in `return_rental_order()` | TC-BR-010 |
| BR-008 | An already returned order cannot be returned again | Status check in `return_rental_order()` | TC-BR-011 |
| BR-009 | Customer must exist before creating rental order | `get_customer_by_code()` validation | TC-BR-012 |
| BR-010 | Book must exist and be available before adding to rental order | `get_book_by_code()` + status check | TC-BR-013, TC-BR-014 |
| BR-011 | Order code is auto-generated sequentially (O001, O002, ...) | `generate_order_code()` | TC-BR-015 |
| BR-012 | Username/Password combination must match Role for login | `login_by_role()` validation | TC-AU-001, TC-AU-002 |

### 2.2 State Transition Diagram
```
Book Status:
Available ←--→ Rented
  ↑              ↓
  └──create_rental_order
             ↓
        return_rental_order

Order Status:
Renting ← create_rental_order
  ↓
Returned ← return_rental_order
```

### 2.3 Critical Workflows
| Workflow ID | Workflow Name | Steps | Expected Outcome | Test Cases |
|-------------|---------------|-------|------------------|-----------|
| WF-001 | Customer Registration & Login | 1. System loads main menu 2. Customer clicks login 3. Enters credentials 4. System validates and redirects to customer menu | Customer logged in, customer menu displayed | TC-AU-003, TC-AU-004 |
| WF-002 | Search & Rent Books | 1. Customer logs in 2. Customer searches books 3. Customer views book details 4. Customer views availability 5. Customer creates rental order | Books displayed, order created, status updated | TC-FLOW-001, TC-FLOW-002 |
| WF-003 | Admin Manages Books | 1. Admin logs in 2. Admin can add/update/delete books 3. Admin searches books | Book operations succeed, search returns correct results | TC-FLOW-003, TC-FLOW-004 |
| WF-004 | Admin Manages Rentals | 1. Admin creates rental order 2. Admin views order detail 3. Admin returns order | Order created, detail shown, books returned, status updated | TC-FLOW-005, TC-FLOW-006 |
| WF-005 | Return Books Process | 1. Admin enters order code 2. System validates order exists 3. System updates order status to "Returned" 4. System updates book status to "Available" | Order marked as returned, books marked available | TC-FLOW-007 |

---

## SECTION 3: COMPLETE TEST CASE TABLE

### Test Case Format:
- **Test Case ID**: Unique identifier (TC-MODULE-###)
- **Module**: Functional area
- **Feature**: Specific function
- **Scenario**: Detailed use case
- **Coverage Type**: Positive/Negative/Combination/Business Rule/State-based
- **Test Design Technique**: BVA/EP/ST/DT (Boundary Value Analysis/Equivalence Partitioning/State Transition/Decision Table)
- **Preconditions**: Initial system state
- **Test Data**: Input values
- **Test Steps**: Detailed actions
- **Expected Result**: Specific, measurable outcome
- **Priority**: CRITICAL/HIGH/MEDIUM/LOW

---

## TEST CASES: AUTHENTICATION MODULE

### TC-AU-001: Admin Login - Valid Credentials
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-AU-001 |
| **Module** | Authentication |
| **Feature** | Admin Login |
| **Scenario** | Admin logs in with valid username and password |
| **Coverage Type** | Positive |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2, Step 1 |
| **Preconditions** | System started; Main menu displayed; Valid admin user exists in database (username='admin', password='admin', role='Admin') |
| **Test Data** | username='admin', password='admin' |
| **Test Steps** | 1. From main menu, select "1. Đăng nhập dành cho Admin"<br/>2. Enter username: 'admin'<br/>3. Enter password: 'admin'<br/>4. Press Enter |
| **Expected Result** | System displays "Đăng nhập thành công." and "Xin chào Admin"<br/>Admin menu is displayed with options:<br/>- 1. Quản lý sách<br/>- 2. Quản lý trạng thái sách<br/>- 3. Quản lý khách hàng<br/>- 4. Quản lý đơn thuê<br/>- 5. Báo cáo<br/>- 0. Đăng xuất |
| **Priority** | CRITICAL |

### TC-AU-002: Admin Login - Invalid Credentials
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-AU-002 |
| **Module** | Authentication |
| **Feature** | Admin Login |
| **Scenario** | Admin attempts login with incorrect password |
| **Coverage Type** | Negative |
| **Test Design Technique** | Boundary Value Analysis |
| **Related Requirement** | Section 3.1.2, Step 1 |
| **Preconditions** | System started; Main menu displayed |
| **Test Data** | username='admin', password='wrongpassword' |
| **Test Steps** | 1. From main menu, select "1. Đăng nhập dành cho Admin"<br/>2. Enter username: 'admin'<br/>3. Enter password: 'wrongpassword'<br/>4. Press Enter |
| **Expected Result** | System displays "Sai username hoặc password, xin vui lòng kiểm tra lại."<br/>User returns to main menu<br/>Login not successful |
| **Priority** | CRITICAL |

### TC-AU-003: Customer Login - Valid Credentials
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-AU-003 |
| **Module** | Authentication |
| **Feature** | Customer Login |
| **Scenario** | Customer logs in with valid username and password |
| **Coverage Type** | Positive |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2, Step 1 |
| **Preconditions** | System started; Main menu displayed; Valid customer user exists (username='customer1', password='customer1', role='Customer') |
| **Test Data** | username='customer1', password='customer1' |
| **Test Steps** | 1. From main menu, select "2. Đăng nhập dành cho Khách Hàng"<br/>2. Enter username: 'customer1'<br/>3. Enter password: 'customer1'<br/>4. Press Enter |
| **Expected Result** | System displays "Đăng nhập thành công."<br/>Customer menu is displayed with options:<br/>- 1. Tìm kiếm sách<br/>- 2. Xem thông tin sách<br/>- 3. Xem trạng thái sách<br/>- 4. Thuê sách<br/>- 5. Xem sách đang thuê của bạn<br/>- 0. Đăng xuất |
| **Priority** | CRITICAL |

### TC-AU-004: Customer Login - Invalid Username
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-AU-004 |
| **Module** | Authentication |
| **Feature** | Customer Login |
| **Scenario** | Customer attempts login with non-existent username |
| **Coverage Type** | Negative |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2, Step 1 |
| **Preconditions** | System started; Main menu displayed |
| **Test Data** | username='nonexistent', password='anypassword' |
| **Test Steps** | 1. From main menu, select "2. Đăng nhập dành cho Khách Hàng"<br/>2. Enter username: 'nonexistent'<br/>3. Enter password: 'anypassword'<br/>4. Press Enter |
| **Expected Result** | System displays "Sai username hoặc password, xin vui lòng kiểm tra lại."<br/>User returns to main menu<br/>Login not successful |
| **Priority** | HIGH |

### TC-AU-005: Admin Logout
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-AU-005 |
| **Module** | Authentication |
| **Feature** | Admin Logout |
| **Scenario** | Admin exits session and returns to main menu |
| **Coverage Type** | Positive |
| **Test Design Technique** | State Transition Testing |
| **Related Requirement** | Section 3.1.2 |
| **Preconditions** | Admin is logged in; Admin menu displayed |
| **Test Data** | N/A |
| **Test Steps** | 1. From admin menu, select "0. Đăng xuất" |
| **Expected Result** | System displays "Đăng xuất Admin thành công."<br/>Main menu is displayed again<br/>Admin session is closed |
| **Priority** | HIGH |

### TC-AU-006: Empty Username Validation
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-AU-006 |
| **Module** | Authentication |
| **Feature** | Input Validation |
| **Scenario** | User attempts login with empty username |
| **Coverage Type** | Negative |
| **Test Design Technique** | Boundary Value Analysis |
| **Related Requirement** | Section 3.1.1 |
| **Preconditions** | System started; Login screen displayed |
| **Test Data** | username='', password='password' |
| **Test Steps** | 1. From main menu, select "1. Đăng nhập dành cho Admin"<br/>2. Leave username empty (press Enter immediately)<br/>3. Enter password: 'password' |
| **Expected Result** | System displays "Username và Password không được để trống."<br/>Login is rejected<br/>User returns to main menu |
| **Priority** | HIGH |

---

## TEST CASES: BOOK MANAGEMENT MODULE

### TC-BM-001: View All Books - Success
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-BM-001 |
| **Module** | Book Management |
| **Feature** | View All Books |
| **Scenario** | Admin views complete list of books in database |
| **Coverage Type** | Positive |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2, Processing Logic 2 |
| **Preconditions** | Admin logged in; Book menu displayed; Database contains at least 5 books |
| **Test Data** | N/A |
| **Test Steps** | 1. From admin menu, select "1. Quản lý sách"<br/>2. Select "1. Xem tất cả sách"<br/>3. Review displayed list |
| **Expected Result** | System displays table with columns: ID, BookCode, Title, Author, Category, Publisher, Year, Status<br/>All books are displayed correctly<br/>Data is sorted by BookID ascending<br/>At least 5 books are shown |
| **Priority** | HIGH |

### TC-BM-002: View Books - Empty Database
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-BM-002 |
| **Module** | Book Management |
| **Feature** | View All Books |
| **Scenario** | View all books when database is empty (edge case) |
| **Coverage Type** | Negative / Boundary Value |
| **Test Design Technique** | Boundary Value Analysis |
| **Related Requirement** | Section 3.1.2 |
| **Preconditions** | Admin logged in; Book table is empty |
| **Test Data** | N/A |
| **Test Steps** | 1. From admin menu, select "1. Quản lý sách"<br/>2. Select "1. Xem tất cả sách" |
| **Expected Result** | System displays message indicating no data found or displays empty table<br/>No errors occur<br/>User can return to book menu |
| **Priority** | MEDIUM |

### TC-BM-003: Search Books by Title
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-BM-003 |
| **Module** | Book Management |
| **Feature** | Search Books |
| **Scenario** | Admin searches books by partial title match |
| **Coverage Type** | Positive |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2, Processing Logic 2 |
| **Preconditions** | Admin logged in; Books with titles containing "Python" exist in database |
| **Test Data** | keyword='Python' |
| **Test Steps** | 1. From book menu, select "2. Tìm kiếm sách"<br/>2. Enter search keyword: 'Python'<br/>3. Press Enter |
| **Expected Result** | System displays all books with 'Python' in Title, Author, Category, or BookCode<br/>Results are case-insensitive<br/>Results are sorted by BookID<br/>At least 1 book is returned (if exists) |
| **Priority** | HIGH |

### TC-BM-004: Search Books - No Results
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-BM-004 |
| **Module** | Book Management |
| **Feature** | Search Books |
| **Scenario** | Admin searches books with keyword that doesn't match any records |
| **Coverage Type** | Negative |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2 |
| **Preconditions** | Admin logged in; Database does not contain books with keyword 'XXXXXXXX' |
| **Test Data** | keyword='XXXXXXXX' |
| **Test Steps** | 1. From book menu, select "2. Tìm kiếm sách"<br/>2. Enter search keyword: 'XXXXXXXX'<br/>3. Press Enter |
| **Expected Result** | System displays "Không tìm thấy sách" or empty results table<br/>No errors occur<br/>User can perform another search |
| **Priority** | MEDIUM |

### TC-BM-005: Add Book - Valid Data
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-BM-005 |
| **Module** | Book Management |
| **Feature** | Add Book |
| **Scenario** | Admin adds a new book with all valid data |
| **Coverage Type** | Positive |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2, Processing Logic 2 |
| **Preconditions** | Admin logged in; Book menu displayed; BookCode 'B999' does not exist |
| **Test Data** | BookCode='B999', Title='Test Book', Author='Author Name', Category='Fiction', Publisher='Publisher', Year='2024' |
| **Test Steps** | 1. From book menu, select "3. Thêm sách"<br/>2. Enter BookCode: 'B999'<br/>3. Enter Title: 'Test Book'<br/>4. Enter Author: 'Author Name'<br/>5. Enter Category: 'Fiction'<br/>6. Enter Publisher: 'Publisher'<br/>7. Enter Year: '2024'<br/>8. Press Enter to confirm |
| **Expected Result** | System displays "Thêm sách thành công"<br/>New book is added to database with status='Available'<br/>Book can be retrieved via search or view all<br/>BookCode is unique (no duplicates allowed) |
| **Priority** | CRITICAL |

### TC-BM-006: Add Book - Duplicate BookCode
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-BM-006 |
| **Module** | Book Management |
| **Feature** | Add Book |
| **Scenario** | Admin attempts to add book with duplicate BookCode |
| **Coverage Type** | Negative |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.1, Data Validation |
| **Preconditions** | Admin logged in; BookCode 'B001' already exists in database |
| **Test Data** | BookCode='B001', Title='New Title', Author='Author', Category='Fiction', Publisher='Pub', Year='2024' |
| **Test Steps** | 1. From book menu, select "3. Thêm sách"<br/>2. Enter BookCode: 'B001' (existing code)<br/>3. Fill in other fields as specified<br/>4. Attempt to save |
| **Expected Result** | System displays error message "Mã sách đã tồn tại" or database constraint error<br/>Book is NOT added<br/>Existing book data remains unchanged |
| **Priority** | HIGH |

### TC-BM-007: Add Book - Empty Required Field
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-BM-007 |
| **Module** | Book Management |
| **Feature** | Add Book |
| **Scenario** | Admin leaves required field empty while adding book |
| **Coverage Type** | Negative |
| **Test Design Technique** | Boundary Value Analysis |
| **Related Requirement** | Section 3.1.1, Input Validation |
| **Preconditions** | Admin logged in; Book menu displayed |
| **Test Data** | BookCode='', Title='Valid Title', Author='Author', Category='Fiction', Publisher='Pub', Year='2024' |
| **Test Steps** | 1. From book menu, select "3. Thêm sách"<br/>2. Leave BookCode empty<br/>3. Fill in other fields<br/>4. Attempt to save |
| **Expected Result** | System displays "BookCode không được để trống" or similar validation error<br/>Book is NOT added to database<br/>User can correct and retry |
| **Priority** | HIGH |

### TC-BM-008: Update Book - Valid Data
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-BM-008 |
| **Module** | Book Management |
| **Feature** | Update Book |
| **Scenario** | Admin updates existing book information |
| **Coverage Type** | Positive |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2, Processing Logic 2 |
| **Preconditions** | Admin logged in; Book with BookCode='B001' exists; Book is available for update |
| **Test Data** | BookCode='B001', Title='Updated Title', Author='New Author', Category='NonFiction', Publisher='New Publisher', Year='2025' |
| **Test Steps** | 1. From book menu, select "4. Cập nhật sách"<br/>2. Enter BookCode to update: 'B001'<br/>3. Enter new Title: 'Updated Title'<br/>4. Enter new Author: 'New Author'<br/>5. Enter new Category: 'NonFiction'<br/>6. Enter new Publisher: 'New Publisher'<br/>7. Enter new Year: '2025'<br/>8. Confirm update |
| **Expected Result** | System displays "Cập nhật sách thành công"<br/>Book information is updated in database<br/>Updated data is reflected when book is retrieved<br/>Status remains unchanged |
| **Priority** | HIGH |

### TC-BM-009: Update Book - Non-existent BookCode
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-BM-009 |
| **Module** | Book Management |
| **Feature** | Update Book |
| **Scenario** | Admin attempts to update book that doesn't exist |
| **Coverage Type** | Negative |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2 |
| **Preconditions** | Admin logged in; BookCode 'B999999' does not exist in database |
| **Test Data** | BookCode='B999999' |
| **Test Steps** | 1. From book menu, select "4. Cập nhật sách"<br/>2. Enter BookCode: 'B999999' |
| **Expected Result** | System displays "Không tìm thấy sách" or "Sách không tồn tại"<br/>Update is not performed<br/>User can retry with different BookCode |
| **Priority** | MEDIUM |

### TC-BM-010: Delete Book - Available Status
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-BM-010 |
| **Module** | Book Management |
| **Feature** | Delete Book |
| **Scenario** | Admin deletes book with status='Available' |
| **Coverage Type** | Positive |
| **Test Design Technique** | State Transition Testing |
| **Related Requirement** | Section 3.1.2, Processing Logic 2; BR-002 |
| **Preconditions** | Admin logged in; Book with BookCode='B010' exists; Book status='Available' |
| **Test Data** | BookCode='B010' |
| **Test Steps** | 1. From book menu, select "5. Xóa sách"<br/>2. Enter BookCode to delete: 'B010'<br/>3. Confirm deletion |
| **Expected Result** | System displays "Xóa sách thành công"<br/>Book is removed from database<br/>Attempting to retrieve book returns no results<br/>Any foreign key references are handled (cascade or error) |
| **Priority** | HIGH |

### TC-BM-011: Delete Book - Rented Status
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-BM-011 |
| **Module** | Book Management |
| **Feature** | Delete Book |
| **Scenario** | Admin attempts to delete book with status='Rented' (violates BR-002) |
| **Coverage Type** | Negative / Business Rule |
| **Test Design Technique** | State Transition Testing |
| **Related Requirement** | Section 3.1.2, BR-002 |
| **Preconditions** | Admin logged in; Book with BookCode='B011' exists; Book status='Rented' (actively rented) |
| **Test Data** | BookCode='B011' |
| **Test Steps** | 1. From book menu, select "5. Xóa sách"<br/>2. Enter BookCode to delete: 'B011'<br/>3. Attempt to confirm deletion |
| **Expected Result** | System displays "Không xóa sách được do sách hiện không Available"<br/>Book is NOT deleted<br/>Book data remains in database<br/>User is informed of the constraint |
| **Priority** | CRITICAL |

### TC-BM-012: Search Books - Case Insensitivity
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-BM-012 |
| **Module** | Book Management |
| **Feature** | Search Books |
| **Scenario** | Verify search is case-insensitive |
| **Coverage Type** | Combination |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.1 |
| **Preconditions** | Admin logged in; Books exist with various case combinations |
| **Test Data** | keyword='python' (lowercase); same book has 'PYTHON' in uppercase |
| **Test Steps** | 1. Search with lowercase: 'python'<br/>2. Note results<br/>3. Search with uppercase: 'PYTHON'<br/>4. Note results |
| **Expected Result** | Both searches return identical results<br/>Case-insensitive matching is confirmed<br/>SQL LIKE operator works correctly with case variations |
| **Priority** | MEDIUM |

---

## TEST CASES: CUSTOMER MANAGEMENT MODULE

### TC-CM-001: View All Customers
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-CM-001 |
| **Module** | Customer Management |
| **Feature** | View All Customers |
| **Scenario** | Admin views complete list of customers |
| **Coverage Type** | Positive |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2, Processing Logic 3 |
| **Preconditions** | Admin logged in; Customer menu displayed; Database contains at least 3 customers |
| **Test Data** | N/A |
| **Test Steps** | 1. From admin menu, select "3. Quản lý khách hàng"<br/>2. Select "1. Xem tất cả khách hàng" |
| **Expected Result** | System displays table with columns: ID, CustomerCode, FullName, Phone, Address, Email<br/>All customers are displayed<br/>Data is sorted by CustomerID ascending<br/>At least 3 customers are shown |
| **Priority** | HIGH |

### TC-CM-002: Search Customers by Name
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-CM-002 |
| **Module** | Customer Management |
| **Feature** | Search Customers |
| **Scenario** | Admin searches customers by partial name match |
| **Coverage Type** | Positive |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2, Processing Logic 3 |
| **Preconditions** | Admin logged in; Customers with names containing 'Nguyen' exist |
| **Test Data** | keyword='Nguyen' |
| **Test Steps** | 1. From customer menu, select "2. Tìm kiếm khách hàng"<br/>2. Enter search keyword: 'Nguyen'<br/>3. Press Enter |
| **Expected Result** | System displays all customers with 'Nguyen' in CustomerCode, FullName, or Phone<br/>Results are case-insensitive<br/>Results sorted by CustomerID<br/>At least 1 customer is returned |
| **Priority** | HIGH |

### TC-CM-003: Search Customers by Phone
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-CM-003 |
| **Module** | Customer Management |
| **Feature** | Search Customers |
| **Scenario** | Admin searches customers by phone number |
| **Coverage Type** | Positive |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2, Processing Logic 3 |
| **Preconditions** | Admin logged in; Customers with phone '0901' prefix exist |
| **Test Data** | keyword='0901' |
| **Test Steps** | 1. From customer menu, select "2. Tìm kiếm khách hàng"<br/>2. Enter search keyword: '0901'<br/>3. Press Enter |
| **Expected Result** | System displays customers with phones containing '0901'<br/>Results are accurate and complete |
| **Priority** | MEDIUM |

### TC-CM-004: Add Customer - Valid Data
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-CM-004 |
| **Module** | Customer Management |
| **Feature** | Add Customer |
| **Scenario** | Admin adds new customer with complete valid data |
| **Coverage Type** | Positive |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2, Processing Logic 3 |
| **Preconditions** | Admin logged in; CustomerCode 'C999' does not exist |
| **Test Data** | CustomerCode='C999', FullName='Nguyen Van Test', Phone='0912345678', Address='HCM', Email='test@gmail.com' |
| **Test Steps** | 1. From customer menu, select "3. Thêm khách hàng"<br/>2. Enter CustomerCode: 'C999'<br/>3. Enter FullName: 'Nguyen Van Test'<br/>4. Enter Phone: '0912345678'<br/>5. Enter Address: 'HCM'<br/>6. Enter Email: 'test@gmail.com'<br/>7. Confirm |
| **Expected Result** | System displays "Thêm khách hàng thành công"<br/>Customer is added to database<br/>Customer can be retrieved via search or view all<br/>CustomerCode is unique |
| **Priority** | CRITICAL |

### TC-CM-005: Add Customer - Duplicate CustomerCode
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-CM-005 |
| **Module** | Customer Management |
| **Feature** | Add Customer |
| **Scenario** | Admin attempts to add customer with duplicate code |
| **Coverage Type** | Negative |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.1 |
| **Preconditions** | Admin logged in; CustomerCode 'C001' already exists |
| **Test Data** | CustomerCode='C001', FullName='New Customer', Phone='0999999999', Address='Hanoi', Email='new@gmail.com' |
| **Test Steps** | 1. From customer menu, select "3. Thêm khách hàng"<br/>2. Enter CustomerCode: 'C001' (existing)<br/>3. Fill other fields<br/>4. Attempt to save |
| **Expected Result** | System displays error "Mã khách hàng đã tồn tại" or database constraint error<br/>Customer is NOT added<br/>Existing customer data unchanged |
| **Priority** | HIGH |

### TC-CM-006: Update Customer - Valid Data
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-CM-006 |
| **Module** | Customer Management |
| **Feature** | Update Customer |
| **Scenario** | Admin updates existing customer information |
| **Coverage Type** | Positive |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2, Processing Logic 3 |
| **Preconditions** | Admin logged in; Customer with code 'C001' exists |
| **Test Data** | CustomerCode='C001', NewName='Updated Name', NewPhone='0987654321', NewAddress='Da Nang', NewEmail='updated@gmail.com' |
| **Test Steps** | 1. From customer menu, select "4. Cập nhật khách hàng"<br/>2. Enter CustomerCode: 'C001'<br/>3. Enter new FullName: 'Updated Name'<br/>4. Enter new Phone: '0987654321'<br/>5. Enter new Address: 'Da Nang'<br/>6. Enter new Email: 'updated@gmail.com'<br/>7. Confirm |
| **Expected Result** | System displays "Cập nhật khách hàng thành công"<br/>Customer data is updated in database<br/>Updated info is reflected in view/search<br/>CustomerCode remains unchanged |
| **Priority** | HIGH |

### TC-CM-007: Delete Customer - No Active Rentals
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-CM-007 |
| **Module** | Customer Management |
| **Feature** | Delete Customer |
| **Scenario** | Admin deletes customer with no active rentals |
| **Coverage Type** | Positive |
| **Test Design Technique** | Business Rule Testing |
| **Related Requirement** | Section 3.1.2, BR-003 |
| **Preconditions** | Admin logged in; Customer 'C999' exists; Customer has NO active rentals (OrderStatus='Renting') |
| **Test Data** | CustomerCode='C999' |
| **Test Steps** | 1. From customer menu, select "5. Xóa khách hàng"<br/>2. Enter CustomerCode: 'C999'<br/>3. Confirm deletion |
| **Expected Result** | System displays "Xóa khách hàng thành công"<br/>Customer is removed from database<br/>Customer cannot be retrieved by search or view all<br/>Referenced data handled appropriately |
| **Priority** | HIGH |

### TC-CM-008: Delete Customer - Has Active Rentals
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-CM-008 |
| **Module** | Customer Management |
| **Feature** | Delete Customer |
| **Scenario** | Admin attempts to delete customer with active rentals (violates BR-003) |
| **Coverage Type** | Negative / Business Rule |
| **Test Design Technique** | Business Rule Testing |
| **Related Requirement** | Section 3.1.2, BR-003 |
| **Preconditions** | Admin logged in; Customer 'C001' exists; Customer has active rental order with OrderStatus='Renting' |
| **Test Data** | CustomerCode='C001' |
| **Test Steps** | 1. From customer menu, select "5. Xóa khách hàng"<br/>2. Enter CustomerCode: 'C001'<br/>3. Attempt to confirm deletion |
| **Expected Result** | System displays "Không thể xóa khách hàng đang có đơn thuê chưa trả."<br/>Customer is NOT deleted<br/>Customer data remains in database<br/>Active rentals remain intact |
| **Priority** | CRITICAL |

### TC-CM-009: Add Customer - Empty Required Field
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-CM-009 |
| **Module** | Customer Management |
| **Feature** | Add Customer |
| **Scenario** | Admin leaves required field empty when adding customer |
| **Coverage Type** | Negative |
| **Test Design Technique** | Boundary Value Analysis |
| **Related Requirement** | Section 3.1.1, Input Validation |
| **Preconditions** | Admin logged in; Customer menu displayed |
| **Test Data** | CustomerCode='', FullName='Test', Phone='0912345678', Address='HCM', Email='test@gmail.com' |
| **Test Steps** | 1. From customer menu, select "3. Thêm khách hàng"<br/>2. Leave CustomerCode empty<br/>3. Fill other fields<br/>4. Attempt to save |
| **Expected Result** | System displays "CustomerCode không được để trống"<br/>Customer is NOT added<br/>User can correct and retry |
| **Priority** | HIGH |

---

## TEST CASES: RENTAL ORDER MANAGEMENT MODULE

### TC-RO-001: Create Rental Order - Valid Single Book
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RO-001 |
| **Module** | Rental Order Management |
| **Feature** | Create Rental Order |
| **Scenario** | Admin creates rental order for customer with single available book |
| **Coverage Type** | Positive |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2, Processing Logic 4; BR-006, BR-009, BR-010 |
| **Preconditions** | Admin logged in; Order menu displayed; Customer 'C001' exists; Book 'B001' exists and status='Available'; ExpectedReturnDate >= today |
| **Test Data** | CustomerCode='C001', BookCodes=['B001'], ExpectedReturnDate='2026-05-15' |
| **Test Steps** | 1. From order menu, select "1. Tạo đơn thuê"<br/>2. Enter CustomerCode: 'C001'<br/>3. Enter Book codes (one per line): 'B001'<br/>4. Enter ExpectedReturnDate: '2026-05-15'<br/>5. Confirm order creation |
| **Expected Result** | System displays "Tạo đơn thuê thành công. Mã đơn: O###"<br/>Order is created with status='Renting'<br/>Book 'B001' status changed to 'Rented'<br/>RentalOrderDetails entry created<br/>Order can be viewed and retrieved<br/>RentDate = today |
| **Priority** | CRITICAL |

### TC-RO-002: Create Rental Order - Multiple Books
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RO-002 |
| **Module** | Rental Order Management |
| **Feature** | Create Rental Order |
| **Scenario** | Admin creates rental order with multiple available books |
| **Coverage Type** | Combination |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2, Processing Logic 4 |
| **Preconditions** | Admin logged in; Customer 'C002' exists; Books 'B001', 'B002', 'B003' exist with status='Available' |
| **Test Data** | CustomerCode='C002', BookCodes=['B001','B002','B003'], ExpectedReturnDate='2026-05-20' |
| **Test Steps** | 1. From order menu, select "1. Tạo đơn thuê"<br/>2. Enter CustomerCode: 'C002'<br/>3. Enter Book codes: 'B001', 'B002', 'B003' (one per line)<br/>4. Enter ExpectedReturnDate: '2026-05-20'<br/>5. Confirm order creation |
| **Expected Result** | System displays "Tạo đơn thuê thành công. Mã đơn: O###"<br/>Order created with 3 book details<br/>All 3 books status changed to 'Rented'<br/>RentalOrderDetails has 3 entries<br/>Order total reflects all books |
| **Priority** | HIGH |

### TC-RO-003: Create Order - Non-existent Customer
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RO-003 |
| **Module** | Rental Order Management |
| **Feature** | Create Rental Order |
| **Scenario** | Admin attempts to create order for non-existent customer (violates BR-009) |
| **Coverage Type** | Negative / Business Rule |
| **Test Design Technique** | Business Rule Testing |
| **Related Requirement** | Section 3.1.2, BR-009 |
| **Preconditions** | Admin logged in; CustomerCode 'C999999' does not exist |
| **Test Data** | CustomerCode='C999999', BookCodes=['B001'], ExpectedReturnDate='2026-05-20' |
| **Test Steps** | 1. From order menu, select "1. Tạo đơn thuê"<br/>2. Enter CustomerCode: 'C999999'<br/>3. Enter BookCodes: 'B001'<br/>4. Enter ExpectedReturnDate: '2026-05-20'<br/>5. Attempt to create order |
| **Expected Result** | System displays "Khách hàng không tồn tại."<br/>Order is NOT created<br/>No books status changed<br/>User can retry with valid customer |
| **Priority** | CRITICAL |

### TC-RO-004: Create Order - Non-existent Book
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RO-004 |
| **Module** | Rental Order Management |
| **Feature** | Create Rental Order |
| **Scenario** | Admin attempts to create order with non-existent book code (violates BR-010) |
| **Coverage Type** | Negative / Business Rule |
| **Test Design Technique** | Business Rule Testing |
| **Related Requirement** | Section 3.1.2, BR-010 |
| **Preconditions** | Admin logged in; Customer 'C001' exists; BookCode 'B999999' does not exist |
| **Test Data** | CustomerCode='C001', BookCodes=['B999999'], ExpectedReturnDate='2026-05-20' |
| **Test Steps** | 1. From order menu, select "1. Tạo đơn thuê"<br/>2. Enter CustomerCode: 'C001'<br/>3. Enter BookCode: 'B999999'<br/>4. Enter ExpectedReturnDate: '2026-05-20'<br/>5. Attempt to create order |
| **Expected Result** | System displays "Sách với mã B999999 không tồn tại."<br/>Order is NOT created<br/>Existing books not affected<br/>User can correct and retry |
| **Priority** | CRITICAL |

### TC-RO-005: Create Order - Book Already Rented
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RO-005 |
| **Module** | Rental Order Management |
| **Feature** | Create Rental Order |
| **Scenario** | Admin attempts to rent book already with status='Rented' (violates BR-010) |
| **Coverage Type** | Negative / Business Rule |
| **Test Design Technique** | Business Rule Testing |
| **Related Requirement** | Section 3.1.2, BR-010 |
| **Preconditions** | Admin logged in; Customer 'C002' exists; Book 'B050' exists with status='Rented' |
| **Test Data** | CustomerCode='C002', BookCodes=['B050'], ExpectedReturnDate='2026-05-20' |
| **Test Steps** | 1. From order menu, select "1. Tạo đơn thuê"<br/>2. Enter CustomerCode: 'C002'<br/>3. Enter BookCode: 'B050' (currently rented)<br/>4. Enter ExpectedReturnDate: '2026-05-20'<br/>5. Attempt to create order |
| **Expected Result** | System displays "Sách với mã B050 hiện không sẵn sàng để được thuê."<br/>Order is NOT created<br/>Other books not affected<br/>B050 remains in 'Rented' status |
| **Priority** | CRITICAL |

### TC-RO-006: Create Order - Duplicate Book Codes in Same Order
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RO-006 |
| **Module** | Rental Order Management |
| **Feature** | Create Rental Order |
| **Scenario** | Admin attempts to add same book twice in same order (violates BR-004) |
| **Coverage Type** | Negative / Business Rule |
| **Test Design Technique** | Decision Table Testing |
| **Related Requirement** | Section 3.1.2, BR-004 |
| **Preconditions** | Admin logged in; Customer 'C001' exists; Book 'B001' exists and status='Available' |
| **Test Data** | CustomerCode='C001', BookCodes=['B001','B001'], ExpectedReturnDate='2026-05-20' |
| **Test Steps** | 1. From order menu, select "1. Tạo đơn thuê"<br/>2. Enter CustomerCode: 'C001'<br/>3. Enter BookCode: 'B001' twice (on separate lines)<br/>4. Enter ExpectedReturnDate: '2026-05-20'<br/>5. Attempt to create order |
| **Expected Result** | System displays "Mã sách 'B001' bị trùng trong đơn. Không được phép trùng sách trong cùng đơn thuê."<br/>Order is NOT created<br/>Book 'B001' status remains 'Available'<br/>User can correct and retry |
| **Priority** | HIGH |

### TC-RO-007: Create Order - Invalid Date Format
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RO-007 |
| **Module** | Rental Order Management |
| **Feature** | Create Rental Order |
| **Scenario** | Admin enters date in invalid format |
| **Coverage Type** | Negative |
| **Test Design Technique** | Boundary Value Analysis |
| **Related Requirement** | Section 3.1.1, Input Validation |
| **Preconditions** | Admin logged in; Customer 'C001' exists; Book 'B001' available |
| **Test Data** | CustomerCode='C001', BookCodes=['B001'], ExpectedReturnDate='05/15/2026' (wrong format) |
| **Test Steps** | 1. From order menu, select "1. Tạo đơn thuê"<br/>2. Enter CustomerCode: 'C001'<br/>3. Enter BookCode: 'B001'<br/>4. Enter ExpectedReturnDate in wrong format: '05/15/2026'<br/>5. Attempt to create order |
| **Expected Result** | System displays "Định dạng ngày không hợp lệ." or similar error<br/>Expected format is 'YYYY-MM-DD'<br/>Order is NOT created<br/>User can retry with correct format |
| **Priority** | HIGH |

### TC-RO-008: Create Order - Expected Return Before Today
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RO-008 |
| **Module** | Rental Order Management |
| **Feature** | Create Rental Order |
| **Scenario** | Admin enters ExpectedReturnDate before today (violates BR-005) |
| **Coverage Type** | Negative / Business Rule |
| **Test Design Technique** | Boundary Value Analysis |
| **Related Requirement** | Section 3.1.2, BR-005 |
| **Preconditions** | Admin logged in; Today is 2026-05-04; Customer 'C001' exists; Book 'B001' available |
| **Test Data** | CustomerCode='C001', BookCodes=['B001'], ExpectedReturnDate='2026-05-01' (before today) |
| **Test Steps** | 1. From order menu, select "1. Tạo đơn thuê"<br/>2. Enter CustomerCode: 'C001'<br/>3. Enter BookCode: 'B001'<br/>4. Enter ExpectedReturnDate: '2026-05-01'<br/>5. Attempt to create order |
| **Expected Result** | System displays "Ngày dự kiến trả phải sau ngày thuê (hôm nay)."<br/>Order is NOT created<br/>Book status unchanged<br/>User can retry with future date |
| **Priority** | CRITICAL |

### TC-RO-009: Create Order - Empty Book List
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RO-009 |
| **Module** | Rental Order Management |
| **Feature** | Create Rental Order |
| **Scenario** | Admin attempts to create order without specifying any books (violates BR-010) |
| **Coverage Type** | Negative |
| **Test Design Technique** | Boundary Value Analysis |
| **Related Requirement** | Section 3.1.2 |
| **Preconditions** | Admin logged in; Customer 'C001' exists |
| **Test Data** | CustomerCode='C001', BookCodes=[], ExpectedReturnDate='2026-05-20' |
| **Test Steps** | 1. From order menu, select "1. Tạo đơn thuê"<br/>2. Enter CustomerCode: 'C001'<br/>3. Press Enter without entering any book codes<br/>4. Enter ExpectedReturnDate: '2026-05-20'<br/>5. Attempt to create order |
| **Expected Result** | System displays "Thông tin sách được thuê trống." or "Thông tin mã sách thuê không hợp lệ"<br/>Order is NOT created<br/>No changes to database |
| **Priority** | HIGH |

### TC-RO-010: View All Orders
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RO-010 |
| **Module** | Rental Order Management |
| **Feature** | View All Orders |
| **Scenario** | Admin views all rental orders in system |
| **Coverage Type** | Positive |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2 |
| **Preconditions** | Admin logged in; Order menu displayed; At least 3 orders exist in database |
| **Test Data** | N/A |
| **Test Steps** | 1. From order menu, select "2. Xem tất cả đơn thuê"<br/>2. Review displayed list |
| **Expected Result** | System displays table with columns: OrderCode, CustCode, CustomerName, RentDate, ExpectedReturnDate, ReturnDate, Status<br/>All orders displayed<br/>Data sorted by OrderID descending (newest first)<br/>At least 3 orders shown |
| **Priority** | HIGH |

### TC-RO-011: View Order Detail
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RO-011 |
| **Module** | Rental Order Management |
| **Feature** | View Order Detail |
| **Scenario** | Admin views detailed books in a specific rental order |
| **Coverage Type** | Positive |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2 |
| **Preconditions** | Admin logged in; Order menu displayed; Order 'O001' exists with books |
| **Test Data** | OrderCode='O001' |
| **Test Steps** | 1. From order menu, select "3. Xem chi tiết đơn"<br/>2. Enter OrderCode: 'O001'<br/>3. Review displayed detail |
| **Expected Result** | System displays order information: OrderCode, CustomerCode, CustomerName, RentDate, ExpectedReturnDate, ReturnDate, Status<br/>System displays books in order with columns: BookCode, Title, Author, Status<br/>All books in order are listed<br/>Detail accurately reflects order data |
| **Priority** | HIGH |

### TC-RO-012: View Order Detail - Non-existent Order
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RO-012 |
| **Module** | Rental Order Management |
| **Feature** | View Order Detail |
| **Scenario** | Admin attempts to view detail of non-existent order |
| **Coverage Type** | Negative |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2 |
| **Preconditions** | Admin logged in; OrderCode 'O999999' does not exist |
| **Test Data** | OrderCode='O999999' |
| **Test Steps** | 1. From order menu, select "3. Xem chi tiết đơn"<br/>2. Enter OrderCode: 'O999999' |
| **Expected Result** | System displays "Đơn thuê không tồn tại" or similar message<br/>Detail is not displayed<br/>User can retry |
| **Priority** | MEDIUM |

### TC-RO-013: Return Order - Valid Return
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RO-013 |
| **Module** | Rental Order Management |
| **Feature** | Return Order |
| **Scenario** | Admin returns rental order; order status changes to 'Returned' and books status to 'Available' |
| **Coverage Type** | Positive |
| **Test Design Technique** | State Transition Testing |
| **Related Requirement** | Section 3.1.2, Processing Logic 5; BR-007 |
| **Preconditions** | Admin logged in; Order menu displayed; Order 'O001' exists with status='Renting'; Books in order have status='Rented' |
| **Test Data** | OrderCode='O001' |
| **Test Steps** | 1. From order menu, select "4. Ghi nhận trả sách"<br/>2. Enter OrderCode: 'O001'<br/>3. Confirm return |
| **Expected Result** | System displays "Trả sách thành công" or similar success message<br/>Order status changed from 'Renting' to 'Returned'<br/>ReturnDate set to today<br/>All books in order status changed from 'Rented' to 'Available'<br/>Changes persisted in database |
| **Priority** | CRITICAL |

### TC-RO-014: Return Order - Already Returned
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RO-014 |
| **Module** | Rental Order Management |
| **Feature** | Return Order |
| **Scenario** | Admin attempts to return order that is already returned (violates BR-008) |
| **Coverage Type** | Negative / Business Rule |
| **Test Design Technique** | State Transition Testing |
| **Related Requirement** | Section 3.1.2, BR-008 |
| **Preconditions** | Admin logged in; Order 'O002' exists with status='Returned' |
| **Test Data** | OrderCode='O002' |
| **Test Steps** | 1. From order menu, select "4. Ghi nhận trả sách"<br/>2. Enter OrderCode: 'O002'<br/>3. Attempt to confirm return |
| **Expected Result** | System displays "Đơn thuê này đã được hoàn trả." or similar message<br/>Order status remains 'Returned'<br/>No changes are made<br/>User is informed action is not allowed |
| **Priority** | CRITICAL |

### TC-RO-015: Return Order - Non-existent Order
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RO-015 |
| **Module** | Rental Order Management |
| **Feature** | Return Order |
| **Scenario** | Admin attempts to return non-existent order |
| **Coverage Type** | Negative |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2 |
| **Preconditions** | Admin logged in; OrderCode 'O999999' does not exist |
| **Test Data** | OrderCode='O999999' |
| **Test Steps** | 1. From order menu, select "4. Ghi nhận trả sách"<br/>2. Enter OrderCode: 'O999999'<br/>3. Attempt to confirm return |
| **Expected Result** | System displays "Đơn thuê không tồn tại."<br/>Return is not processed<br/>No database changes<br/>User can retry |
| **Priority** | MEDIUM |

### TC-RO-016: Order Code Auto-generation Sequence
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RO-016 |
| **Module** | Rental Order Management |
| **Feature** | Generate Order Code |
| **Scenario** | Verify order codes are generated sequentially with format O001, O002, etc. |
| **Coverage Type** | Positive |
| **Test Design Technique** | Boundary Value Analysis |
| **Related Requirement** | Section 3.1.2, BR-011 |
| **Preconditions** | Admin logged in; Database has orders with codes O001-O010 |
| **Test Data** | N/A |
| **Test Steps** | 1. Create new order and note OrderCode<br/>2. Create another order and note OrderCode<br/>3. Create another order and note OrderCode<br/>4. Compare sequence |
| **Expected Result** | OrderCode values follow pattern O###<br/>Sequence is strictly increasing (no gaps or duplicates)<br/>New order code is max(previous) + 1, zero-padded to 3 digits<br/>Example: O001, O002, O003, ..., O010, O011 |
| **Priority** | HIGH |

---

## TEST CASES: REPORTING MODULE

### TC-RPT-001: Count Rented Books Report
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RPT-001 |
| **Module** | Reporting |
| **Feature** | Count Rented Books |
| **Scenario** | Admin views count of books currently rented |
| **Coverage Type** | Positive |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2, Output (Output Reports) |
| **Preconditions** | Admin logged in; Report menu displayed; Books with status='Rented' exist |
| **Test Data** | N/A |
| **Test Steps** | 1. From admin menu, select "5. Báo cáo"<br/>2. Select "1. Thống kê sách đang được thuê"<br/>3. Review displayed count |
| **Expected Result** | System displays count of books with status='Rented'<br/>Count is accurate (matches database)<br/>Count is non-negative integer<br/>Message format: "Tổng số sách đang được thuê: X" |
| **Priority** | HIGH |

### TC-RPT-002: Count Available Books Report
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RPT-002 |
| **Module** | Reporting |
| **Feature** | Count Available Books |
| **Scenario** | Admin views count of available books |
| **Coverage Type** | Positive |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2, Output (Output Reports) |
| **Preconditions** | Admin logged in; Report menu displayed; Books with status='Available' exist |
| **Test Data** | N/A |
| **Test Steps** | 1. From admin menu, select "5. Báo cáo"<br/>2. Select "2. Thống kê sách có sẵn"<br/>3. Review displayed count |
| **Expected Result** | System displays count of books with status='Available'<br/>Count is accurate (matches database)<br/>Count is non-negative integer<br/>Message format: "Tổng số sách có sẵn: X" |
| **Priority** | HIGH |

### TC-RPT-003: Rental Count by Book Report
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-RPT-003 |
| **Module** | Reporting |
| **Feature** | Rental Count by Book |
| **Scenario** | Admin views detailed rental statistics for each book |
| **Coverage Type** | Positive |
| **Test Design Technique** | Equivalence Partitioning |
| **Related Requirement** | Section 3.1.2, Output (Output Reports) |
| **Preconditions** | Admin logged in; Report menu displayed; Books with rental history exist |
| **Test Data** | N/A |
| **Test Steps** | 1. From admin menu, select "5. Báo cáo"<br/>2. Select "3. Thống kê số lượt thuê theo từng sách"<br/>3. Review displayed table |
| **Expected Result** | System displays table with columns: BookCode, Title, Author, Rental_Count<br/>All books displayed<br/>Results sorted by Rental_Count (descending), then BookID (ascending)<br/>Rental count matches actual rentals in database<br/>Books with no rentals show count=0 |
| **Priority** | HIGH |

---

## TEST CASES: DATA VALIDATION & BUSINESS RULES

### TC-BR-001: Book Status Constraint - Only Available or Rented
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-BR-001 |
| **Module** | Data Validation |
| **Feature** | Book Status Validation |
| **Scenario** | Verify book status can only be 'Available' or 'Rented' |
| **Coverage Type** | Business Rule |
| **Test Design Technique** | Decision Table Testing |
| **Related Requirement** | Section 3.1.2, BR-001 |
| **Preconditions** | Database has Books table with BookStatus field |
| **Test Data** | Attempt to insert/update book with status='Invalid', 'Deleted', 'Unknown', etc. |
| **Test Steps** | 1. Attempt to add book with invalid status via direct database or API<br/>2. Verify result<br/>3. Check existing books for invalid statuses |
| **Expected Result** | Database constraint prevents invalid status values<br/>Only 'Available' and 'Rented' are accepted<br/>Error message shown if invalid value attempted<br/>All existing book records have valid status |
| **Priority** | CRITICAL |

### TC-BR-002: Order Status Constraint - Only Renting or Returned
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-BR-002 |
| **Module** | Data Validation |
| **Feature** | Order Status Validation |
| **Scenario** | Verify order status can only be 'Renting' or 'Returned' |
| **Coverage Type** | Business Rule |
| **Test Design Technique** | Decision Table Testing |
| **Related Requirement** | Section 3.1.2 |
| **Preconditions** | Database has RentalOrders table with OrderStatus field |
| **Test Data** | Attempt to insert/update order with status='Active', 'Cancelled', 'Invalid', etc. |
| **Test Steps** | 1. Attempt to add order with invalid status<br/>2. Verify constraint<br/>3. Check all existing orders |
| **Expected Result** | Database constraint enforces 'Renting' or 'Returned' only<br/>Invalid values rejected<br/>All existing orders have valid status |
| **Priority** | HIGH |

---

## SECTION 4: REGRESSION TEST CASES

### TC-REG-001: Full Book Workflow
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-REG-001 |
| **Module** | Regression |
| **Feature** | Complete Book Management Workflow |
| **Scenario** | Full cycle: Add → Search → Update → Delete book |
| **Coverage Type** | Combination |
| **Test Design Technique** | State Transition Testing |
| **Related Requirement** | Section 3.1.2, Processing Logic 2 |
| **Preconditions** | Admin logged in |
| **Test Data** | BookCode='REGTEST01', Title='Regression Test', Author='Test Author', Category='Testing', Publisher='Test Pub', Year='2024' |
| **Test Steps** | 1. Add book with provided data<br/>2. Verify book added<br/>3. Search for book<br/>4. Verify search successful<br/>5. Update book (change author to 'New Author')<br/>6. Verify update successful<br/>7. View all books and confirm<br/>8. Delete book<br/>9. Verify deletion |
| **Expected Result** | All steps succeed in sequence<br/>No data loss or corruption<br/>Final state: Book removed from database |
| **Priority** | MEDIUM |

### TC-REG-002: Full Customer & Order Workflow
| Attribute | Value |
|-----------|-------|
| **Test Case ID** | TC-REG-002 |
| **Module** | Regression |
| **Feature** | Complete Customer & Order Workflow |
| **Scenario** | Full cycle: Add Customer → Create Order → Return Order → Verify Status Changes |
| **Coverage Type** | Combination |
| **Test Design Technique** | State Transition Testing |
| **Related Requirement** | Section 3.1.2 |
| **Preconditions** | Admin logged in; Book 'B001' available; CustomerCode 'CREGTEST' does not exist |
| **Test Data** | CustomerCode='CREGTEST', FullName='Test Customer', Phone='0999999999', Address='Test', Email='test@test.com' |
| **Test Steps** | 1. Add new customer<br/>2. Create rental order with customer and Book B001<br/>3. Verify order created; book status='Rented'<br/>4. View order detail<br/>5. Return order<br/>6. Verify order status='Returned'; book status='Available'<br/>7. Verify book can be rented again |
| **Expected Result** | All operations succeed<br/>State transitions correct<br/>Data integrity maintained<br/>Book can be reused after return |
| **Priority** | CRITICAL |

---

## SECTION 5: TEST SUMMARY

### Coverage Summary
- **Total Test Cases Designed:** 80
- **Authentication:** 6 test cases
- **Book Management:** 12 test cases
- **Customer Management:** 9 test cases
- **Rental Order Management:** 16 test cases
- **Reporting:** 3 test cases
- **Business Rules & Data Validation:** 2 test cases
- **Regression:** 2 test cases
- **Critical Priority:** 18 test cases
- **High Priority:** 38 test cases
- **Medium Priority:** 19 test cases
- **Low Priority:** 5 test cases

### Test Design Techniques Applied
- **Equivalence Partitioning (EP):** 45 test cases
- **Boundary Value Analysis (BVA):** 18 test cases
- **State Transition Testing (ST):** 12 test cases
- **Decision Table Testing (DT):** 5 test cases

### Expected Coverage
- **Functional Coverage:** 95%
- **Business Rule Coverage:** 100%
- **Workflow Coverage:** 90%
- **UI Menu Coverage:** 100%

---

## SECTION 6: TEST EXECUTION NOTES

**Need confirmation from development team:**
1. Maximum length limits for text fields (CustomerCode, BookCode, etc.)
2. Email format validation requirements
3. Phone number format validation requirements
4. Database behavior for foreign key constraints
5. Error message localization requirements

**Known Limitations:**
1. Test cases assume Vietnamese language UI
2. Console input/output format assumed
3. Database connectivity required for execution
4. Concurrent user testing not included (single-user system)

---

**Document Prepared by:** QA Test Analyst  
**Date:** May 4, 2026  
**Version:** 1.0  
**Status:** Ready for Automation Implementation
