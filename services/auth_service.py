from db import fetch_one

def login_by_role(username, password, expected_role):
    query = """
        SELECT 
            u.UserID,
            u.Username,
            u.Password,
            u.Role,
            u.CustomerID,
            c.CustomerCode,
            c.FullName
        FROM Users u JOIN Customers c ON u.CustomerID = c.CustomerID
        WHERE u.Username = ? AND u.Password = ? AND u.Role = ?
    """
    return fetch_one(query, (username, password, expected_role))
