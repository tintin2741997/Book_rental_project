import pyodbc
from config import SERVER, DATABASE, USERNAME, PASSWORD, DRIVER

#Kết nối DB
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

# Hàm lấy tất cả giá trị được query ra
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

# Hàm lấy giá trị đầu tiên được query ra
def fetch_one(query, params=None): # params: tham số truyền vào câu SQL (mặc định None — không bắt buộc)
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchone()
    except Exception as e:
        print("Lỗi fetch_one:", e)
        return None
    finally:
        conn.close()

# Hàm thực thi query hay đổi dữ liệu như INSERT, UPDATE, DELETE
def execute_query(query, params=None):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit() #Lưu thay đổi vào DB
        return True
    except Exception as e:
        conn.rollback()
        print("Lỗi execute_query:", e)
        return False

def execute_insert_and_get_id(query, params=None):
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        row = cursor.fetchone()
        conn.commit()

        if row: #Nếu row không rỗng
            return row[0] #Lấy giá trị cột đầu tiên trong row
        return None
    except Exception as e:
        conn.rollback()
        print("Lỗi execute_insert_and_get_id:", e)
        return None

    finally:
        conn.close()