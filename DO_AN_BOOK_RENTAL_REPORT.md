# ĐẠI HỌC QUỐC GIA THÀNH PHỐ HỒ CHÍ MINH
# TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN
# KHOA KHOA HỌC VÀ KỸ THUẬT THÔNG TIN

# BÁO CÁO ĐỒ ÁN
# MÔN KỸ THUẬT LẬP TRÌNH PYTHON

Đề tài: Xây dựng ứng dụng quản lý thuê sách (Book Rental Store) bằng ngôn ngữ lập trình Python và cơ sở dữ liệu SQL Server

Sinh viên thực hiện:

Mã lớp: IE221.E12.CN2

\pagebreak

IE221.E12.CN2 - Kỹ thuật lập trình Python

# NHẬN XÉT CỦA GIÁO VIÊN HƯỚNG DẪN

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

..................................................................................................................................

……., ngày……tháng……năm 20…

Người nhận xét

(Ký tên và ghi rõ họ tên)

\pagebreak

IE221.E12.CN2 - Kỹ thuật lập trình Python

# MỤC LỤC

MỤC LỤC

Chương 1: Giới thiệu

1.1. Tổng quan

1.2. Mục tiêu

Chương 2: Cơ sở lý thuyết

2.1. Giới thiệu về hệ thống quản lý thuê sách

2.2. Giới thiệu Python và SQL Server trong xây dựng ứng dụng quản lý dữ liệu

Chương 3: Phương pháp thực hiện

3.1. Mô hình tổng quát (Input-Processing-Output)

3.1.1. Input (Đầu vào)

3.1.2. Processing (Xử lý logic)

3.1.3. Output (Đầu ra)

3.2. Use Case Diagram cho hệ thống quản lý thuê sách

Chương 4: Triển khai lập trình và Diễn giải

Chương 5: Kết luận

5.1. Ưu điểm đã làm được

5.2. Nhược điểm chưa làm được

5.3. Hướng phát triển

TÀI LIỆU THAM KHẢO

PHỤ LỤC

\pagebreak

IE221.E12.CN2 - Kỹ thuật lập trình Python

# Chương 1: Giới thiệu

## 1.1. Tổng quan

Tên đề tài: Xây dựng ứng dụng quản lý thuê sách (Book Rental Store) bằng ngôn ngữ lập trình Python và cơ sở dữ liệu SQL Server.

Lý do chọn đề tài:

Trong thực tế, các cửa hàng cho thuê sách hoặc thư viện quy mô nhỏ thường cần theo dõi nhiều nhóm thông tin như danh mục sách, thông tin khách hàng, tình trạng sách đang có sẵn hay đang được thuê, đơn thuê sách và quá trình trả sách. Nếu các thao tác này được ghi nhận thủ công bằng sổ sách hoặc bảng tính rời rạc, người quản lý dễ gặp các vấn đề như thất lạc thông tin, cập nhật chậm, khó kiểm tra lịch sử thuê, khó biết cuốn sách nào đang được mượn và khó thống kê số lượng sách còn trong kho.

Vì vậy, đề tài xây dựng ứng dụng Book Rental Store được lựa chọn nhằm mô phỏng một hệ thống quản lý thuê sách cơ bản, có khả năng lưu trữ dữ liệu tập trung trên SQL Server và thao tác thông qua chương trình Python dạng menu. Hệ thống hỗ trợ hai nhóm người dùng chính: Admin và Customer. Admin có quyền quản lý sách, khách hàng, đơn thuê, ghi nhận trả sách và xem báo cáo thống kê. Customer có thể đăng nhập, tra cứu sách, xem trạng thái sách, tạo yêu cầu thuê sách và xem các sách mình đang thuê.

Đề tài phù hợp với môn Kỹ thuật lập trình Python vì kết hợp được nhiều nội dung quan trọng: tổ chức chương trình theo module, viết hàm xử lý nghiệp vụ, kết nối cơ sở dữ liệu bằng `pyodbc`, sử dụng câu lệnh SQL, kiểm tra điều kiện đầu vào, xử lý transaction và kiểm thử tự động bằng `pytest`. Thông qua đề tài, người thực hiện có thể rèn luyện khả năng phân tích yêu cầu, thiết kế dữ liệu, triển khai chức năng và kiểm thử tính đúng đắn của ứng dụng.

## 1.2. Mục tiêu

Mục tiêu đầu tiên của đề tài là phát triển một ứng dụng quản lý thuê sách bằng Python với giao diện console rõ ràng, dễ thao tác, có các nhóm chức năng chính bao gồm:

- Đăng nhập theo vai trò Admin và Customer.
- Quản lý sách: xem danh sách, tìm kiếm, thêm, cập nhật và xóa sách khi sách còn ở trạng thái có sẵn.
- Quản lý khách hàng: xem danh sách, tìm kiếm, thêm, cập nhật và kiểm tra điều kiện trước khi xóa.
- Quản lý đơn thuê: tạo đơn thuê, xem danh sách đơn, xem chi tiết đơn, ghi nhận trả sách.
- Xử lý nghiệp vụ thuê sách: kiểm tra khách hàng tồn tại, kiểm tra sách tồn tại, kiểm tra sách có sẵn, không cho trùng mã sách trong cùng một đơn, kiểm tra ngày dự kiến trả hợp lệ.
- Cập nhật trạng thái sách: khi tạo đơn thuê, sách chuyển sang trạng thái `Rented`; khi trả sách, sách chuyển lại trạng thái `Available`.
- Báo cáo thống kê: thống kê sách đang được thuê, sách có sẵn và số lượt thuê theo từng sách.
- Lưu trữ dữ liệu bằng SQL Server với các bảng, khóa chính, khóa ngoại, ràng buộc duy nhất và ràng buộc kiểm tra dữ liệu.
- Kiểm thử tự động các chức năng cốt lõi bằng `pytest`.

Ngoài ra, đề tài còn hướng đến việc nâng cao kỹ năng lập trình Python theo hướng có cấu trúc, tách rõ tầng menu, tầng service và tầng truy cập dữ liệu. Người thực hiện cũng đặt mục tiêu hiểu rõ hơn về cách xây dựng một ứng dụng quản lý dữ liệu hoàn chỉnh: từ phân tích nghiệp vụ, thiết kế cơ sở dữ liệu, viết chức năng, xử lý lỗi cho đến kiểm thử.

\pagebreak

IE221.E12.CN2 - Kỹ thuật lập trình Python

# Chương 2: Cơ sở lý thuyết

## 2.1. Giới thiệu về hệ thống quản lý thuê sách

Hệ thống quản lý thuê sách là một dạng ứng dụng quản lý nghiệp vụ, trong đó dữ liệu trung tâm bao gồm sách, khách hàng, người dùng, đơn thuê và chi tiết đơn thuê. Mục tiêu của hệ thống là hỗ trợ cửa hàng hoặc thư viện kiểm soát vòng đời của một cuốn sách từ khi có sẵn trong kho, được khách hàng thuê, cho đến khi được trả lại.

Trong mô hình này, mỗi cuốn sách được gán một mã sách duy nhất, đi kèm các thông tin như tên sách, tác giả, thể loại, nhà xuất bản, năm xuất bản và trạng thái hiện tại. Trạng thái sách là yếu tố quan trọng vì quyết định sách có thể được đưa vào đơn thuê hay không. Dự án sử dụng hai trạng thái chính: `Available` cho sách có sẵn và `Rented` cho sách đang được thuê.

Khách hàng được quản lý bằng mã khách hàng duy nhất, họ tên, số điện thoại, địa chỉ và email. Khi khách hàng thuê sách, hệ thống tạo một đơn thuê trong bảng `RentalOrders` và lưu từng cuốn sách thuộc đơn thuê trong bảng `RentalOrderDetails`. Cách tách bảng đơn thuê và chi tiết đơn thuê giúp hệ thống hỗ trợ một đơn có thể gồm nhiều cuốn sách, đồng thời vẫn đảm bảo dữ liệu được chuẩn hóa.

Các nghiệp vụ chính của hệ thống quản lý thuê sách gồm:

- Tra cứu sách theo mã, tên sách, tác giả hoặc thể loại.
- Quản lý thông tin sách và khách hàng.
- Tạo đơn thuê cho khách hàng.
- Kiểm tra điều kiện trước khi cho thuê sách.
- Ghi nhận ngày thuê, ngày dự kiến trả và ngày trả thực tế.
- Cập nhật trạng thái sách và trạng thái đơn thuê.
- Thống kê dữ liệu phục vụ theo dõi hoạt động của cửa hàng.

Thông qua hệ thống này, người quản lý có thể giảm thao tác thủ công, hạn chế sai sót khi cập nhật trạng thái sách và dễ dàng theo dõi những đơn thuê đang còn hiệu lực.

## 2.2. Giới thiệu Python và SQL Server trong xây dựng ứng dụng quản lý dữ liệu

Python là ngôn ngữ lập trình bậc cao, có cú pháp rõ ràng, dễ đọc và phù hợp để xây dựng các chương trình quản lý nghiệp vụ ở quy mô học tập hoặc triển khai nội bộ. Trong dự án Book Rental Store, Python được dùng để xây dựng toàn bộ logic chương trình, bao gồm giao diện menu console, kiểm tra dữ liệu đầu vào, gọi các hàm service, kết nối cơ sở dữ liệu và hiển thị kết quả cho người dùng.

Một số đặc điểm nổi bật của Python được áp dụng trong dự án:

- Cú pháp đơn giản, thuận tiện cho việc tổ chức chương trình thành nhiều file và nhiều hàm.
- Hỗ trợ thư viện kết nối cơ sở dữ liệu như `pyodbc`.
- Dễ kiểm thử bằng framework `pytest`.
- Phù hợp với mô hình ứng dụng console, giúp tập trung vào logic nghiệp vụ và cơ sở dữ liệu.

SQL Server là hệ quản trị cơ sở dữ liệu quan hệ do Microsoft phát triển, hỗ trợ lưu trữ dữ liệu dạng bảng, thiết lập khóa chính, khóa ngoại, ràng buộc kiểm tra và thực hiện truy vấn bằng SQL. Trong dự án, SQL Server được sử dụng để tạo database `BookRentalStore` với các bảng chính:

- `Books`: lưu thông tin sách.
- `Customers`: lưu thông tin khách hàng.
- `Users`: lưu tài khoản đăng nhập và vai trò.
- `RentalOrders`: lưu thông tin đơn thuê.
- `RentalOrderDetails`: lưu danh sách sách thuộc từng đơn thuê.

Để Python có thể làm việc với SQL Server, dự án sử dụng thư viện `pyodbc`. File `db.py` định nghĩa các hàm dùng chung như `get_connection`, `fetch_all`, `fetch_one`, `execute_query` và `execute_insert_and_get_id`. Nhờ đó, các service không cần lặp lại mã kết nối mà chỉ tập trung vào câu truy vấn và nghiệp vụ tương ứng.

Trong các nghiệp vụ quan trọng như tạo đơn thuê và trả sách, hệ thống sử dụng transaction với các thao tác `BEGIN TRANSACTION`, `COMMIT` và `ROLLBACK`. Transaction giúp đảm bảo tính toàn vẹn dữ liệu: nếu một bước trong quá trình tạo đơn hoặc trả sách xảy ra lỗi, toàn bộ thay đổi sẽ được hủy bỏ, tránh tình trạng đơn thuê được tạo nhưng trạng thái sách chưa được cập nhật hoặc ngược lại.

\pagebreak

IE221.E12.CN2 - Kỹ thuật lập trình Python

# Chương 3: Phương pháp thực hiện

## 3.1. Mô hình tổng quát (Input-Processing-Output)

Hệ thống Book Rental Store được xây dựng theo mô hình Input - Processing - Output. Người dùng nhập dữ liệu thông qua menu console, chương trình xử lý dữ liệu bằng các hàm service và truy vấn SQL Server, sau đó hiển thị kết quả ra màn hình.

### 3.1.1. Input (Đầu vào)

Nguồn đầu vào chính của hệ thống là bàn phím. Người dùng lựa chọn chức năng từ menu và nhập các thông tin cần thiết theo từng nghiệp vụ. Các nhóm dữ liệu đầu vào gồm:

- Thông tin đăng nhập: username, password và vai trò đăng nhập tương ứng.
- Thông tin sách: mã sách, tên sách, tác giả, thể loại, nhà xuất bản, năm xuất bản và trạng thái sách.
- Thông tin khách hàng: mã khách hàng, họ tên, số điện thoại, địa chỉ và email.
- Thông tin thuê sách: mã khách hàng, danh sách mã sách muốn thuê và ngày dự kiến trả.
- Thông tin trả sách: mã đơn thuê cần ghi nhận trả.
- Từ khóa tìm kiếm: mã sách, tên sách, tác giả, thể loại, mã khách hàng, họ tên hoặc số điện thoại.

Chương trình có các bước kiểm tra đầu vào như không cho bỏ trống thông tin bắt buộc, chuẩn hóa mã sách về chữ hoa, loại bỏ khoảng trắng thừa, kiểm tra định dạng ngày theo `YYYY-MM-DD`, kiểm tra ngày dự kiến trả không nhỏ hơn ngày thuê và kiểm tra mã sách bị trùng trong cùng một đơn thuê.

### 3.1.2. Processing (Xử lý logic)

Các logic nghiệp vụ chính của hệ thống bao gồm:

1. Xử lý đăng nhập:

- Người dùng chọn đăng nhập với vai trò Admin hoặc Customer.
- Hàm `login_by_role` kiểm tra username, password và role trong bảng `Users`.
- Nếu thông tin hợp lệ, hệ thống chuyển đến menu tương ứng với vai trò.

2. Xử lý quản lý sách:

- Admin có thể xem toàn bộ sách, tìm kiếm sách, thêm sách mới, cập nhật thông tin sách và xóa sách.
- Khi xóa sách, hệ thống chỉ cho phép xóa nếu sách đang ở trạng thái `Available`.
- Tìm kiếm sách được thực hiện theo mã sách, tên sách, tác giả hoặc thể loại.

3. Xử lý quản lý khách hàng:

- Admin có thể xem, tìm kiếm, thêm và cập nhật thông tin khách hàng.
- Khi xóa khách hàng, hệ thống kiểm tra khách hàng có đơn thuê đang ở trạng thái `Renting` hay không.
- Việc kiểm tra giúp tránh xóa khách hàng khi còn phát sinh dữ liệu thuê sách chưa hoàn tất.

4. Xử lý tạo đơn thuê:

- Hệ thống kiểm tra khách hàng có tồn tại không.
- Hệ thống kiểm tra danh sách mã sách có rỗng không.
- Ngày dự kiến trả được kiểm tra theo định dạng ngày và không được nhỏ hơn ngày hiện tại.
- Mã sách được chuẩn hóa, loại bỏ trùng lặp và kiểm tra từng mã sách.
- Mỗi sách phải tồn tại và đang có trạng thái `Available`.
- Hệ thống sinh mã đơn thuê mới theo dạng `O001`, `O002`, ...
- Dữ liệu được ghi vào `RentalOrders` và `RentalOrderDetails`.
- Trạng thái các sách trong đơn được cập nhật thành `Rented`.
- Toàn bộ thao tác được đặt trong transaction để đảm bảo dữ liệu nhất quán.

5. Xử lý trả sách:

- Hệ thống kiểm tra mã đơn thuê có tồn tại không.
- Nếu đơn đã ở trạng thái `Returned`, hệ thống không cho trả lại lần nữa.
- Khi trả hợp lệ, hệ thống cập nhật `ReturnDate` bằng ngày hiện tại và cập nhật `OrderStatus` thành `Returned`.
- Các sách thuộc đơn thuê được cập nhật lại trạng thái `Available`.
- Thao tác trả sách cũng được thực hiện trong transaction.

6. Xử lý báo cáo:

- Thống kê số lượng sách đang được thuê.
- Thống kê số lượng sách có sẵn.
- Thống kê số lượt thuê theo từng sách bằng cách kết hợp bảng `Books` và `RentalOrderDetails`.

### 3.1.3. Output (Đầu ra)

Nguồn đầu ra của hệ thống là màn hình console. Sau mỗi thao tác, chương trình hiển thị thông báo kết quả hoặc bảng dữ liệu tương ứng. Các loại đầu ra chính gồm:

- Thông báo đăng nhập thành công hoặc thất bại.
- Danh sách sách với các cột: ID, mã sách, tên sách, tác giả, thể loại, năm xuất bản và trạng thái.
- Danh sách khách hàng với mã khách hàng, họ tên, số điện thoại, địa chỉ và email.
- Danh sách đơn thuê với mã đơn, mã khách hàng, tên khách hàng, ngày thuê, ngày dự kiến trả và trạng thái đơn.
- Chi tiết đơn thuê gồm thông tin đơn và danh sách sách trong đơn.
- Thông báo tạo đơn thuê thành công hoặc lý do thất bại.
- Thông báo trả sách thành công hoặc lý do không thể trả.
- Kết quả thống kê sách đang thuê, sách có sẵn và số lượt thuê theo sách.

Các dữ liệu hiển thị được định dạng thành bảng bằng chuỗi định dạng trong Python để người dùng dễ quan sát. Ví dụ, menu đơn thuê hiển thị các cột `OrderCode`, `CustCode`, `Customer Name`, `RentDate`, `ExpectedReturn` và `Status`.

## 3.2. Use Case Diagram cho hệ thống quản lý thuê sách

Hệ thống có hai tác nhân chính:

- Admin: người quản trị cửa hàng, chịu trách nhiệm quản lý sách, khách hàng, đơn thuê, trả sách và báo cáo thống kê.
- Customer: khách hàng đăng nhập vào hệ thống để tra cứu sách, xem thông tin sách, thuê sách và xem danh sách sách mình đang thuê.

Các use case của Admin:

- Đăng nhập Admin.
- Quản lý sách: thêm sách, xem danh sách sách, tìm kiếm sách, cập nhật sách, xóa sách.
- Quản lý khách hàng: thêm khách hàng, xem danh sách khách hàng, tìm kiếm khách hàng, cập nhật khách hàng, xóa khách hàng.
- Quản lý đơn thuê: tạo đơn thuê, xem danh sách đơn thuê, xem chi tiết đơn thuê, ghi nhận trả sách.
- Xem báo cáo: thống kê sách đang thuê, sách có sẵn và số lượt thuê theo sách.

Các use case của Customer:

- Đăng nhập Customer.
- Tìm kiếm sách.
- Xem thông tin sách.
- Xem trạng thái sách.
- Chọn thuê sách.
- Xem sách đang thuê của bản thân.
- Đăng xuất.

Mô tả Use Case Diagram bằng văn bản:

```
Admin --> Đăng nhập
Admin --> Quản lý sách
Admin --> Quản lý khách hàng
Admin --> Quản lý đơn thuê
Admin --> Xem báo cáo

Customer --> Đăng nhập
Customer --> Tìm kiếm sách
Customer --> Xem thông tin sách
Customer --> Xem trạng thái sách
Customer --> Thuê sách
Customer --> Xem sách đang thuê
```

Hình 1. Use Case Diagram cho hệ thống quản lý thuê sách (có thể vẽ lại bằng draw.io dựa trên mô tả trên).

\pagebreak

IE221.E12.CN2 - Kỹ thuật lập trình Python

# Chương 4: Triển khai lập trình và Diễn giải

Thư viện và khởi tạo

- `pyodbc`: thư viện dùng để kết nối Python với SQL Server thông qua ODBC Driver.
- `datetime`: thư viện xử lý ngày tháng, dùng để kiểm tra ngày dự kiến trả sách và ghi nhận thời gian thuê/trả.
- `pytest`: framework kiểm thử tự động, dùng để kiểm tra các chức năng service và dữ liệu.
- Các module nội bộ của dự án được chia thành hai nhóm chính: `services` và `menus`.

Kết nối cơ sở dữ liệu

File `config.py` lưu thông tin cấu hình kết nối gồm server, database, username, password và driver. File `db.py` sử dụng các thông tin này để tạo kết nối SQL Server. Hàm `get_connection` trả về connection nếu kết nối thành công, ngược lại in thông báo lỗi và trả về `None`.

Các hàm dùng chung trong `db.py`:

- `fetch_all(query, params=None)`: thực hiện truy vấn và trả về danh sách dòng dữ liệu.
- `fetch_one(query, params=None)`: thực hiện truy vấn và trả về một dòng dữ liệu đầu tiên.
- `execute_query(query, params=None)`: thực hiện các câu lệnh thay đổi dữ liệu như `INSERT`, `UPDATE`, `DELETE`.
- `execute_insert_and_get_id(query, params=None)`: thực hiện insert và lấy ID được sinh ra.

Cấu trúc cơ sở dữ liệu

Database của dự án có tên `BookRentalStore`. Các bảng chính gồm:

1. Bảng `Books`:

- `BookID`: khóa chính, tự tăng.
- `BookCode`: mã sách, duy nhất.
- `Title`: tên sách.
- `Author`: tác giả.
- `Category`: thể loại.
- `Publisher`: nhà xuất bản.
- `PublishYear`: năm xuất bản.
- `BookStatus`: trạng thái sách, chỉ nhận `Available` hoặc `Rented`.

2. Bảng `Customers`:

- `CustomerID`: khóa chính, tự tăng.
- `CustomerCode`: mã khách hàng, duy nhất.
- `FullName`: họ tên khách hàng.
- `Phone`: số điện thoại.
- `Address`: địa chỉ.
- `Email`: email.

3. Bảng `Users`:

- `UserID`: khóa chính, tự tăng.
- `Username`: tên đăng nhập, duy nhất.
- `Password`: mật khẩu.
- `Role`: vai trò, chỉ nhận `Admin` hoặc `Customer`.
- `CustomerID`: khóa ngoại liên kết đến `Customers`, có thể rỗng đối với tài khoản Admin.

4. Bảng `RentalOrders`:

- `OrderID`: khóa chính, tự tăng.
- `OrderCode`: mã đơn thuê, duy nhất.
- `CustomerID`: khóa ngoại liên kết đến khách hàng.
- `RentDate`: ngày thuê, mặc định là ngày hiện tại.
- `ExpectedReturnDate`: ngày dự kiến trả.
- `ReturnDate`: ngày trả thực tế, có thể rỗng khi đơn đang thuê.
- `OrderStatus`: trạng thái đơn, gồm `Renting` hoặc `Returned`.

5. Bảng `RentalOrderDetails`:

- `OrderDetailID`: khóa chính, tự tăng.
- `OrderID`: khóa ngoại liên kết đến `RentalOrders`.
- `BookID`: khóa ngoại liên kết đến `Books`.

Các ràng buộc quan trọng:

- `BookCode`, `CustomerCode`, `OrderCode` và `Username` là duy nhất.
- `RentalOrderDetails.BookID` tham chiếu `Books.BookID`.
- `RentalOrderDetails.OrderID` tham chiếu `RentalOrders.OrderID`.
- `RentalOrders.CustomerID` tham chiếu `Customers.CustomerID`.
- `Users.CustomerID` tham chiếu `Customers.CustomerID`.
- `ExpectedReturnDate >= RentDate`.
- `ReturnDate` phải rỗng hoặc lớn hơn/bằng `RentDate`.

Màn hình menu chính

File `main.py` gọi hàm `show_main_menu()` để khởi động chương trình. Menu chính có ba lựa chọn: đăng nhập dành cho Admin, đăng nhập dành cho Customer và thoát chương trình. Từ lựa chọn của người dùng, hệ thống gọi các hàm xử lý đăng nhập trong `menus/main_menu.py`.

Xử lý đăng nhập

Chức năng đăng nhập được triển khai trong `auth_service.py` thông qua hàm `login_by_role(username, password, expected_role)`. Hàm này truy vấn bảng `Users`, kết hợp với bảng `Customers` để lấy thêm thông tin khách hàng nếu tài khoản thuộc vai trò Customer.

Quy trình đăng nhập:

- Người dùng nhập username và password.
- Hệ thống kiểm tra thông tin không được để trống.
- Hệ thống gọi `login_by_role`.
- Nếu đăng nhập Admin thành công, chương trình hiển thị `show_admin_menu`.
- Nếu đăng nhập Customer thành công, chương trình hiển thị `show_customer_menu`.
- Nếu sai thông tin, chương trình hiển thị thông báo lỗi.

Quản lý sách

Các hàm xử lý sách được đặt trong `book_service.py` và giao diện menu được đặt trong `book_menu.py`. Nhóm chức năng này cho phép Admin quản lý dữ liệu sách trong bảng `Books`.

Các chức năng chính:

- `get_all_books`: lấy toàn bộ danh sách sách.
- `get_book_by_code`: lấy thông tin sách theo mã sách.
- `search_books`: tìm kiếm sách theo mã, tên, tác giả hoặc thể loại.
- `add_book`: thêm sách mới vào cơ sở dữ liệu.
- `update_book`: cập nhật thông tin sách theo mã sách.
- `delete_book`: xóa sách nếu sách tồn tại và đang ở trạng thái `Available`.
- `is_book_code_exists`: kiểm tra mã sách đã tồn tại hay chưa.

Quản lý khách hàng

Các hàm xử lý khách hàng được đặt trong `customer_service.py` và phần menu nằm trong `customer_manage_menu.py`. Chức năng này hỗ trợ Admin quản lý thông tin khách hàng.

Các chức năng chính:

- `get_all_customers`: lấy danh sách khách hàng.
- `get_customer_by_code`: lấy khách hàng theo mã.
- `search_customers`: tìm kiếm khách hàng theo mã, họ tên hoặc số điện thoại.
- `add_customer`: thêm khách hàng.
- `update_customer`: cập nhật thông tin khách hàng.
- `delete_customer`: xóa khách hàng sau khi kiểm tra điều kiện liên quan đến đơn thuê.
- `has_active_rental`: kiểm tra khách hàng có đơn thuê đang ở trạng thái `Renting` hay không.

Quản lý đơn thuê

Phần xử lý đơn thuê nằm trong `order_service.py` và `order_menu.py`. Đây là nghiệp vụ trung tâm của hệ thống vì tác động đồng thời đến bảng đơn thuê, chi tiết đơn thuê và trạng thái sách.

Các chức năng chính:

- `generate_order_code`: sinh mã đơn thuê theo dạng `O001`, `O002`, ...
- `get_customer_by_code`: kiểm tra và lấy khách hàng theo mã.
- `get_book_by_code`: kiểm tra và lấy sách theo mã.
- `get_order_by_code`: lấy thông tin đơn thuê theo mã.
- `get_all_orders`: lấy toàn bộ danh sách đơn thuê.
- `get_order_details`: lấy danh sách sách thuộc một đơn thuê.
- `create_rental_order`: tạo đơn thuê mới.
- `return_rental_order`: ghi nhận trả sách.

Quy trình tạo đơn thuê:

1. Nhập mã khách hàng, danh sách mã sách và ngày dự kiến trả.
2. Kiểm tra khách hàng tồn tại.
3. Kiểm tra danh sách sách không rỗng.
4. Kiểm tra ngày dự kiến trả đúng định dạng và không nhỏ hơn ngày hiện tại.
5. Chuẩn hóa mã sách, loại bỏ khoảng trắng và chuyển về chữ hoa.
6. Kiểm tra không có mã sách trùng trong cùng một đơn.
7. Kiểm tra từng sách tồn tại và đang `Available`.
8. Tạo mã đơn thuê mới.
9. Bắt đầu transaction.
10. Thêm dữ liệu vào `RentalOrders`.
11. Thêm từng sách vào `RentalOrderDetails`.
12. Cập nhật trạng thái sách thành `Rented`.
13. Commit nếu thành công hoặc rollback nếu xảy ra lỗi.

Quy trình trả sách:

1. Nhập mã đơn thuê cần trả.
2. Kiểm tra đơn thuê tồn tại.
3. Kiểm tra đơn chưa được trả trước đó.
4. Bắt đầu transaction.
5. Cập nhật `ReturnDate` bằng `GETDATE()` và `OrderStatus` thành `Returned`.
6. Cập nhật các sách thuộc đơn về trạng thái `Available`.
7. Commit nếu thành công hoặc rollback nếu xảy ra lỗi.

Chức năng dành cho Customer

Phần chức năng dành cho Customer được triển khai trong `customer_user_service.py` và `customer_menu.py`. Sau khi đăng nhập, khách hàng có thể thao tác với dữ liệu liên quan đến việc tra cứu và thuê sách.

Các chức năng chính:

- Tìm kiếm sách theo mã, tên sách, tác giả hoặc thể loại.
- Xem thông tin chi tiết của một sách.
- Xem sách theo trạng thái `Available` hoặc `Rented`.
- Chọn thuê một hoặc nhiều sách.
- Xem danh sách sách bản thân đang thuê.

Khi Customer thuê sách, hệ thống sử dụng logic tương tự tạo đơn thuê của Admin: kiểm tra mã sách, trạng thái sách, ngày dự kiến trả và cập nhật dữ liệu liên quan trong database.

Báo cáo thống kê

Phần báo cáo được triển khai trong `report_service.py` và `report_menu.py`. Mục tiêu của chức năng này là hỗ trợ Admin theo dõi nhanh tình hình sách trong cửa hàng.

Các báo cáo chính:

- Thống kê tổng số sách đang được thuê.
- Thống kê tổng số sách có sẵn.
- Thống kê số lượt thuê theo từng sách.

Truy vấn số lượt thuê theo sách sử dụng phép `LEFT JOIN` giữa `Books` và `RentalOrderDetails`, sau đó nhóm theo thông tin sách để đếm số lần sách xuất hiện trong các đơn thuê.

Kiểm thử chương trình

Dự án có hai file kiểm thử chính:

- `test_order_automation.py`: kiểm thử các chức năng liên quan đến đơn thuê, tạo đơn, trả sách, kiểm tra khách hàng, kiểm tra sách và lấy chi tiết đơn.
- `test_menu_automation.py`: kiểm thử các service chính của sách, khách hàng, đơn thuê, tính toàn vẹn dữ liệu và các trường hợp đặc biệt.

Kết quả kiểm thử được ghi nhận trong báo cáo test của dự án:

- Tổng số test: 32.
- Số test pass: 32.
- Số test fail: 0.
- Tỷ lệ pass: 100%.
- Các nhóm chức năng đã kiểm thử: tạo mã đơn, lấy khách hàng, lấy sách, tạo đơn thuê, trả sách, lấy thông tin đơn, tìm kiếm, kiểm tra trạng thái sách, kiểm tra trạng thái đơn và kiểm tra ngày thuê/trả.

Các test quan trọng:

- Không cho tạo đơn với khách hàng không tồn tại.
- Không cho tạo đơn với danh sách sách rỗng.
- Không cho ngày dự kiến trả nhỏ hơn ngày thuê.
- Không cho trùng sách trong cùng một đơn.
- Không cho thuê sách không tồn tại hoặc không còn `Available`.
- Khi trả sách, đơn phải tồn tại và chưa được trả trước đó.
- Trạng thái sách chỉ thuộc `Available` hoặc `Rented`.
- Trạng thái đơn chỉ thuộc `Renting` hoặc `Returned`.

\pagebreak

IE221.E12.CN2 - Kỹ thuật lập trình Python

# Chương 5: Kết luận

## 5.1. Ưu điểm đã làm được

Dự án đã xây dựng được một ứng dụng quản lý thuê sách bằng Python, kết nối cơ sở dữ liệu SQL Server và triển khai được các chức năng cốt lõi của một hệ thống cho thuê sách. Các kết quả đạt được gồm:

- Xây dựng được menu chính phân quyền theo Admin và Customer.
- Xây dựng được chức năng đăng nhập theo vai trò.
- Xây dựng được nhóm chức năng quản lý sách: xem, tìm kiếm, thêm, cập nhật và xóa có điều kiện.
- Xây dựng được nhóm chức năng quản lý khách hàng: xem, tìm kiếm, thêm, cập nhật và kiểm tra trước khi xóa.
- Xây dựng được chức năng tạo đơn thuê nhiều sách trong một đơn.
- Kiểm tra được các điều kiện nghiệp vụ quan trọng như khách hàng tồn tại, sách tồn tại, sách có sẵn, ngày trả hợp lệ và không trùng sách trong cùng đơn.
- Xây dựng được chức năng ghi nhận trả sách và cập nhật đồng bộ trạng thái sách.
- Thiết kế được cơ sở dữ liệu có khóa chính, khóa ngoại, ràng buộc duy nhất và ràng buộc kiểm tra dữ liệu.
- Sử dụng transaction cho các nghiệp vụ quan trọng nhằm đảm bảo tính nhất quán dữ liệu.
- Xây dựng được chức năng báo cáo thống kê sách đang thuê, sách có sẵn và số lượt thuê theo sách.
- Có kiểm thử tự động bằng `pytest` với kết quả 32/32 test pass.

## 5.2. Nhược điểm chưa làm được

Bên cạnh các chức năng đã hoàn thành, dự án vẫn còn một số hạn chế:

- Giao diện hiện tại là console, chưa có giao diện đồ họa hoặc giao diện web nên trải nghiệm người dùng còn đơn giản.
- Mật khẩu đang được lưu dạng văn bản thường, chưa áp dụng mã hóa hoặc băm mật khẩu.
- Chưa có chức năng đăng ký tài khoản Customer trực tiếp từ chương trình.
- Chưa có chức năng tính phí thuê sách, phí trễ hạn hoặc quản lý thanh toán.
- Chưa có chức năng gia hạn ngày trả sách.
- Chưa có phân trang hoặc lọc nâng cao khi dữ liệu sách và khách hàng tăng nhiều.
- Chưa xử lý đầy đủ các trường hợp đồng thời nhiều người dùng cùng thuê một sách tại cùng thời điểm.
- Một số câu truy vấn và hàm service vẫn cần được rà soát thêm để chuẩn hóa cú pháp và thông báo tiếng Việt.

## 5.3. Hướng phát triển

Trong tương lai, hệ thống có thể được phát triển thêm theo các hướng sau:

- Xây dựng giao diện đồ họa bằng Tkinter, PyQt hoặc giao diện web bằng Flask/Django.
- Bổ sung chức năng đăng ký tài khoản khách hàng.
- Mã hóa mật khẩu người dùng để tăng tính bảo mật.
- Bổ sung quản lý phí thuê, tiền cọc, phí phạt khi trả trễ và lịch sử thanh toán.
- Bổ sung chức năng gia hạn đơn thuê.
- Bổ sung chức năng tìm kiếm nâng cao theo nhiều tiêu chí như tác giả, năm xuất bản, thể loại và trạng thái.
- Bổ sung báo cáo doanh thu, báo cáo khách hàng thuê nhiều và sách được thuê nhiều nhất.
- Tối ưu xử lý đồng thời và khóa dữ liệu khi nhiều người dùng cùng thao tác.
- Đóng gói ứng dụng để dễ triển khai trên máy khác.
- Tích hợp xuất báo cáo ra Excel hoặc PDF.

\pagebreak

IE221.E12.CN2 - Kỹ thuật lập trình Python

# TÀI LIỆU THAM KHẢO

Python Software Foundation, "Python Documentation," [Online]. Available: https://docs.python.org/3/. (accessed 01-May-2026).

Microsoft, "SQL Server Documentation," [Online]. Available: https://learn.microsoft.com/en-us/sql/sql-server/. (accessed 01-May-2026).

Microsoft, "ODBC Driver for SQL Server," [Online]. Available: https://learn.microsoft.com/en-us/sql/connect/odbc/microsoft-odbc-driver-for-sql-server. (accessed 01-May-2026).

pyodbc contributors, "pyodbc Wiki," [Online]. Available: https://github.com/mkleehammer/pyodbc/wiki. (accessed 01-May-2026).

pytest, "pytest Documentation," [Online]. Available: https://docs.pytest.org/. (accessed 01-May-2026).

Microsoft, "Transactions - SQL Server," [Online]. Available: https://learn.microsoft.com/en-us/sql/t-sql/language-elements/transactions-transact-sql. (accessed 01-May-2026).

\pagebreak

IE221.E12.CN2 - Kỹ thuật lập trình Python

# PHỤ LỤC

Phụ lục A. Cấu trúc thư mục dự án

```
book_rental_project/
├── config.py
├── db.py
├── main.py
├── menus/
│   ├── main_menu.py
│   ├── admin_menu.py
│   ├── book_menu.py
│   ├── customer_menu.py
│   ├── customer_manage_menu.py
│   ├── order_menu.py
│   └── report_menu.py
├── services/
│   ├── auth_service.py
│   ├── book_service.py
│   ├── customer_service.py
│   ├── customer_user_service.py
│   ├── order_service.py
│   └── report_service.py
├── SQL Server Scripts1/
│   └── init_database.sql
├── test_order_automation.py
├── test_menu_automation.py
├── RUN_TESTS.py
├── TEST_REPORT.md
└── TEST_EXECUTION_SUMMARY.txt
```

Phụ lục B. Cấu hình kết nối cơ sở dữ liệu

```python
SERVER = r'DESKTOP-ACIIC93\SQLEXPRESS'
DATABASE = 'BookRentalStore'
USERNAME = 'tin_nguyen'
PASSWORD = '123456'
DRIVER = 'ODBC Driver 17 for SQL Server'
```

Phụ lục C. Hàm kết nối và truy vấn dữ liệu dùng chung

```python
def get_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{{DRIVER}}};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            f"UID={USERNAME};"
            f"PWD={PASSWORD};"
        )
        return conn
    except Exception as e:
        print("Kết nối database thất bại.")
        print("Chi tiết lỗi:", e)
        return None

def fetch_all(query, params=None):
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print("Lỗi fetch_all:", e)
        return []
    finally:
        conn.close()
```

Phụ lục D. Mô tả bảng dữ liệu chính

```sql
CREATE TABLE Books (
    BookID INT IDENTITY(1,1) PRIMARY KEY,
    BookCode VARCHAR(20) NOT NULL UNIQUE,
    Title NVARCHAR(200) NOT NULL,
    Author NVARCHAR(100) NOT NULL,
    Category NVARCHAR(100),
    Publisher NVARCHAR(100),
    PublishYear INT,
    BookStatus VARCHAR(20) NOT NULL
);

CREATE TABLE Customers (
    CustomerID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerCode VARCHAR(20) NOT NULL UNIQUE,
    FullName NVARCHAR(100) NOT NULL,
    Phone VARCHAR(20),
    Address NVARCHAR(200),
    Email VARCHAR(100)
);

CREATE TABLE RentalOrders (
    OrderID INT IDENTITY(1,1) PRIMARY KEY,
    OrderCode VARCHAR(20) NOT NULL UNIQUE,
    CustomerID INT NOT NULL,
    RentDate DATETIME NOT NULL DEFAULT GETDATE(),
    ExpectedReturnDate DATETIME NOT NULL,
    ReturnDate DATETIME,
    OrderStatus VARCHAR(20) NOT NULL
);

CREATE TABLE RentalOrderDetails (
    OrderDetailID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID INT NOT NULL,
    BookID INT NOT NULL
);
```

Phụ lục E. Logic tạo đơn thuê

```python
def create_rental_order(customer_code, book_codes, expected_return_date):
    customer = get_customer_by_code(customer_code)
    if not customer:
        return False, "Khách hàng không tồn tại."

    if not book_codes:
        return False, "Thông tin sách được thuê trống."

    expected_date = datetime.strptime(expected_return_date, "%Y-%m-%d")
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if expected_date < today:
        return False, "Ngày dự kiến trả phải sau ngày thuê."

    normalized_codes = []
    seen = set()
    for code in book_codes:
        upper_code = code.strip().upper()
        if upper_code in seen:
            return False, "Không được trùng sách trong cùng đơn thuê."
        seen.add(upper_code)
        normalized_codes.append(upper_code)

    for code in normalized_codes:
        book = get_book_by_code(code)
        if not book:
            return False, "Sách không tồn tại."
        if book.BookStatus != "Available":
            return False, "Sách hiện không sẵn sàng để thuê."

    # Sau khi kiểm tra hợp lệ, hệ thống tạo RentalOrders,
    # tạo RentalOrderDetails và cập nhật Books.BookStatus trong transaction.
```

Phụ lục F. Logic trả sách

```python
def return_rental_order(order_code):
    order = get_order_by_code(order_code)
    if not order:
        return False, "Đơn thuê không tồn tại."

    if order.OrderStatus == "Returned":
        return False, "Đơn thuê này đã được hoàn trả."

    # Trong transaction:
    # 1. Cập nhật RentalOrders.ReturnDate = GETDATE()
    # 2. Cập nhật RentalOrders.OrderStatus = 'Returned'
    # 3. Cập nhật Books.BookStatus = 'Available'
    #    cho các sách thuộc đơn thuê.
```

Phụ lục G. Lệnh chạy kiểm thử

```bash
pytest test_order_automation.py test_menu_automation.py -v
```

Kết quả kiểm thử:

```text
Total Tests: 32
Passed: 32
Failed: 0
Pass Rate: 100%
```
