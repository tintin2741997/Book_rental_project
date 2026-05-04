# Book Rental System - Requirement Based Test Case Suite

## Section 1: Functional Coverage Map

| Module | UI / Console Function | Service / Data Function | Coverage Notes |
|---|---|---|---|
| Authentication | Main menu: Admin login, Customer login, Exit | `login_by_role` | Valid login, invalid login, empty credentials, role mismatch, logout |
| Admin book management | Add, view list, search, update, delete | `add_book`, `get_all_books`, `search_books`, `update_book`, `delete_book` | CRUD, required fields, duplicate code, year validation, status delete rule |
| Admin customer management | Add, view list, search, update, delete | `add_customer`, `get_all_customers`, `search_customers`, `update_customer`, `delete_customer` | CRUD, duplicate code, active rental dependency, user-account dependency need confirmation |
| Admin rental orders | Create order, view orders, view detail, return books | `create_rental_order`, `get_all_orders`, `get_order_details`, `return_rental_order` | Single/multiple books, date validation, duplicate books, state changes |
| Customer functions | Search books, view book info/status, rent books, view current rentals | `customer_user_service` functions | Customer-visible search, status filtering, customer-created rental workflow |
| Reports | Rented books, available books, rental count by book | `count_rented_books`, `count_available_books`, `get_rental_count_by_book` | Count accuracy, detail table accuracy, empty data behavior |
| Data rules | Database constraints and service validation | SQL Server constraints, services | Unique codes, FK checks, allowed statuses, transaction integrity |

## Section 2: Business Rule / Workflow Coverage Matrix

| Rule / Workflow ID | Rule / Workflow | Covered Test Cases | Status |
|---|---|---|---|
| BR-01 | BookStatus only `Available` or `Rented` | TC-BR-001 | Covered |
| BR-02 | OrderStatus only `Renting` or `Returned` | TC-BR-002 | Covered |
| BR-03 | Delete book only when `Available` | TC-BM-010, TC-BM-011 | Covered |
| BR-04 | Cannot delete customer with active `Renting` order | TC-CM-008 | Covered |
| BR-05 | Customer must exist before rental order | TC-RO-003 | Covered |
| BR-06 | Book must exist before rental order | TC-RO-004 | Covered |
| BR-07 | Book must be `Available` before rental | TC-RO-005 | Covered |
| BR-08 | No duplicate book codes in same order after trim/uppercase | TC-RO-006 | Covered |
| BR-09 | Expected return date format is `YYYY-MM-DD` | TC-RO-007 | Covered |
| BR-10 | Expected return date must be >= today | TC-RO-008, TC-BR-005 | Covered, current DB mismatch found for equality |
| WF-01 | Login -> role menu -> logout | TC-AU-001, TC-AU-003, TC-AU-006 | Covered |
| WF-02 | Add/Search/Update/Delete book | TC-REG-001 | Covered |
| WF-03 | Create order -> detail -> return -> status restored | TC-REG-002 | Covered |
| WF-04 | Customer search -> rent -> view current rentals | TC-CU-001 to TC-CU-005 | Covered |

## Section 3: Full Test Case Table

| Test Case ID | Module | Sub-module | Feature / Function | Scenario | Coverage Type | Test Design Technique | Related Requirement / Source | Preconditions | Test Data | Test Steps | Expected Result | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-AU-001 | Authentication | Admin | Admin login | Login with valid admin credentials | Positive | EP | Report 1.2, 3.1.2; UI main menu option 1 | Admin user exists | `admin` / valid password / `Admin` | Select admin login, enter username/password | User object returned; Admin menu displayed; role is `Admin` | Critical |
| TC-AU-002 | Authentication | Admin | Admin login | Login with wrong password | Negative | EP | `login_by_role` | Admin user exists | `admin` / wrong password | Select admin login, submit invalid password | Login rejected; no admin menu; error shown | High |
| TC-AU-003 | Authentication | Customer | Customer login | Login with valid customer credentials | Positive | EP | Report customer use case | Customer user linked to `Customers` | valid customer account | Select customer login, enter credentials | Customer menu displayed; customer identity available | Critical |
| TC-AU-004 | Authentication | Role | Role mismatch | Customer credential used on Admin login | Negative | Decision Table | Users.Role check | Customer user exists | customer username/password, role `Admin` | Select admin login with customer credentials | Login rejected because role does not match | High |
| TC-AU-005 | Authentication | Validation | Empty credentials | Username or password blank | Negative | BVA | Input validation: not empty | Main menu displayed | empty username/password | Submit blank credential fields | Validation message; database not queried for invalid login | High |
| TC-AU-006 | Authentication | Session | Logout | Logout from admin/customer menu | State-based | State Transition | UI option `0. Đăng xuất` | User is logged in | N/A | Select `0` in role menu | Session returns to previous/main menu; logout message shown | High |
| TC-BM-001 | Book | View | View all books | Admin views book list | Positive | EP | Report book management | Admin logged in; books exist | N/A | Open book menu, select view list | Table shows ID, Code, Title, Author, Category, Year, Status | High |
| TC-BM-002 | Book | Search | Search by code/title/author/category | Search returns matching books | Positive | EP | Search requirement | Admin logged in | keyword matching one book | Select search, enter keyword | Only matching rows shown; no unrelated rows | High |
| TC-BM-003 | Book | Search | Empty search keyword | Search with blank keyword | Negative | BVA | Input not empty | Admin logged in | blank keyword | Select search, press Enter | Message says keyword cannot be empty | Medium |
| TC-BM-004 | Book | Add | Add valid book | Add complete valid book | Positive | EP | `add_book` | BookCode does not exist | unique code, title, author, year 2026 | Select add, enter all fields | Book inserted with `Available`; appears in list/search | Critical |
| TC-BM-005 | Book | Add | Required fields | Missing BookCode/Title/Author | Negative | BVA | Required input rule | Admin logged in | blank required field | Select add and omit one required value | Add rejected; no row created | High |
| TC-BM-006 | Book | Add | Duplicate BookCode | Add existing code | Negative | EP | Unique code rule | BookCode exists | existing BookCode | Submit add form | Rejected with duplicate-code message | High |
| TC-BM-007 | Book | Add/Update | Publish year validation | Non-numeric year | Negative | BVA | Menu year validation | Admin logged in | `20AB` | Add/update book with non-numeric year | Rejected; no change committed | Medium |
| TC-BM-008 | Book | Update | Update existing book | Update title/author/category/publisher/year | Positive | EP | `update_book` | Book exists | new title and author | Select update, enter code, enter new values | Fields changed; unchanged blank fields retain old values | High |
| TC-BM-009 | Book | Update | Update non-existing book | Unknown code | Negative | EP | `get_book_by_code` | Admin logged in | `B999999` | Select update, enter unknown code | Message says book not found; no update | Medium |
| TC-BM-010 | Book | Delete | Delete available book | Delete book with `Available` status | Business Rule | State Transition | BR-03 | Book exists and Available | temp BookCode | Select delete, enter code | Book removed from list/search | High |
| TC-BM-011 | Book | Delete | Delete rented book | Try deleting book with `Rented` status | Business Rule | State Transition | BR-03 | Book status is Rented | rented BookCode | Select delete, enter code | Delete rejected; book remains | Critical |
| TC-CM-001 | Customer | View | View all customers | Admin views customer list | Positive | EP | Report customer management | Admin logged in | N/A | Customer menu, select view list | Table displays CustomerID, Code, FullName, Phone, Address, Email | High |
| TC-CM-002 | Customer | Search | Search customer by code/name/phone | Matching customer search | Positive | EP | Customer search requirement | Admin logged in | partial name/phone | Enter keyword | Matching customer rows displayed | High |
| TC-CM-003 | Customer | Search | Blank search | Empty keyword | Negative | BVA | Input validation | Admin logged in | blank | Submit empty keyword | Rejected with keyword-required message | Medium |
| TC-CM-004 | Customer | Add | Add valid customer | Add complete customer | Positive | EP | `add_customer` | CustomerCode unique | unique code/name/phone/email | Enter fields and save | Customer inserted and searchable | High |
| TC-CM-005 | Customer | Add | Duplicate customer code | Add existing code | Negative | EP | Unique CustomerCode | CustomerCode exists | existing code | Submit add | Rejected; no duplicate row | High |
| TC-CM-006 | Customer | Update | Update existing customer | Update contact details | Positive | EP | `update_customer` | Customer exists | new phone/address/email | Submit update | Fields updated; blank optional values retain current values | High |
| TC-CM-007 | Customer | Delete | Delete customer with no active rentals | Valid delete | Positive | State Transition | Delete condition | Customer has no active orders | temp customer | Delete customer | Customer removed | Medium |
| TC-CM-008 | Customer | Delete | Delete customer with active rental | Active dependency | Business Rule | Decision Table | BR-04 | Customer has `Renting` order | CustomerCode | Delete customer | Rejected; customer and order remain | Critical |
| TC-CM-009 | Customer | Delete | Customer has login account | Account dependency | Need confirmation | Decision Table | Code has `has_user_account`; report unclear | Customer linked to Users | CustomerCode | Delete customer | Need confirmation: expected reject if user account exists | Medium |
| TC-RO-001 | Rental Order | Create | Single-book order | Create order with one available book | Positive | EP | Report 3.1.2 order workflow | Customer exists; book Available | C001, one book, future date | Select create order, enter data | Order created; detail row inserted; book becomes Rented | Critical |
| TC-RO-002 | Rental Order | Create | Multi-book order | Create order with multiple available books | Combination | EP | Order supports multiple books | Customer exists; 2 books Available | two BookCodes | Submit create order | One order and two details created; both books Rented | Critical |
| TC-RO-003 | Rental Order | Create | Missing customer | Unknown customer code | Negative | EP | BR-05 | No such customer | `C999999` | Create order | Rejected with customer-not-exist message | Critical |
| TC-RO-004 | Rental Order | Create | Missing book | Unknown book code | Negative | EP | BR-06 | Customer exists | `B999999` | Create order | Rejected with book-not-exist message | Critical |
| TC-RO-005 | Rental Order | Create | Rented book | Book unavailable | Business Rule | Decision Table | BR-07 | Book is Rented | rented BookCode | Create order | Rejected; no order/detail created | Critical |
| TC-RO-006 | Rental Order | Create | Duplicate books | Same book entered twice including case/space variation | Business Rule | EP | BR-08 | Customer exists | `B001, b001, B001 ` | Create order | Rejected for duplicate normalized BookCode | High |
| TC-RO-007 | Rental Order | Date | Invalid date format | Date not `YYYY-MM-DD` | Negative | BVA | BR-09 | Customer/book valid | `05/20/2026` | Create order | Rejected with date format message | High |
| TC-RO-008 | Rental Order | Date | Return date before today | Past date | Negative | BVA | BR-10 | Customer/book valid | yesterday | Create order | Rejected; no data created | High |
| TC-BR-005 | Rental Order | Date | Return date equals today | Boundary value equality | Business Rule | BVA | Report says date must not be earlier than today | Customer/book valid | today | Create order | Expected: accepted. Actual current run: DB constraint rejects; defect logged | Critical |
| TC-RO-009 | Rental Order | Create | Empty book list | No books provided | Negative | BVA | Required book list | Customer exists | empty list | Create order | Rejected with empty book list message | High |
| TC-RO-010 | Rental Order | View | View order list | Admin views all orders | Positive | EP | UI order menu option 2 | Orders exist | N/A | Select view orders | Table displays order code, customer, dates, status | High |
| TC-RO-011 | Rental Order | Detail | View existing order detail | Show order header and books | Positive | EP | UI order menu option 3 | Order exists | OrderCode | Enter order code | Order info and book detail table displayed | High |
| TC-RO-012 | Rental Order | Detail | Unknown order detail | Non-existing order | Negative | EP | `get_order_by_code` | No such order | `O999999` | Enter order code | Message says order not found | Medium |
| TC-RO-013 | Rental Order | Return | Return valid renting order | Valid return workflow | State-based | State Transition | BR-11 | Order is Renting; books Rented | OrderCode | Select return, enter code | ReturnDate set today; OrderStatus Returned; books Available | Critical |
| TC-RO-014 | Rental Order | Return | Return already returned order | Duplicate return | Business Rule | State Transition | BR-12 | OrderStatus Returned | OrderCode | Return same order again | Rejected; status unchanged | Critical |
| TC-RO-015 | Rental Order | Return | Unknown order return | Non-existing order | Negative | EP | `return_rental_order` validation | No such order | `O999999` | Enter order code | Rejected with order-not-exist message | High |
| TC-RO-016 | Rental Order | OrderCode | Sequential generated code | Generate next order code | Business Rule | BVA | `O001`, `O002` pattern | Existing orders known | N/A | Create order or call generator | Code starts `O`; numeric part increments from latest OrderID | Medium |
| TC-CU-001 | Customer UI | Search | Customer searches books | Search by code/title/author/category | Positive | EP | Customer use case | Customer logged in | keyword | Customer menu option 1 | Matching books shown with status | High |
| TC-CU-002 | Customer UI | Book info | View book by code | Existing code lookup | Positive | EP | Customer use case | Customer logged in | BookCode | Option 2, enter code | Full book fields displayed | High |
| TC-CU-003 | Customer UI | Status | View available/rented books | Status filter | Positive | EP | Customer use case | Customer logged in | Available/Rented option | Option 3 then choose status | Only selected status rows shown | High |
| TC-CU-004 | Customer UI | Rent | Customer rents available books | Customer order creation | Combination | State Transition | Customer rent workflow | Customer account linked to CustomerID; book Available | BookCode, future date | Option 4, enter codes/date | Order created; book Rented; customer can view it | Critical |
| TC-CU-005 | Customer UI | My rentals | View current rentals | Customer sees active rented books | Positive | EP | Customer use case | Customer has active order | N/A | Option 5 | Rows show OrderCode, RentDate, ExpectedReturn, BookCode, Title, Status | High |
| TC-RPT-001 | Reports | Rented count | Count rented books | Admin views rented report | Positive | EP | Report requirement | Admin logged in | N/A | Report option 1 | Count equals DB count where BookStatus=Rented; rented list shown | High |
| TC-RPT-002 | Reports | Available count | Count available books | Admin views available report | Positive | EP | Report requirement | Admin logged in | N/A | Report option 2 | Count equals DB count where BookStatus=Available; available list shown | High |
| TC-RPT-003 | Reports | Rental count | Rental count by book | Admin views rental statistics | Positive | EP | Report requirement | Admin logged in | N/A | Report option 3 | Table contains BookCode, Title, Author, RentalCount; counts match detail table | High |
| TC-REG-001 | Regression | Book lifecycle | Add -> search -> update -> delete | Complete book workflow | Combination | State Transition | Book management workflow | Admin logged in | unique temp book | Execute lifecycle sequence | All operations succeed; final book no longer exists | Medium |
| TC-REG-002 | Regression | Order lifecycle | Create -> detail -> return | Complete rental workflow | Combination | State Transition | Rental workflow | Customer and book exist | unique temp book | Create order, view detail, return | Correct order/book state transitions and data persistence | Critical |

## Need Confirmation

| Area | Question |
|---|---|
| Field validation | Maximum lengths for BookCode, CustomerCode, Username, phone, email, title, and author are not specified in the report. |
| Email/phone validation | Report lists email/phone fields but does not define required format rules. |
| Customer deletion | Code references `has_user_account`, but the report only clearly specifies active-rental blocking. Confirm whether customers with login accounts must be blocked from deletion. |
| Date boundary | Report says expected return date must not be earlier than current date, but the current database rejects equality with today. Confirm whether rule is `>= today` or `> today`. |
